import os

import boto3

from aviationapi.lib.chart_provider_keys import DEFAULT_CHART_PROVIDER

TOPIC_ARN = os.environ.get(
    "TRIGGER_CHART_PROCESSOR_TOPIC_ARN", "trigger-chart-processor"
)
TOPIC = boto3.resource("sns").Topic(TOPIC_ARN)


def publish_update_messages_for_airac(airac_data):
    for packet, is_packet_processed in airac_data.is_packet_processed.items():
        if not is_packet_processed:
            _publish_message(
                airac_data.airac,
                packet,
                getattr(airac_data, "provider", DEFAULT_CHART_PROVIDER),
            )


def _publish_message(airac, packet, provider=DEFAULT_CHART_PROVIDER):
    TOPIC.publish(
        Message=f"Update packet {packet} for provider {provider} airac {airac}",
        MessageAttributes={
            "airac": {"DataType": "String", "StringValue": airac},
            "packet": {"DataType": "String", "StringValue": packet},
            "provider": {"DataType": "String", "StringValue": provider},
        },
    )
