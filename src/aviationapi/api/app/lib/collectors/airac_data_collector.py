import aviationapi.lib.repositories.airac_data_repository as AiracDataRepository
from aviationapi.chart_processor.app.providers.registry import get_providers


def _get_availability(cycle_chart_type):
    availability = []
    for provider in get_providers():
        airac_data = AiracDataRepository.get_all_airac(
            cycle_chart_type, source=provider.source
        )
        if airac_data is None:
            continue

        if type(airac_data) is not list:
            availability.append(airac_data.api_dict())
            continue

        availability.extend([airac.api_dict() for airac in airac_data])

    if len(availability) == 0:
        return None

    availability.sort(key=lambda airac: (airac["source"], airac["cycle_chart_type"]))

    if len(availability) == 1:
        return availability[0]

    return availability


def get_next_availability():
    return _get_availability("next")


def get_current_availability():
    return _get_availability("current")
