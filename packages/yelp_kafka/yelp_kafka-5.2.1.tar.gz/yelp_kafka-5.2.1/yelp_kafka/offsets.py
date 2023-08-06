# -*- coding: utf-8 -*-
# Copyright 2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import defaultdict
from collections import namedtuple

import six
from kafka.common import BrokerResponseError
from kafka.common import check_error
from kafka.common import OffsetCommitRequest
from kafka.common import OffsetFetchRequest
from kafka.common import OffsetFetchResponse
from kafka.common import OffsetRequest
from kafka.common import OffsetResponse
from kafka.common import UnknownTopicOrPartitionError
from kafka.util import kafka_bytestring

from yelp_kafka.error import InvalidOffsetStorageError
from yelp_kafka.error import OffsetCommitError
from yelp_kafka.error import UnknownPartitions
from yelp_kafka.error import UnknownTopic


PartitionOffsets = namedtuple(
    'PartitionOffsets',
    ['topic', 'partition', 'highmark', 'lowmark']
)
"""Tuple representing the offsets for a topic partition.

* **topic**\(``str``): Name of the topic
* **partition**\(``int``): Partition number
* **highmark**\(``int``): high watermark
* **lowmark**\(``int``): low watermark
"""

HIGH_WATERMARK = "high"
LOW_WATERMARK = "low"


def pluck_topic_offset_or_zero_on_unknown(resp):
    try:
        check_error(resp)
    except UnknownTopicOrPartitionError:
        # If the server doesn't have any commited offsets by this group for
        # this topic, assume it's zero.
        pass
    # The API spec says server wont set an error, but 0.8.1.1 does. The actual
    # check is if the offset is -1.
    if resp.offset == -1:
        return OffsetFetchResponse(
            resp.topic,
            resp.partition,
            0,
            resp.metadata,
            0,
        )
    return resp


def _check_fetch_response_error(resp):
    try:
        check_error(resp)
    except BrokerResponseError:
        # In case of error we set the offset to (-1,)
        return OffsetResponse(
            resp.topic,
            resp.partition,
            resp.error,
            (-1,),
        )
    return resp


def _check_commit_response_error(resp):
    try:
        check_error(resp)
    except BrokerResponseError as e:
        exception = OffsetCommitError(
            resp.topic,
            resp.partition,
            e.message
        )
        return exception


def _validate_topics_list_or_dict(topics):
    if isinstance(topics, dict):
        return topics
    elif isinstance(topics, (list, set, tuple)):
        return dict([(topic, []) for topic in topics])
    else:
        raise TypeError("Invalid topics: {topics}. It must be either a "
                        "list of topics or a dict "
                        "topic: [partitions]".format(topics=topics))


def _verify_topics_and_partitions(kafka_client, topics, raise_on_error):
    topics = _validate_topics_list_or_dict(topics)
    valid_topics = {}
    for topic, partitions in six.iteritems(topics):
        # Check topic exists
        if not kafka_client.has_metadata_for_topic(topic):
            if raise_on_error:
                raise UnknownTopic("Topic {topic!r} does not exist in "
                                   "kafka".format(topic=topic))
            else:
                continue
        if partitions:
            # Check the partitions really exist
            unknown_partitions = set(partitions) - \
                set(kafka_client.get_partition_ids_for_topic(topic))
            if unknown_partitions:
                if raise_on_error:
                    raise UnknownPartitions(
                        "Partitions {partitions!r} for topic {topic!r} do not"
                        "exist in kafka".format(
                            partitions=unknown_partitions,
                            topic=topic,
                        )
                    )
                else:
                    # We only use the available partitions in this case
                    partitions = set(partitions) - unknown_partitions
        else:
            # Default get all partitions metadata
            partitions = kafka_client.get_partition_ids_for_topic(topic)
        valid_topics[topic] = partitions
    return valid_topics


