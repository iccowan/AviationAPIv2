import shutil

import aviationapi.lib.messengers.trigger_chart_post_processor as TriggerChartPostProcessorMessenger
from aviationapi.chart_processor.app.providers.faa_tpp import DOWNLOAD_PATH
from aviationapi.chart_processor.app.providers.registry import get_provider
from aviationapi.lib.chart_provider_keys import DEFAULT_CHART_PROVIDER
from aviationapi.lib.logger import logError, logInfo


def lambda_handler(event, context):
    logInfo(f"Trigger received with event: {str(event)}")
    attributes = event["Records"][0]["Sns"]["MessageAttributes"]
    packet = attributes["packet"]["Value"]
    airac = attributes["airac"]["Value"]
    provider = attributes.get("provider", {}).get("Value", DEFAULT_CHART_PROVIDER)

    chart_provider = get_provider(provider)
    if chart_provider is None:
        logError(f"No chart provider registered for provider {provider}")
        return 1

    logInfo(f"provider: {provider}, packet: {packet}, airac: {airac}")
    process_result = chart_provider.process_packet(packet, airac)
    success = process_result["success"]
    cycle_chart_type = process_result["cycle_chart_type"]

    if success:
        logInfo(
            f"Sending success message to post processor for provider {provider} "
            f"{cycle_chart_type} packet {packet} airac {airac}"
        )
        TriggerChartPostProcessorMessenger.publish_success_message(
            airac, packet, cycle_chart_type, provider
        )
    else:
        logInfo(
            f"Error processing provider {provider} {cycle_chart_type} packet {packet} "
            f"airac {airac}. Success message not sent"
        )

    logInfo("Cleaning up drive")
    shutil.rmtree(DOWNLOAD_PATH)
