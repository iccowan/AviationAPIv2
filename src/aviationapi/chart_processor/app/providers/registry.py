from aviationapi.chart_processor.app.providers.faa_tpp import FaaTppChartProvider

PROVIDERS = {FaaTppChartProvider.provider: FaaTppChartProvider()}


def get_provider(provider):
    return PROVIDERS.get(provider)
