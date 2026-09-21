from aviationapi.lib.chart_provider_keys import (
    DEFAULT_CHART_PROVIDER,
    build_airport_data_key,
    build_provider_cycle_chart_type,
    parse_airport_data_key,
    parse_provider_cycle_chart_type,
)
from aviationapi.lib.models.AiracData import AiracData, CycleChartTypes


def test_build_airport_data_key_includes_provider():
    assert build_airport_data_key("faa_tpp", "tpp", "250417") == "faa_tpp::tpp::250417"


def test_parse_airport_data_key_supports_legacy_values():
    assert parse_airport_data_key("tpp::250417") == {
        "provider": DEFAULT_CHART_PROVIDER,
        "product": "tpp",
        "airac": "250417",
    }


def test_build_provider_cycle_chart_type_includes_provider():
    assert (
        build_provider_cycle_chart_type("faa_tpp", CycleChartTypes.CHARTS.value)
        == "faa_tpp::charts"
    )


def test_parse_provider_cycle_chart_type_supports_legacy_values():
    assert parse_provider_cycle_chart_type(CycleChartTypes.CHARTS.value) == {
        "provider": DEFAULT_CHART_PROVIDER,
        "cycle_chart_type": CycleChartTypes.CHARTS.value,
    }


def test_airac_data_defaults_provider_to_faa():
    airac_data = AiracData()

    assert airac_data.provider == DEFAULT_CHART_PROVIDER


def test_airac_data_initializes_processing_state_from_expected_jobs():
    airac_data = AiracData(expected_jobs=["job_a", "job_b"])

    assert airac_data.is_packet_processed == {"job_a": False, "job_b": False}
