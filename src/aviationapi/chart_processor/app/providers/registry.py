from aviationapi.chart_processor.app.providers.faa_tpp import FaaTppChartProvider

PROVIDERS = {FaaTppChartProvider.provider: FaaTppChartProvider()}


def get_provider(provider):
    return PROVIDERS.get(provider)


def get_providers():
    return list(PROVIDERS.values())


def get_expected_jobs(provider_name, cycle_chart_type):
    provider = get_provider(provider_name)
    if provider is None:
        raise ValueError(f"No chart provider registered for provider {provider_name}")

    return provider.get_expected_jobs(cycle_chart_type)
