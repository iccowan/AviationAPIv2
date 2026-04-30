from datetime import datetime
from unittest.mock import Mock, patch

from aviationapi.api.app.lib.collectors import airport_collector as AirportCollector
from aviationapi.lib.models.AiracData import AiracData, CycleChartTypes, CycleTypes


def _build_airac(provider, is_retrieveable=True):
    return AiracData(
        airac="250417",
        provider=provider,
        cycle_type=CycleTypes.CURRENT.value,
        cycle_chart_type=CycleChartTypes.CHARTS.value,
        valid_date=datetime(2025, 4, 17),
        is_retrieveable=is_retrieveable,
    )


@patch(
    "aviationapi.api.app.lib.collectors.airport_collector.AirportRepository.get_airport"
)
@patch(
    "aviationapi.api.app.lib.collectors.airport_collector.AiracDataRepository.get_airac"
)
@patch("aviationapi.api.app.lib.collectors.airport_collector.get_providers")
def test_get_current_charts_for_airport_returns_first_provider_match(
    mock_get_providers, mock_get_airac, mock_get_airport
):
    mock_get_providers.return_value = [
        Mock(provider="faa_tpp"),
        Mock(provider="uk_aip"),
    ]
    mock_get_airac.side_effect = [_build_airac("faa_tpp"), _build_airac("uk_aip")]
    mock_get_airport.side_effect = [
        None,
        Mock(dict=lambda: {"airport_data": {}, "charts": {}}),
    ]

    charts = AirportCollector.get_current_charts_for_airport("EGLL")

    assert charts == {"airport_data": {}, "charts": {}}
    mock_get_airport.assert_any_call("EGLL", "250417", "tpp", provider="uk_aip")


@patch("aviationapi.api.app.lib.collectors.airport_collector.logError")
@patch(
    "aviationapi.api.app.lib.collectors.airport_collector.AirportRepository.get_airport"
)
@patch(
    "aviationapi.api.app.lib.collectors.airport_collector.AiracDataRepository.get_airac"
)
@patch("aviationapi.api.app.lib.collectors.airport_collector.get_providers")
def test_get_current_charts_for_airport_logs_when_multiple_providers_match(
    mock_get_providers, mock_get_airac, mock_get_airport, mock_log_error
):
    mock_get_providers.return_value = [
        Mock(provider="faa_tpp"),
        Mock(provider="uk_aip"),
    ]
    mock_get_airac.side_effect = [_build_airac("faa_tpp"), _build_airac("uk_aip")]
    mock_get_airport.side_effect = [
        Mock(dict=lambda: {"provider": "faa"}),
        Mock(dict=lambda: {"provider": "uk"}),
    ]

    charts = AirportCollector.get_current_charts_for_airport("EGLL")

    assert charts == {"provider": "faa"}
    mock_log_error.assert_called_once()
