from unittest.mock import patch

from aviationapi.lib.messengers import (
    trigger_chart_post_processor as TriggerChartPostProcessorMessenger,
)
from aviationapi.lib.messengers import (
    trigger_chart_processor as TriggerChartProcessorMessenger,
)
from aviationapi.lib.models.AiracData import AiracData


@patch("aviationapi.lib.messengers.trigger_chart_processor.TOPIC.publish")
def test_publish_update_messages_for_airac_includes_source(mock_publish):
    airac_data = AiracData(airac="250417", source="faa_tpp")
    airac_data.is_packet_processed = {"A": False}

    TriggerChartProcessorMessenger.publish_update_messages_for_airac(airac_data)

    message_attributes = mock_publish.call_args.kwargs["MessageAttributes"]
    assert message_attributes["source"]["StringValue"] == "faa_tpp"


@patch("aviationapi.lib.messengers.trigger_chart_post_processor.TOPIC.publish")
def test_publish_success_message_includes_source(mock_publish):
    TriggerChartPostProcessorMessenger.publish_success_message(
        "250417", "A", "charts", "faa_tpp"
    )

    message_attributes = mock_publish.call_args.kwargs["MessageAttributes"]
    assert message_attributes["source"]["StringValue"] == "faa_tpp"
