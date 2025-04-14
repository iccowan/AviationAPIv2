import os
import pathlib
import shutil
import zipfile

import boto3
import boto3.s3.transfer as s3transfer
import requests
from botocore.config import Config
from pypdf import PdfReader, PdfWriter

import app.format_chart_db_data as ChartDataFormatter
from app.lib.logger import logInfo

DOWNLOAD_PATH = (
    pathlib.Path(os.environ.get("DOWNLOAD_PATH", os.getcwd() + "/temp")) / "data"
)
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "aviationapi-charts")
UPLOAD_THREADS = int(os.environ.get("UPLOAD_THREADS", 2))


def generate_file_name(packet, airac):
    if packet == "chart_supplement":
        return f"DCS_20{airac}"

    return f"DDTPP{packet}_{airac}"


def generate_download_url(file_name, packet):
    chart_type = "terminal"
    if packet == "chart_supplement":
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
    s3_config = Config(
        s3={"use_accelerate_endpoint": True}, max_pool_connections=UPLOAD_THREADS
    )
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
            if file_ext != ".pdf":
                continue

            s3t.upload(
                os.path.join(root, file),
                S3_BUCKET_NAME,
                s3_object_name + file,
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
    zip_file_download_path.write_bytes(
        requests.get(generate_download_url(file_name, packet)).content
    )

    return (zip_file_download_path, file_name)


def insert_charts_to_dynamodb(airac, files_path):
    ChartDataFormatter.process_data(airac, files_path)

    logInfo("Inserting charts to DynamoDB")
    logInfo("Finished inserting charts to DynamoDB")


def download_chart_supplement(airac):
    logInfo("Downloading and processing chart supplement")
    logInfo(f"airac: {airac}")


def download_and_unzip_charts(packet, airac):
    zip_file_download_path, file_name = download_charts(packet, airac)
    charts_path = unzip_charts(zip_file_download_path, file_name)

    return charts_path

def process_standard_chart_packets(packet, airac):
    download_and_unzip_charts(packet, airac)
    combine_associated_charts(charts_path)
    push_charts_to_s3(airac, charts_path)


def process_chart_packet_with_db_and_changes(packet, airac):
    download_and_unzip_charts(packet, airac)
    insert_charts_to_dynamodb(airac, charts_path)
    charts_path /= "compare_pdf"
    combine_associated_charts(charts_path)
    push_charts_to_s3(airac, charts_path)


def process_chart_supplement(packet, airac):
    download_and_unzip_charts(packet, airac)
    insert_cs_to_dynamodb(airac, charts_path)
    push_charts_to_s3(airac, charts_path)


def lambda_handler(event, context):
    logInfo(f"Trigger received with event: {str(event)}")
    attributes = event["Records"][0]["Sns"]["MessageAttributes"]
    packet = attributes["packet"]["Value"]
    airac = attributes["airac"]["Value"]

    logInfo(f"packet: {packet}, airac: {airac}")

    match packet:
        case "A" | "B" | "C" | "D":
            process_standard_chart_packets(packet, airac)
        case "E":
            process_chart_packet_with_db_and_changes(packet, airac)
        case "ChartSupplement":
            process_chart_supplement(packet, airac)
        case _:
            logError("Invalid packet specified")
            return 1

    logInfo("Cleaning up drive")
    shutil.rmtree(DOWNLOAD_PATH)
