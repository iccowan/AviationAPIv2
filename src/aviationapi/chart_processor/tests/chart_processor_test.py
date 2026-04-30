from unittest.mock import Mock, patch

from aviationapi.chart_processor.app.lambda_function import lambda_handler


@patch("aviationapi.chart_processor.app.lambda_function.get_provider")
@patch(
    "aviationapi.lib.messengers.trigger_chart_post_processor.publish_success_message"
)
@patch("aviationapi.chart_processor.app.lambda_function.shutil.rmtree")
def test_lambda_handler_dispatches_to_provider(
    shutil_rmtree, publish_success_message, get_provider
):
    chart_provider = Mock()
    chart_provider.process_packet.return_value = {
        "success": True,
        "cycle_chart_type": "charts",
    }
    get_provider.return_value = chart_provider

    packet = "A"
    airac = "250417"
    event = generate_handler_event(packet, airac)

    lambda_handler(event, {})

    get_provider.assert_called_once_with("faa_tpp")
    chart_provider.process_packet.assert_called_once_with(packet, airac)
    publish_success_message.assert_called_once_with(airac, packet, "charts", "faa_tpp")


@patch("aviationapi.chart_processor.app.lambda_function.get_provider")
@patch("aviationapi.chart_processor.app.lambda_function.shutil.rmtree")
def test_lambda_handler_returns_error_when_provider_has_no_registration(
    shutil_rmtree, get_provider
):
    get_provider.return_value = None

    result = lambda_handler(generate_handler_event("A", "250417", "uk_aip"), {})

    assert result == 1
    shutil_rmtree.assert_not_called()


def generate_handler_event(packet, airac, provider="faa_tpp"):
    return {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "packet": {"Type": "S", "Value": packet},
                        "airac": {"Type": "S", "Value": airac},
                        "provider": {"Type": "S", "Value": provider},
                    }
                }
            }
        ]
    }
