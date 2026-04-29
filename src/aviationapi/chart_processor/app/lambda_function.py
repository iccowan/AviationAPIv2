import shutil

from aviationapi.chart_processor.app.providers.faa_tpp import DOWNLOAD_PATH
from aviationapi.chart_processor.app.providers.registry import get_provider
from aviationapi.lib.chart_data_keys import DEFAULT_CHART_SOURCE
import aviationapi.lib.messengers.trigger_chart_post_processor as TriggerChartPostProcessorMessenger
from aviationapi.lib.logger import logError, logInfo


def lambda_handler(event, context):
    logInfo(f"Trigger received with event: {str(event)}")
    attributes = event["Records"][0]["Sns"]["MessageAttributes"]
    packet = attributes["packet"]["Value"]
    airac = attributes["airac"]["Value"]
    source = attributes.get("source", {}).get("Value", DEFAULT_CHART_SOURCE)

    provider = get_provider(source)
    if provider is None:
        logError(f"No chart provider registered for source {source}")
        return 1

    logInfo(f"source: {source}, packet: {packet}, airac: {airac}")
    process_result = provider.process_packet(packet, airac)
    success = process_result["success"]
    cycle_chart_type = process_result["cycle_chart_type"]

    if success:
        logInfo(
            f"Sending success message to post processor for source {source} "
            f"{cycle_chart_type} packet {packet} airac {airac}"
        )
        TriggerChartPostProcessorMessenger.publish_success_message(
            airac, packet, cycle_chart_type, source
        )
    else:
        logInfo(
            f"Error processing source {source} {cycle_chart_type} packet {packet} "
            f"airac {airac}. Success message not sent"
        )

    logInfo("Cleaning up drive")
    shutil.rmtree(DOWNLOAD_PATH)
