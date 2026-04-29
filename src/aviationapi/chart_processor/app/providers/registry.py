from aviationapi.chart_processor.app.providers.faa_tpp import FaaTppChartProvider

PROVIDERS = {FaaTppChartProvider.source: FaaTppChartProvider()}


def get_provider(source):
    return PROVIDERS.get(source)


def get_providers():
    return list(PROVIDERS.values())


def get_expected_jobs(source, cycle_chart_type):
    provider = get_provider(source)
    if provider is None:
        raise ValueError(f"No chart provider registered for source {source}")

    return provider.get_expected_jobs(cycle_chart_type)
