import os

import boto3

from aviationapi.lib.chart_provider_keys import DEFAULT_CHART_PROVIDER

TOPIC_ARN = os.environ.get(
    "TRIGGER_CHART_POST_PROCESSOR_TOPIC_ARN", "trigger-chart-post-processor"
)
TOPIC = boto3.resource("sns").Topic(TOPIC_ARN)


def publish_success_message(
    airac, packet, cycle_chart_type, provider=DEFAULT_CHART_PROVIDER
):
    _publish_message(airac, packet, cycle_chart_type, provider)


def _publish_message(airac, packet, cycle_chart_type, provider=DEFAULT_CHART_PROVIDER):
    TOPIC.publish(
        Message=(
            f"Success status {cycle_chart_type} packet {packet} "
            f"for provider {provider} airac {airac}"
        ),
        MessageAttributes={
            "airac": {"DataType": "String", "StringValue": airac},
            "packet": {"DataType": "String", "StringValue": packet},
            "cycle_chart_type": {"DataType": "String", "StringValue": cycle_chart_type},
            "provider": {"DataType": "String", "StringValue": provider},
        },
    )
