from aviationapi.chart_processor.app.providers.faa_tpp import FaaTppChartProvider

PROVIDERS = {FaaTppChartProvider.source: FaaTppChartProvider()}


def get_provider(source):
    return PROVIDERS.get(source)
