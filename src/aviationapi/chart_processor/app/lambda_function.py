import os
import pathlib
import shutil
import zipfile

import boto3
import boto3.s3.transfer as s3transfer
import requests
from botocore.config import Config
from pypdf import PdfReader, PdfWriter

import aviationapi.chart_processor.app.airport_codes as AirportCodes
import aviationapi.chart_processor.app.format_chart_db_data as ChartDataFormatter
import aviationapi.chart_processor.app.format_cs_db_data as ChartSupplementDataFormatter
import aviationapi.lib.messengers.trigger_chart_post_processor as TriggerChartPostProcessorMessenger
from aviationapi.lib.logger import logInfo
from aviationapi.lib.models.AiracData import CycleChartTypes

DOWNLOAD_PATH = (
    pathlib.Path(os.environ.get("DOWNLOAD_PATH", os.getcwd() + "/temp")) / "data"
)
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "aviationapi-charts")
UPLOAD_THREADS = int(os.environ.get("UPLOAD_THREADS", 2))
MONTHS = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}


def generate_file_name(packet, airac):
    if packet == "ChartSupplement":
        return f"DCS_20{airac}"

    if packet == "codes":
        year = airac[0:2]
        month = MONTHS[airac[2:4]]
        day = airac[4:6]

        return f"{day}_{month}_20{year}_APT_CSV"

    return f"DDTPP{packet}_{airac}"


def generate_download_url(file_name, packet):
    if packet == "codes":
        return f"https://nfdc.faa.gov/webContent/28DaySub/extra/{file_name}.zip"

    chart_type = "terminal"
    if packet == "ChartSupplement":
        chart_type = "supplements"

    return f"https://aeronav.faa.gov/upload_313-d/{chart_type}/{file_name}.zip"


def unzip_charts(download_path, file_name):
    charts_path = DOWNLOAD_PATH / file_name
    with zipfile.ZipFile(download_path, "r") as zip:
        zip.extractall(charts_path)

    return charts_path


def group_associated_charts(charts_path):
    chart_multiple_page_counts = {}

    for root, dir, files in os.walk(charts_path):
        for file in files:
            name_addition = ""
            if "_CMP" in file:
                file = file.replace("_CMP", "")
                name_addition = "_CMP"

            file = file.split("_C")[0]
            file = f"{root}/{file.split('.PDF')[0]}{name_addition}"

            if file in chart_multiple_page_counts:
                chart_multiple_page_counts[file] += 1
            else:
                chart_multiple_page_counts[file] = 1

    return chart_multiple_page_counts


def merge_files(merger, input_file, file_number):
    reader = PdfReader(input_file)
    num_pages = reader.get_num_pages()
    reader.close()

    for page_number in range(0, num_pages):
        insert_index = (file_number * (1 + page_number)) + page_number
        insert_range = (page_number, page_number + 1)

        merger.merge(position=insert_index, fileobj=input_file, pages=insert_range)


def combine_files(base_file_name, file_count):
    merger = PdfWriter()
    to_be_deleted = []
    for file_number in range(0, file_count):
        input_file = base_file_name
        name_addition = ""
        if "_CMP" in input_file:
            name_addition = "_CMP"
            input_file = input_file.replace("_CMP", "")

        if file_number == 0:
            input_file += f"{name_addition}.PDF"
        elif file_number == 1:
            input_file += f"_C{name_addition}.PDF"
            to_be_deleted.append(input_file)
        else:
            input_file += f"_C{str(file_number)}{name_addition}.PDF"
            to_be_deleted.append(input_file)

        merge_files(merger, input_file, file_number)

    merger.write(f"{base_file_name}.PDF")
    merger.close()

    for file in to_be_deleted:
        os.remove(file)


def combine_associated_charts(charts_path):
    logInfo("Combining associated charts")
    chart_multiple_page_counts = group_associated_charts(charts_path)

    for base_file_name, file_count in chart_multiple_page_counts.items():
        if file_count == 1:
            continue

        combine_files(base_file_name, file_count)

    logInfo("Finished combining charts")


def upload_file_s3(s3_client, path, bucket_name, object_name):
    s3_client.upload_file(path, bucket_name, object_name)


