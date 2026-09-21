from aviationapi.chart_processor.app.providers.faa_tpp import FaaTppChartProvider
from aviationapi.chart_processor.app.providers.registry import get_provider


def test_get_provider_returns_faa_chart_processor():
    assert isinstance(get_provider("faa_tpp"), FaaTppChartProvider)
