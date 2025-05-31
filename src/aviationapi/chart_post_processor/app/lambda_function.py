import aviationapi.lib.repositories.airac_data_repository as AiracDataRepository
from aviationapi.lib.logger import logInfo


def get_airac_data(airac, cycle_chart_type):
    return AiracDataRepository.get_airac_by_cycle_chart_type_and_airac(
        airac, cycle_chart_type
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

    airac_data = get_airac_data(airac, cycle_chart_type)

    if airac_data is None:
        logError(f"No {cycle_chart_type} airac data found for airac {airac}")
        return 1

    logInfo(
        f"Processing successful processing of packet {packet} for airac {airac} {cycle_chart_type}"
    )
    update_airac_data(airac_data, packet)
    logInfo(
        f"Successfully saved processed status for packet {packet} for airac {airac} {cycle_chart_type}"
    )
