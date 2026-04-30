from datetime import datetime
from unittest.mock import patch

from aviationapi.chart_post_processor.app.lambda_function import lambda_handler
from aviationapi.lib.models.AiracData import AiracData, CycleChartTypes, CycleTypes


def generate_handler_event(packet, airac, cycle_chart_type, source):
    return {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "packet": {"Type": "S", "Value": packet},
                        "airac": {"Type": "S", "Value": airac},
                        "cycle_chart_type": {
                            "Type": "S",
                            "Value": cycle_chart_type,
                        },
                        "source": {"Type": "S", "Value": source},
                    }
                }
            }
        ]
    }


@patch(
    "aviationapi.chart_post_processor.app.lambda_function.AiracDataRepository.put_airac"
)
@patch(
    "aviationapi.chart_post_processor.app.lambda_function.AiracDataRepository.get_airac_by_cycle_chart_type_and_airac"
)
def test_lambda_handler_uses_source_aware_airac_lookup(mock_get_airac, mock_put_airac):
    mock_get_airac.return_value = AiracData(
        airac="250417",
        source="faa_tpp",
        cycle_type=CycleTypes.CURRENT.value,
        cycle_chart_type=CycleChartTypes.CHARTS.value,
        valid_date=datetime(2025, 4, 17),
    )

    event = generate_handler_event(
        "A", "250417", CycleChartTypes.CHARTS.value, "faa_tpp"
    )

    lambda_handler(event, {})

    mock_get_airac.assert_called_once_with(
        "250417", CycleChartTypes.CHARTS.value, source="faa_tpp"
    )
    assert mock_put_airac.call_args.args[0].is_packet_processed["A"] is True
