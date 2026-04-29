from datetime import datetime
from unittest.mock import patch

from aviationapi.chart_pre_processor.app.lambda_function import (
    CHART_SOURCE,
    create_airac_data,
    get_current_airacs,
)
from aviationapi.lib.models.AiracData import AiracData, CycleChartTypes, CycleTypes


def _build_airac_data(cycle_type, cycle_chart_type):
    return AiracData(
        airac="250417",
        source=CHART_SOURCE,
        cycle_type=cycle_type,
        cycle_chart_type=cycle_chart_type,
        valid_date=datetime(2025, 4, 17),
    )


@patch(
    "aviationapi.chart_pre_processor.app.lambda_function.AiracDataRepository.get_airac"
)
def test_get_current_airacs_requests_faa_source(mock_get_airac):
    mock_get_airac.side_effect = [
        _build_airac_data(CycleTypes.CURRENT.value, CycleChartTypes.CHARTS.value),
        _build_airac_data(CycleTypes.NEXT.value, CycleChartTypes.CHARTS.value),
        _build_airac_data(
            CycleTypes.CURRENT.value, CycleChartTypes.CHART_SUPPLEMENT.value
        ),
        _build_airac_data(
            CycleTypes.NEXT.value, CycleChartTypes.CHART_SUPPLEMENT.value
        ),
    ]

    get_current_airacs()

    for call in mock_get_airac.call_args_list:
        assert call.kwargs["source"] == CHART_SOURCE


def test_create_airac_data_uses_provider_expected_jobs():
    airac_data = create_airac_data(
        airac="250417",
        cycle_type=CycleTypes.CURRENT.value,
        cycle_chart_type=CycleChartTypes.CHARTS.value,
        valid_date=datetime(2025, 4, 17),
    )

    assert airac_data.is_packet_processed == {
        "A": False,
        "B": False,
        "C": False,
        "D": False,
        "E": False,
    }