def push_charts_to_s3(airac, charts_path):
    logInfo("Pushing downloaded charts to S3")
    s3_config = Config(max_pool_connections=UPLOAD_THREADS)
    s3_client = boto3.client("s3", config=s3_config)
    s3_object_name = f"{airac}/"
    logInfo(f"s3_bucket: {S3_BUCKET_NAME}, s3_object_path: {s3_object_name}")

    transfer_config = s3transfer.TransferConfig(
        use_threads=True, max_concurrency=UPLOAD_THREADS
    )

    s3t = s3transfer.create_transfer_manager(s3_client, transfer_config)
    metadata = {"ContentType": "application/pdf", "ContentDisposition": "inline"}

    for root, dir, files in os.walk(charts_path):
        for file in files:
            _, file_ext = os.path.splitext(file)
            if file_ext.lower() != ".pdf":
                continue

            s3t.upload(
                os.path.join(root, file),
                S3_BUCKET_NAME,
                s3_object_name + file.lower(),
                extra_args=metadata,
            )

    s3t.shutdown()
    s3_client.close()

    logInfo("S3 upload complete")


def download_charts(packet, airac):
    logInfo("Downloading and processing chart packet")
    pathlib.Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)

    file_name = generate_file_name(packet, airac)
    zip_file_download_path = DOWNLOAD_PATH / f"{file_name}.zip"
    response = requests.get(generate_download_url(file_name, packet))
    zip_file_download_path.write_bytes(response.content)

    should_continue = True
    if response.status_code != 200:
        should_continue = False
        logInfo(
            "Error downloading charts. Could this possibly be trying to download the chart supplement on a 28 day cycle?"
        )

    return (zip_file_download_path, file_name, should_continue)


def insert_charts_to_dynamodb(airac, files_path):
    ChartDataFormatter.process_data(airac, files_path)

    logInfo("Inserting charts to DynamoDB")
    logInfo("Finished inserting charts to DynamoDB")


def download_and_unzip_charts(packet, airac):
    zip_file_download_path, file_name, should_continue = download_charts(packet, airac)
    charts_path = ""
    if should_continue:
        charts_path = unzip_charts(zip_file_download_path, file_name)

    return (charts_path, should_continue)


def process_standard_chart_packets(packet, airac):
    charts_path, success = download_and_unzip_charts(packet, airac)

    if success:
        combine_associated_charts(charts_path)
        push_charts_to_s3(airac, charts_path)

    return success


def process_chart_packet_with_db_and_changes(packet, airac):
    charts_path, success = download_and_unzip_charts(packet, airac)

    if success:
        insert_charts_to_dynamodb(airac, charts_path)
        charts_path /= "compare_pdf"
        combine_associated_charts(charts_path)
        push_charts_to_s3(airac, charts_path)

    return success


def process_airport_codes(airac):
    path, _ = download_and_unzip_charts("codes", airac)
    return AirportCodes.process_airport_codes(path)


def process_chart_supplement(packet, airac):
    airport_codes = process_airport_codes(airac)
    charts_path, success = download_and_unzip_charts(packet, airac)
    if success:
        ChartSupplementDataFormatter.insert_cs_to_dynamodb(
            airac, charts_path, airport_codes, MONTHS
        )
        push_charts_to_s3(airac, charts_path)

    return success


def lambda_handler(event, context):
    logInfo(f"Trigger received with event: {str(event)}")
    attributes = event["Records"][0]["Sns"]["MessageAttributes"]
    packet = attributes["packet"]["Value"]
    airac = attributes["airac"]["Value"]
    cycle_chart_type = CycleChartTypes.CHARTS.value

    logInfo(f"packet: {packet}, airac: {airac}")
    success = True

    match packet:
        case "A" | "B" | "C" | "D":
            success = process_standard_chart_packets(packet, airac)
        case "E":
            success = process_chart_packet_with_db_and_changes(packet, airac)
        case "ChartSupplement":
            success = process_chart_supplement(packet, airac)
            cycle_chart_type = CycleChartTypes.CHART_SUPPLEMENT.value
        case _:
            logError("Invalid packet specified")
            success = False

    if success:
        logInfo(
            f"Sending success message to post processor for {cycle_chart_type} packet {packet} airac {airac}"
        )
        TriggerChartPostProcessorMessenger.publish_success_message(
            airac, packet, cycle_chart_type
        )
    else:
        logInfo(
            f"Error processing {cycle_chart_type} packet {packet} airac {airac}. Success message not sent"
        )

    logInfo("Cleaning up drive")
    shutil.rmtree(DOWNLOAD_PATH)
