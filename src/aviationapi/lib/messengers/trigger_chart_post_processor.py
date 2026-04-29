import os

import boto3

from aviationapi.lib.chart_data_keys import DEFAULT_CHART_SOURCE

TOPIC_ARN = os.environ.get(
    "TRIGGER_CHART_POST_PROCESSOR_TOPIC_ARN", "trigger-chart-post-processor"
)
TOPIC = boto3.resource("sns").Topic(TOPIC_ARN)


def publish_success_message(
    airac, packet, cycle_chart_type, source=DEFAULT_CHART_SOURCE
):
    _publish_message(airac, packet, cycle_chart_type, source)


def _publish_message(airac, packet, cycle_chart_type, source=DEFAULT_CHART_SOURCE):
    TOPIC.publish(
        Message=(
            f"Success status {cycle_chart_type} packet {packet} "
            f"for source {source} airac {airac}"
        ),
        MessageAttributes={
            "airac": {"DataType": "String", "StringValue": airac},
            "packet": {"DataType": "String", "StringValue": packet},
            "cycle_chart_type": {"DataType": "String", "StringValue": cycle_chart_type},
            "source": {"DataType": "String", "StringValue": source},
        },
    )
