from datetime import datetime, timedelta

import aviationapi.lib.messengers.trigger_chart_processor as TriggerChartProcessorMessenger
import aviationapi.lib.repositories.airac_data_repository as AiracDataRepository
from aviationapi.lib.logger import logInfo
from aviationapi.lib.models.AiracData import AiracData, CycleChartTypes, CycleTypes

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
    next_airac_has_cs = True

    while next_charts_airac < TODAY:
        current_charts_airac = next_charts_airac
        next_charts_airac += timedelta(days=28)
        next_airac_has_cs = not next_airac_has_cs

    current_cs_airac = current_charts_airac
    next_cs_airac = current_charts_airac + timedelta(days=56)
    if next_airac_has_cs:
        current_cs_airac = next_charts_airac - timedelta(days=56)
        next_cs_airac = next_charts_airac

    return {
        "current_charts_airac": current_charts_airac,
        "next_charts_airac": next_charts_airac,
        "current_supplement_airac": current_cs_airac,
        "next_supplement_airac": next_cs_airac,
    }


def get_current_airacs():
    logInfo("Pulling airac data from DynamoDB")

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
        logInfo("Bad airac data found from DynamoDB. Creating new airac data")

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
        "next_supplement_airac": next_supplement_airac,
    }


def update_airac(current_airacs, chart_type):
    current_key = "current_charts_airac"
    next_key = "next_charts_airac"
    cycle_days = 28

    if chart_type == CycleChartTypes.CHART_SUPPLEMENT.value:
        current_key = "current_supplement_airac"
        next_key = "next_supplement_airac"
        cycle_days = 56

    if (
        current_airacs[next_key].valid_date <= TODAY
        and current_airacs[next_key].is_retrieveable
    ):
        logInfo(
            f"Update detected for {chart_type}. Old airac {current_airacs[current_key].airac}, new airac {current_airacs[next_key].airac}"
        )

        AiracDataRepository.delete_airac(current_airacs[current_key])

        current_airacs[current_key] = current_airacs[next_key]
        current_airacs[current_key].cycle_type = CycleTypes.CURRENT.value
        next_valid_date = current_airacs[current_key].valid_date + timedelta(
            days=cycle_days
        )

        current_airacs[next_key] = AiracData(
            date_to_airac(next_valid_date),
            CycleTypes.NEXT.value,
            chart_type,
            next_valid_date,
        )

        AiracDataRepository.put_airac(current_airacs[current_key])
        AiracDataRepository.put_airac(current_airacs[next_key])


def update_airacs(current_airacs):
    logInfo("Updating airacs")

    update_airac(current_airacs, CycleChartTypes.CHARTS.value)
    update_airac(current_airacs, CycleChartTypes.CHART_SUPPLEMENT.value)


def trigger_airac_updates(current_airacs):
    logInfo("Triggering packets requiring processing")

    for _, airac_data in current_airacs.items():
        if (
            TODAY + timedelta(days=14) >= airac_data.valid_date
            and not airac_data.is_retrieveable
        ):
            logInfo(f"Triggering processor for airac {airac_data.airac}")
            TriggerChartProcessorMessenger.publish_update_messages_for_airac(airac_data)


def lambda_handler(event, context):
    current_airacs = get_current_airacs()
    update_airacs(current_airacs)
    trigger_airac_updates(current_airacs)
