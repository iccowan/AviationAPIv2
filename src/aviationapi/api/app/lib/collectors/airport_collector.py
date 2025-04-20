import aviationapi.lib.repositories.airport_repository as AirportRepository
import aviationapi.lib.repositories.airac_data_repository as AiracDataRepository

def _get_airport(airport, chart_cycle_type, chart_type):
    airport_chart_type = "tpp"
    if chart_type == "chart_supplement":
        airport_chart_type = "cs"

    airac_data = AiracDataRepository.get_airac(chart_cycle_type, chart_type)
    if not airac_data.is_retrieveable:
        return {}

    charts = AirportRepository.get_airport(airport, airac_data.airac, airport_chart_type)

    return charts.dict()


def _get_charts_for_airport(airport, chart_type):
    return _get_airport(airport, chart_type, "charts")

def _get_chart_supplement_for_airport(airport, chart_type):
    return _get_airport(airport, chart_type, "chart_supplement")


def get_current_charts_for_airport(airport):
    return _get_charts_for_airport(airport, "current")

def get_next_charts_for_airport(airport):
    return _get_charts_for_airport(airport, "next")

def get_current_chart_supplement_for_airport(airport):
    return _get_chart_supplement_for_airport(airport, "current")

def get_next_chart_supplement_for_airport(airport):
    return _get_chart_supplement_for_airport(airport, "next")

