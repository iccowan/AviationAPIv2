import boto3
import os

TOPIC_ARN = os.environ.get("TRIGGER_CHART_POST_PROCESSOR_TOPIC_ARN", "trigger-chart-post-processor")
TOPIC = boto3.resource("sns").Topic(TOPIC_ARN)

def publish_success_message(airac, packet):
    _publish_message(airac, packet)

def _publish_message(airac, packet):
    TOPIC.publish(
        Message=f"Success status packet {packet} for airac {airac}",
        MessageAttributes={
            "airac": {
                "DataType": "String",
                "StringValue": airac
            },
            "packet": {
                "DataType": "String",
                "StringValue": packet
            }
        }
    )
