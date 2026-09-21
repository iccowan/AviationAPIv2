import pytest

from aviationapi.lib.models.AiracData import CycleChartTypes
from aviationapi.lib.providers.registry import get_expected_jobs, get_providers


def test_get_providers_returns_faa_provider_metadata():
    providers = get_providers()

    assert [provider.provider for provider in providers] == ["faa_tpp"]


def test_get_expected_jobs_returns_chart_jobs():
    assert get_expected_jobs("faa_tpp", CycleChartTypes.CHARTS.value) == [
        "A",
        "B",
        "C",
        "D",
        "E",
    ]


def test_get_expected_jobs_returns_chart_supplement_job():
    assert get_expected_jobs("faa_tpp", CycleChartTypes.CHART_SUPPLEMENT.value) == [
        "ChartSupplement"
    ]


def test_get_expected_jobs_rejects_unknown_provider():
    with pytest.raises(
        ValueError, match="No chart provider registered for provider unknown"
    ):
        get_expected_jobs("unknown", CycleChartTypes.CHARTS.value)