def _verify_commit_offsets_requests(kafka_client, new_offsets, raise_on_error):
    type_error_str = (
        "Invalid new_offsets: {new_offsets}. It must be a "
        "dict of the format: "
        "{{<topic>: {{<partition>: <offset>}}}}"
    ).format(new_offsets=new_offsets)

    if not isinstance(new_offsets, dict):
        raise TypeError(type_error_str)

    for topic, partitions in six.iteritems(new_offsets):
        if not isinstance(partitions, dict):
            raise TypeError(type_error_str)

    topics = dict(
        (topic, partitions.keys())
        for topic, partitions in six.iteritems(new_offsets)
    )

    valid_topics = _verify_topics_and_partitions(kafka_client, topics, raise_on_error)

    return dict(
        (topic, dict(
            (partition, new_offsets[topic][partition])
            for partition in partitions
        ))
        for topic, partitions in six.iteritems(valid_topics)
        if partitions
    )


def get_current_consumer_offsets(
    kafka_client,
    group,
    topics,
    raise_on_error=True,
    offset_storage='zookeeper',
):
    """ Get current consumer offsets.

    NOTE: This method does not refresh client metadata. It is up to the caller
    to avoid using stale metadata.

    If any partition leader is not available, the request fails for all the
    other topics. This is the tradeoff of sending all topic requests in batch
    and save both in performance and Kafka load.

    :param kafka_client: a connected KafkaClient
    :param group: kafka group_id
    :param topics: topic list or dict {<topic>: [partitions]}
    :param raise_on_error: if False the method ignores missing topics and
      missing partitions. It still may fail on the request send.
    :param offset_storage: String, one of {zookeeper, kafka}.
    :returns: a dict topic: partition: offset
    :raises:
      :py:class:`yelp_kafka.error.UnknownTopic`: upon missing
      topics and raise_on_error=True

      :py:class:`yelp_kafka.error.UnknownPartition`: upon missing
      partitions and raise_on_error=True

      :py:class:`yelp_kafka.error.InvalidOffsetStorageError: upon unknown
      offset_storage choice.

      FailedPayloadsError: upon send request error.
    """

    topics = _verify_topics_and_partitions(kafka_client, topics, raise_on_error)

    group_offset_reqs = [
        OffsetFetchRequest(kafka_bytestring(topic), partition)
        for topic, partitions in six.iteritems(topics)
        for partition in partitions
    ]

    group_offsets = {}

    if offset_storage == 'zookeeper':
        send_api = kafka_client.send_offset_fetch_request
    elif offset_storage == 'kafka':
        send_api = kafka_client.send_offset_fetch_request_kafka
    else:
        raise InvalidOffsetStorageError(offset_storage)

    if group_offset_reqs:
        # fail_on_error = False does not prevent network errors
        group_resps = send_api(
            group=kafka_bytestring(group),
            payloads=group_offset_reqs,
            fail_on_error=False,
            callback=pluck_topic_offset_or_zero_on_unknown,
        )
        for resp in group_resps:
            group_offsets.setdefault(
                resp.topic,
                {},
            )[resp.partition] = resp.offset

    return group_offsets


