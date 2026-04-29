from datetime import datetime
from unittest.mock import Mock, patch

from aviationapi.api.app.lib.collectors import (
    airac_data_collector as AiracDataCollector,
)
from aviationapi.lib.models.AiracData import AiracData, CycleChartTypes, CycleTypes


def _build_airac(source, cycle_chart_type):
    return AiracData(
        airac="250417",
        source=source,
        cycle_type=CycleTypes.CURRENT.value,
        cycle_chart_type=cycle_chart_type,
        valid_date=datetime(2025, 4, 17),
    )


@patch(
    "aviationapi.api.app.lib.collectors.airac_data_collector.AiracDataRepository.get_all_airac"
)
@patch("aviationapi.api.app.lib.collectors.airac_data_collector.get_providers")
def test_get_current_availability_aggregates_all_sources(
    mock_get_providers, mock_get_all_airac
):
    mock_get_providers.return_value = [Mock(source="faa_tpp"), Mock(source="uk_aip")]
    mock_get_all_airac.side_effect = [
        [
            _build_airac("faa_tpp", CycleChartTypes.CHARTS.value),
            _build_airac("faa_tpp", CycleChartTypes.CHART_SUPPLEMENT.value),
        ],
        _build_airac("uk_aip", CycleChartTypes.CHARTS.value),
    ]

    availability = AiracDataCollector.get_current_availability()

    assert [item["source"] for item in availability] == ["faa_tpp", "faa_tpp", "uk_aip"]
