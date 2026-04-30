import aviationapi.lib.repositories.airac_data_repository as AiracDataRepository
import aviationapi.lib.repositories.airport_repository as AirportRepository
from aviationapi.chart_processor.app.providers.registry import get_providers
from aviationapi.lib.logger import logError


def _get_airport_chart_type(chart_type):
    airport_chart_type = "tpp"
    if chart_type == "chart_supplement":
        airport_chart_type = "cs"

    return airport_chart_type


def _get_airport_from_source(airport, chart_cycle_type, chart_type, source):
    airac_data = AiracDataRepository.get_airac(
        chart_cycle_type, chart_type, source=source
    )
    if airac_data is None or not airac_data.is_retrieveable:
        return None

    charts = AirportRepository.get_airport(
        airport,
        airac_data.airac,
        _get_airport_chart_type(chart_type),
        source=source,
    )
    if charts is None:
        return None

    return charts.dict()


def _get_airport(airport, chart_cycle_type, chart_type):
    source_matches = []
    for provider in get_providers():
        charts = _get_airport_from_source(
            airport, chart_cycle_type, chart_type, provider.source
        )
        if charts is None:
            continue

        source_matches.append({"source": provider.source, "charts": charts})

    if len(source_matches) == 0:
        return {}

    if len(source_matches) > 1:
        matched_sources = ", ".join([match["source"] for match in source_matches])
        logError(
            f"Airport {airport} matched multiple sources for {chart_type}: {matched_sources}"
        )

    return source_matches[0]["charts"]


def _get_charts_for_airport(airport, chart_type):
    return _get_airport(airport, chart_type, "charts")


def _get_chart_supplement_for_airport(airport, chart_type):
    return _get_airport(airport, chart_type, "chart_supplement")


def get_current_charts_for_airport(airport):
    return _get_charts_for_airport(airport, "current")


def get_current_charts_for_airport_list(airport_list):
    return [get_current_charts_for_airport(airport) for airport in airport_list]


def get_next_charts_for_airport(airport):
    return _get_charts_for_airport(airport, "next")


def get_next_charts_for_airport_list(airport_list):
    return [get_next_charts_for_airport(airport) for airport in airport_list]


def get_current_chart_supplement_for_airport(airport):
    return _get_chart_supplement_for_airport(airport, "current")


def get_current_chart_supplement_for_airport_list(airport_list):
    return [
        get_current_chart_supplement_for_airport(airport) for airport in airport_list
    ]


def get_next_chart_supplement_for_airport(airport):
    return _get_chart_supplement_for_airport(airport, "next")


def get_next_chart_supplement_for_airport_list(airport_list):
    return [get_next_chart_supplement_for_airport(airport) for airport in airport_list]