def get_topics_watermarks(kafka_client, topics, raise_on_error=True):
    """ Get current topic watermarks.

    NOTE: This method does not refresh client metadata. It is up to the caller
    to use avoid using stale metadata.

    If any partition leader is not available, the request fails for all the
    other topics. This is the tradeoff of sending all topic requests in batch
    and save both in performance and Kafka load.

    :param kafka_client: a connected KafkaClient
    :param topics: topic list or dict {<topic>: [partitions]}
    :param raise_on_error: if False the method ignores missing topics
      and missing partitions. It still may fail on the request send.
    :returns: a dict topic: partition: Part
    :raises:
      :py:class:`~yelp_kafka.error.UnknownTopic`: upon missing
      topics and raise_on_error=True

      :py:class:`~yelp_kafka.error.UnknownPartition`: upon missing
      partitions and raise_on_error=True

      FailedPayloadsError: upon send request error.
    """
    topics = _verify_topics_and_partitions(
        kafka_client,
        topics,
        raise_on_error,
    )
    highmark_offset_reqs = []
    lowmark_offset_reqs = []

    for topic, partitions in six.iteritems(topics):
        # Batch watermark requests
        for partition in partitions:
            # Request the the latest offset
            highmark_offset_reqs.append(
                OffsetRequest(
                    kafka_bytestring(topic), partition, -1, max_offsets=1
                )
            )
            # Request the earliest offset
            lowmark_offset_reqs.append(
                OffsetRequest(
                    kafka_bytestring(topic), partition, -2, max_offsets=1
                )
            )

    watermark_offsets = {}

    if not (len(highmark_offset_reqs) + len(lowmark_offset_reqs)):
        return watermark_offsets

    # fail_on_error = False does not prevent network errors
    highmark_resps = kafka_client.send_offset_request(
        highmark_offset_reqs,
        fail_on_error=False,
        callback=_check_fetch_response_error,
    )
    lowmark_resps = kafka_client.send_offset_request(
        lowmark_offset_reqs,
        fail_on_error=False,
        callback=_check_fetch_response_error,
    )

    # At this point highmark and lowmark should ideally have the same length.
    assert len(highmark_resps) == len(lowmark_resps)
    aggregated_offsets = defaultdict(lambda: defaultdict(dict))
    for resp in highmark_resps:
        aggregated_offsets[resp.topic][resp.partition]['highmark'] = \
            resp.offsets[0]
    for resp in lowmark_resps:
        aggregated_offsets[resp.topic][resp.partition]['lowmark'] = \
            resp.offsets[0]

    for topic, partition_watermarks in six.iteritems(aggregated_offsets):
        for partition, watermarks in six.iteritems(partition_watermarks):
            watermark_offsets.setdefault(
                topic,
                {},
            )[partition] = PartitionOffsets(
                topic,
                partition,
                watermarks['highmark'],
                watermarks['lowmark'],
            )
    return watermark_offsets


def _commit_offsets_to_watermark(
    kafka_client,
    group,
    topics,
    watermark,
    raise_on_error,
    offset_storage
):
    topics = _verify_topics_and_partitions(kafka_client, topics, raise_on_error)

    watermark_offsets = get_topics_watermarks(kafka_client, topics, raise_on_error)

    if watermark == HIGH_WATERMARK:
        group_offset_reqs = [
            OffsetCommitRequest(
                kafka_bytestring(topic), partition,
                watermark_offsets[topic][partition].highmark, None
            )
            for topic, partitions in six.iteritems(topics)
            for partition in partitions
        ]
    elif watermark == LOW_WATERMARK:
        group_offset_reqs = [
            OffsetCommitRequest(
                kafka_bytestring(topic), partition,
                watermark_offsets[topic][partition].lowmark, None
            )
            for topic, partitions in six.iteritems(topics)
            for partition in partitions
        ]
    else:
        raise ValueError(
            "Unknown watermark: {watermark}".format(watermark=watermark)
        )

    status = []
    if group_offset_reqs:
        if offset_storage in ['zookeeper', 'dual']:
            status = kafka_client.send_offset_commit_request(
                kafka_bytestring(group),
                group_offset_reqs,
                raise_on_error,
                callback=_check_commit_response_error
            )
        if offset_storage in ['kafka', 'dual']:
            status = kafka_client.send_offset_commit_request_kafka(
                kafka_bytestring(group),
                group_offset_reqs,
                raise_on_error,
                callback=_check_commit_response_error
            )

    return filter(None, status)


def advance_consumer_offsets(
    kafka_client,
    group,
    topics,
    raise_on_error=True,
    offset_storage='zookeeper',
):
    """Advance consumer offsets to the latest message in the topic
    partition (the high watermark).

    This method shall refresh the client metadata prior to updating
    the offsets.

    If any partition leader is not available, the request fails for all the
    other topics. This is the tradeoff of sending all topic requests in batch
    and save both in performance and Kafka load.

    :param kafka_client: a connected KafkaClient
    :param group: kafka group_id
    :param topics: topic list or dict {<topic>: [partitions]}
    :param raise_on_error: if False the method does not raise exceptions
      on missing topics/partitions. It may still fail on the request send.
    :param offset_storage: String, one of {zookeeper, kafka, dual}.
    :returns: a list of errors for each partition offset update that failed.
    :rtype: list [OffsetCommitError]
    :raises:
      :py:class:`yelp_kafka.error.UnknownTopic`: upon missing
      topics and raise_on_error=True

      :py:class:`yelp_kafka.error.UnknownPartition`: upon missing
      partitions and raise_on_error=True

      FailedPayloadsError: upon send request error.
    """
    kafka_client.load_metadata_for_topics()

    return _commit_offsets_to_watermark(
        kafka_client, group, topics,
        HIGH_WATERMARK, raise_on_error, offset_storage
    )


