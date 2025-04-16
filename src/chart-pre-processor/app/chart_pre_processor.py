from datetime import datetime, timedelta

import app.lib.repositories.airac_data_repository as AiracDataRepository
from app.lib.models.AiracData import AiracData, CycleChartTypes, CycleTypes

AIRAC_DATE_FORMAT = "%y%m%d"
TODAY = datetime.today()
BASE_AIRAC_WITH_CS = "250220"


def airac_to_date(airac):
    return datetime.strptime(airac, AIRAC_DATE_FORMAT)


def date_to_airac(date_time):
    return date_time.strftime(AIRAC_DATE_FORMAT)


def deduce_current_next_airac():
    current_charts_airac = None
    next_charts_airac = airac_to_date(BASE_AIRAC_WITH_CS)
    next_airac_has_cs = False

    while next_charts_airac < TODAY:
        current_charts_airac = next_charts_airac
        next_charts_airac += timedelta(days=28)
        next_airac_has_cs = not next_airac_has_cs

    current_cs_airac = current_charts_airac
    next_cs_airac = current_charts_airac + timedelta(days=56)
    if next_airac_has_cs:
        current_cs_airac -= timedelta(days=28)
        next_cs_airac -= timedelta(days=28)

    return {
        "current_charts_airac": current_charts_airac,
        "next_charts_airac": next_charts_airac,
        "current_supplement_airac": current_cs_airac,
        "next_supplement_airac": next_cs_airac,
    }

def get_current_airacs():
    current_charts_airac = AiracDataRepository.get_airac(
        CycleTypes.CURRENT.value, CycleChartTypes.CHARTS.value
    )
    next_charts_airac = AiracDataRepository.get_airac(
        CycleTypes.NEXT.value, CycleChartTypes.CHARTS.value
    )
    current_supplement_airac = AiracDataRepository.get_airac(
        CycleTypes.CURRENT.value, CycleChartTypes.CHART_SUPPLEMENT.value
    )
    next_supplement_airac = AiracDataRepository.get_airac(
        CycleTypes.NEXT.value, CycleChartTypes.CHART_SUPPLEMENT.value
    )

    if (
        current_charts_airac is None
        or next_charts_airac is None
        or current_supplement_airac is None
        or next_supplement_airac is None
    ):
        current_airacs = deduce_current_next_airac()

        current_charts_airac = AiracData(
            date_to_airac(current_airacs["current_charts_airac"]),
            CycleTypes.CURRENT.value,
            CycleChartTypes.CHARTS.value,
            current_airacs["current_charts_airac"],
        )
        next_charts_airac = AiracData(
            date_to_airac(current_airacs["next_charts_airac"]),
            CycleTypes.NEXT.value,
            CycleChartTypes.CHARTS.value,
            current_airacs["next_charts_airac"],
        )
        current_supplement_airac = AiracData(
            date_to_airac(current_airacs["current_supplement_airac"]),
            CycleTypes.CURRENT.value,
            CycleChartTypes.CHART_SUPPLEMENT.value,
            current_airacs["current_supplement_airac"],
        )
        next_supplement_airac = AiracData(
            date_to_airac(current_airacs["next_supplement_airac"]),
            CycleTypes.NEXT.value,
            CycleChartTypes.CHART_SUPPLEMENT.value,
            current_airacs["next_supplement_airac"],
        )

        AiracDataRepository.put_airac(current_charts_airac)
        AiracDataRepository.put_airac(next_charts_airac)
        AiracDataRepository.put_airac(current_supplement_airac)
        AiracDataRepository.put_airac(next_supplement_airac)

    return {
        "current_charts_airac": current_charts_airac,
        "next_charts_airac": next_charts_airac,
        "current_supplement_airac": current_supplement_airac,
        "next_supplement_airac": next_supplement_airac
    }

def update_airacs(current_airacs):
    if current_airacs["next_charts_airac"].valid_date >= TODAY:
        AiracDataRepository.delete_airac(current_airacs["current_charts_airac"])

        current_airacs["current_charts_airac"] = current_airacs["next_charrts_airac"]
        current_airacs["current_charts_airac"].cycle_type = CycleTypes.CURRENT.value
        next_airac_string = current_airacs["current_charts_airac"].valid_date + timedelta(days=28)

        current_airacs["next_charts_airac"] = AiracData(next_airac_string, CycleTypes.NEXT.value, CycleChartTypes.CHARTS.value, airac_to_date(next_airac_string))

        AiracDataRepository.put_airac(current_airacs["next_charts_airac"])


def lambda_handler(event, context):
    current_airacs = get_current_airacs()
    update_airacs(current_airacs)
    trigger_airac_updates(current_airacs)


lambda_handler(None, None)
