import aviationapi.lib.repositories.airac_data_repository as AiracDataRepository
from aviationapi.lib.chart_data_keys import DEFAULT_CHART_SOURCE
from aviationapi.lib.logger import logError, logInfo


def get_airac_data(airac, cycle_chart_type, source=DEFAULT_CHART_SOURCE):
    return AiracDataRepository.get_airac_by_cycle_chart_type_and_airac(
        airac, cycle_chart_type, source=source
    )


def update_airac_data(airac_data, packet):
    airac_data.is_packet_processed[packet] = True
    is_retrieveable = True

    for _, is_packet_processed in airac_data.is_packet_processed.items():
        is_retrieveable = is_retrieveable and is_packet_processed

    airac_data.is_retrieveable = is_retrieveable

    AiracDataRepository.put_airac(airac_data)


def lambda_handler(event, context):
    logInfo(f"Trigger received with event: {str(event)}")
    attributes = event["Records"][0]["Sns"]["MessageAttributes"]
    packet = attributes["packet"]["Value"]
    airac = attributes["airac"]["Value"]
    cycle_chart_type = attributes["cycle_chart_type"]["Value"]
    source = attributes.get("source", {}).get("Value", DEFAULT_CHART_SOURCE)

    airac_data = get_airac_data(airac, cycle_chart_type, source)

    if airac_data is None:
        logError(
            f"No {cycle_chart_type} airac data found for source {source} airac {airac}"
        )
        return 1

    logInfo(
        f"Processing successful processing of packet {packet} "
        f"for source {source} airac {airac} {cycle_chart_type}"
    )
    update_airac_data(airac_data, packet)
    logInfo(
        f"Successfully saved processed status for packet {packet} "
        f"for source {source} airac {airac} {cycle_chart_type}"
    )
