from aviationapi.lib.chart_data_keys import (
    DEFAULT_CHART_SOURCE,
    build_airport_data_key,
    build_source_cycle_chart_type,
    parse_airport_data_key,
    parse_source_cycle_chart_type,
)
from aviationapi.lib.models.AiracData import AiracData, CycleChartTypes


def test_build_airport_data_key_includes_source():
    assert build_airport_data_key("faa_tpp", "tpp", "250417") == "faa_tpp::tpp::250417"


def test_parse_airport_data_key_supports_legacy_values():
    assert parse_airport_data_key("tpp::250417") == {
        "source": DEFAULT_CHART_SOURCE,
        "product": "tpp",
        "airac": "250417",
    }


def test_build_source_cycle_chart_type_includes_source():
    assert (
        build_source_cycle_chart_type("faa_tpp", CycleChartTypes.CHARTS.value)
        == "faa_tpp::charts"
    )


def test_parse_source_cycle_chart_type_supports_legacy_values():
    assert parse_source_cycle_chart_type(CycleChartTypes.CHARTS.value) == {
        "source": DEFAULT_CHART_SOURCE,
        "cycle_chart_type": CycleChartTypes.CHARTS.value,
    }


def test_airac_data_defaults_source_to_faa():
    airac_data = AiracData()

    assert airac_data.source == DEFAULT_CHART_SOURCE
