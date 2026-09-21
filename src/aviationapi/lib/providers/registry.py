from dataclasses import dataclass

from aviationapi.lib.chart_provider_keys import DEFAULT_CHART_PROVIDER
from aviationapi.lib.models.AiracData import CycleChartTypes


@dataclass(frozen=True)
class Provider:
    provider: str
    chart_jobs: tuple[str, ...]
    chart_supplement_jobs: tuple[str, ...]

    def get_expected_jobs(self, cycle_chart_type):
        if cycle_chart_type == CycleChartTypes.CHART_SUPPLEMENT.value:
            return list(self.chart_supplement_jobs)

        return list(self.chart_jobs)


PROVIDERS = {
    DEFAULT_CHART_PROVIDER: Provider(
        provider=DEFAULT_CHART_PROVIDER,
        chart_jobs=("A", "B", "C", "D", "E"),
        chart_supplement_jobs=("ChartSupplement",),
    )
}


def get_providers():
    return list(PROVIDERS.values())


def get_expected_jobs(provider_name, cycle_chart_type):
    provider = PROVIDERS.get(provider_name)
    if provider is None:
        raise ValueError(f"No chart provider registered for provider {provider_name}")

    return provider.get_expected_jobs(cycle_chart_type)
