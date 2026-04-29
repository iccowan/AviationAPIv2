from aviationapi.chart_processor.app.providers.faa_tpp import FaaTppChartProvider
from aviationapi.chart_processor.app.providers.registry import get_expected_jobs
from aviationapi.lib.models.AiracData import CycleChartTypes


def test_faa_provider_returns_expected_jobs_for_charts():
    provider = FaaTppChartProvider()

    assert provider.get_expected_jobs(CycleChartTypes.CHARTS.value) == [
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
