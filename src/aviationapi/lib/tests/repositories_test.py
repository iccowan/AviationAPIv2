from datetime import datetime
from unittest.mock import patch

from aviationapi.lib.chart_data_keys import DEFAULT_CHART_SOURCE
from aviationapi.lib.models.AiracData import AiracData, CycleChartTypes
from aviationapi.lib.models.Airport import Airport
from aviationapi.lib.repositories import airac_data_repository as AiracDataRepository
from aviationapi.lib.repositories import airport_repository as AirportRepository


def test_generate_airport_key_includes_source():
    airport = Airport("250417")
    airport.source = "faa_tpp"
    airport.airport_data.icao_ident = "KJFK"

    assert AirportRepository.generate_key(airport) == {
        "unique_airport_id": "KJFK",
        "chart_type::airac": "faa_tpp::tpp::250417",
    }


@patch("aviationapi.lib.repositories.airport_repository._get")
def test_get_airport_falls_back_to_legacy_default_source(mock_get):
    mock_get.side_effect = [
        None,
        {"airport_data": {"icao_ident": "KJFK"}, "charts": {}},
    ]

    airport = AirportRepository.get_airport("KJFK", "250417", "tpp")

    assert mock_get.call_count == 2
    assert airport.source == DEFAULT_CHART_SOURCE


@patch("aviationapi.lib.repositories.airac_data_repository._put")
def test_put_airac_encodes_source_into_storage_key(mock_put):
    airac_data = AiracData(
        airac="250417",
        source="faa_tpp",
        cycle_chart_type=CycleChartTypes.CHARTS.value,
        valid_date=datetime(2025, 4, 17),
    )

    AiracDataRepository.put_airac(airac_data)

    stored_item = mock_put.call_args.args[0]
    assert stored_item["source"] == "faa_tpp"
    assert stored_item["cycle_chart_type"] == "faa_tpp::charts"


@patch("aviationapi.lib.repositories.airac_data_repository._get")
def test_get_airac_falls_back_to_legacy_default_source(mock_get):
    mock_get.side_effect = [
        None,
        {
            "airac": "250417",
            "cycle_type": "current",
            "cycle_chart_type": CycleChartTypes.CHARTS.value,
            "valid_date": "2025-04-17",
            "is_retrieveable": False,
            "is_packet_processed": {},
        },
    ]

    airac_data = AiracDataRepository.get_airac("current", CycleChartTypes.CHARTS.value)

    assert mock_get.call_count == 2
    assert airac_data.source == DEFAULT_CHART_SOURCE
    assert airac_data.cycle_chart_type == CycleChartTypes.CHARTS.value


@patch("aviationapi.lib.repositories.airac_data_repository._query")
def test_get_all_airac_filters_to_requested_source(mock_query):
    mock_query.return_value = [
        {
            "airac": "250417",
            "cycle_type": "current",
            "cycle_chart_type": CycleChartTypes.CHARTS.value,
            "valid_date": "2025-04-17",
            "is_retrieveable": False,
            "is_packet_processed": {},
        },
        {
            "airac": "250417",
            "source": "faa_tpp",
            "cycle_type": "current",
            "cycle_chart_type": "faa_tpp::charts",
            "valid_date": "2025-04-18",
            "is_retrieveable": False,
            "is_packet_processed": {},
        },
        {
            "airac": "250417",
            "source": "uk_aip",
            "cycle_type": "current",
            "cycle_chart_type": "uk_aip::charts",
            "valid_date": "2025-04-17",
            "is_retrieveable": False,
            "is_packet_processed": {},
        },
    ]

    airac_data = AiracDataRepository.get_all_airac("current", source="faa_tpp")

    assert type(airac_data) is not list
    assert airac_data.source == "faa_tpp"
    assert airac_data.valid_date.strftime("%Y-%m-%d") == "2025-04-18"
