import boto3
import os
import requests
import pathlib
import threading
import shutil
import zipfile
import boto3.s3.transfer as s3transfer
from botocore.config import Config
from pypdf import PdfWriter

from app.lib.logger import logInfo

DOWNLOAD_PATH = pathlib.Path(os.environ.get('DOWNLOAD_PATH', os.getcwd() + '/temp')) / 'data'
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'aviationapi-charts')
UPLOAD_THREADS = int(os.environ.get('UPLOAD_THREADS', 2))

def generate_file_name(packet, airac):
    return 'DDTPP' + packet + '_' + airac

def generate_download_url(file_name):
    return f'https://aeronav.faa.gov/upload_313-d/terminal/{file_name}.zip'

def unzip_charts(download_path, file_name):
    charts_path = DOWNLOAD_PATH / file_name
    with zipfile.ZipFile(download_path, 'r') as zip:
        zip.extractall(charts_path)

    return charts_path

def combine_associated_charts(charts_path):
    logInfo('Combining associated charts')
    chart_multiple_page_counts = {}

    for root, dir, files in os.walk(charts_path):
        for file in files:
            file = file.split('_C')[0]
            file = f'{root}/{file.split('.')[0]}'

            if file in chart_multiple_page_counts:
                chart_multiple_page_counts[file] += 1
            else:
                chart_multiple_page_counts[file] = 1

    for file_name, pages in chart_multiple_page_counts.items():
        if pages == 1:
            continue
        
        merger = PdfWriter()
        to_be_deleted = []
        for page_number in range(0, pages):
            input_file = file_name
            if page_number == 0:
                input_file += '.PDF'
            elif page_number == 1:
                input_file += '_C.PDF'
                to_be_deleted.append(input_file)
            else:
                input_file += f'_C{str(page_number)}.PDF'
                to_be_deleted.append(input_file)

            merger.append(input_file)
        
        merger.write(f'{file_name}.PDF')
        merger.close()

        for file in to_be_deleted:
            os.remove(file)

    logInfo('Finished combining charts')

def upload_file_s3(s3_client, path, bucket_name, object_name):
    s3_client.upload_file(path, bucket_name, object_name)

def push_charts_to_s3(packet, airac, charts_path):
    logInfo('Pushing downloaded charts to S3')
    s3_config = Config(s3 = {"use_accelerate_endpoint": True}, max_pool_connections = UPLOAD_THREADS)
    s3_client = boto3.client('s3', config=s3_config)
    s3_object_name = f'{airac}/'
    logInfo(f's3_bucket: {S3_BUCKET_NAME}, s3_object_path: {s3_object_name}')
    
    transfer_config = s3transfer.TransferConfig(
        use_threads=True,
        max_concurrency=UPLOAD_THREADS
    )

    s3t = s3transfer.create_transfer_manager(s3_client, transfer_config)
    metadata = {
        'ContentType': 'application/pdf',
        'ContentDisposition': 'inline'
    }

    for root, dir, files in os.walk(charts_path):
        for file in files:
            s3t.upload(os.path.join(root, file), S3_BUCKET_NAME, s3_object_name + file, extra_args=metadata)

    s3t.shutdown()

    logInfo('S3 upload complete')

def download_charts(packet, airac):
    logInfo('Downloading and processing chart packet')
    pathlib.Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)

    file_name = generate_file_name(packet, airac)
    zip_file_download_path = DOWNLOAD_PATH / f'{file_name}.zip'
    zip_file_download_path.write_bytes(requests.get(generate_download_url(file_name)).content)

    return (zip_file_download_path, file_name)

def insert_charts_to_dynamodb(airac, files_path):
    logInfo('Inserting charts to DynamoDB')
    logInfo('Finished inserting charts to DynamoDB')

def download_chart_supplement(airac):
    logInfo('Downloading and processing chart supplement')
    logInfo(f'airac: {airac}')

def lambda_handler(event, context):
    logInfo(f'Trigger received with event: {str(event)}')
    attributes = event['Records'][0]['Sns']['MessageAttributes']
    packet = attributes['packet']['Value']
    airac = attributes['airac']['Value']

    logInfo(f'packet: {packet}, airac: {airac}')

    match packet:
        case 'A' | 'B' | 'C' | 'D':
            zip_file_download_path, file_name = download_charts(packet, airac)
            charts_path = unzip_charts(zip_file_download_path, file_name)
            combine_associated_charts(charts_path)
            push_charts_to_s3(packet, airac, charts_path)
        case 'E':
            zip_file_download_path, file_name = download_charts(packet, airac)
            insert_charts_dynamodb(airac, unzip_charts(zip_file_download_path, file_name))
        case 'ChartSupplement':
            download_chart_supplement(airac)
        case _:
            logError('Invalid packet specified')
            return 1

    logInfo('Cleaning up drive')
    shutil.rmtree(DOWNLOAD_PATH)
    