def rewind_consumer_offsets(
    kafka_client,
    group,
    topics,
    raise_on_error=True,
    offset_storage='zookeeper'
):
    """Rewind consumer offsets to the earliest message in the topic
    partition (the low watermark).

    This method shall refresh the client metadata prior to updating
    the offsets.

    If any partition leader is not available, the request fails for all the
    other topics. This is the tradeoff of sending all topic requests in batch
    and save both in performance and Kafka load.

    :param kafka_client: a connected KafkaClient
    :param group: kafka group_id
    :param topics: topic list or dict {<topic>: [partitions]}
    :param raise_on_error: if False the method does not raise exceptions
      on missing topics/partitions. It may still fail on the request send.
    :param offset_storage: String, one of {zookeeper, kafka, dual}.
    :returns: a list of errors for each partition offset update that failed.
    :rtype: list [OffsetCommitError]
    :raises:
      :py:class:`yelp_kafka.error.UnknownTopic`: upon missing
      topics and raise_on_error=True

      :py:class:`yelp_kafka.error.UnknownPartition`: upon missing
      partitions and raise_on_error=True

      FailedPayloadsError: upon send request error.
    """
    kafka_client.load_metadata_for_topics()

    return _commit_offsets_to_watermark(
        kafka_client, group, topics,
        LOW_WATERMARK, raise_on_error, offset_storage
    )


def set_consumer_offsets(
    kafka_client,
    group,
    new_offsets,
    raise_on_error=True,
    offset_storage='zookeeper',
):
    """Set consumer offsets to the specified offsets.

    This method does not validate the specified offsets, it is up to
    the caller to specify valid offsets within a topic partition.

    If any partition leader is not available, the request fails for all the
    other topics. This is the tradeoff of sending all topic requests in batch
    and save both in performance and Kafka load.

    :param kafka_client: a connected KafkaClient
    :param group: kafka group_id
    :param topics: dict {<topic>: {<partition>: <offset>}}
    :param raise_on_error: if False the method does not raise exceptions
      on errors encountered. It may still fail on the request send.
    :param offset_storage: String, one of {zookeeper, kafka, dual}.
    :returns: a list of errors for each partition offset update that failed.
    :rtype: list [OffsetCommitError]
    :raises:
      :py:class:`yelp_kafka.error.UnknownTopic`: upon missing
      topics and raise_on_error=True

      :py:class:`yelp_kafka.error.UnknownPartition`: upon missing
      partitions and raise_on_error=True

      :py:class:`exceptions.TypeError`: upon badly formatted input
      new_offsets

      FailedPayloadsError: upon send request error.
    """
    valid_new_offsets = _verify_commit_offsets_requests(
        kafka_client,
        new_offsets,
        raise_on_error
    )

    group_offset_reqs = [
        OffsetCommitRequest(
            kafka_bytestring(topic),
            partition,
            offset,
            None
        )
        for topic, new_partition_offsets in six.iteritems(valid_new_offsets)
        for partition, offset in six.iteritems(new_partition_offsets)
    ]

    status = []
    if group_offset_reqs:
        if offset_storage in ['zookeeper', 'dual']:
            status = kafka_client.send_offset_commit_request(
                kafka_bytestring(group),
                group_offset_reqs,
                raise_on_error,
                callback=_check_commit_response_error
            )
        if offset_storage in ['kafka', 'dual']:
            status = kafka_client.send_offset_commit_request_kafka(
                kafka_bytestring(group),
                group_offset_reqs,
                raise_on_error,
                callback=_check_commit_response_error
            )

    return filter(None, status)
