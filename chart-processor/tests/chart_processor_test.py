import pathlib
from app.chart_processor import lambda_handler
from unittest.mock import patch

@patch('app.chart_processor.download_charts')
@patch('app.chart_processor.unzip_charts')
@patch('app.chart_processor.combine_associated_charts')
@patch('app.chart_processor.push_charts_to_s3')
@patch('shutil.rmtree')
def test_lambda_handler_calls_download_charts_when_packet_a(shutil_rmtree, push_charts_to_s3, combine_associated_charts, unzip_charts, download_charts):
    packet = 'A'
    airac = '250417'
    
    unzip_charts.return_value = pathlib.Path('')
    download_charts.return_value = ('', '')

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    download_charts.assert_called_once_with(packet, airac)

@patch('app.chart_processor.download_charts')
@patch('app.chart_processor.unzip_charts')
@patch('app.chart_processor.combine_associated_charts')
@patch('app.chart_processor.push_charts_to_s3')
@patch('shutil.rmtree')
def test_lambda_handler_calls_download_charts_when_packet_b(shutil_rmtree, push_charts_to_s3, combine_associated_charts, unzip_charts, download_charts):
    packet = 'B'
    airac = '250417'
    
    unzip_charts.return_value = pathlib.Path('')
    download_charts.return_value = ('', '')

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    download_charts.assert_called_once_with(packet, airac)

@patch('app.chart_processor.download_charts')
@patch('app.chart_processor.unzip_charts')
@patch('app.chart_processor.combine_associated_charts')
@patch('app.chart_processor.push_charts_to_s3')
@patch('shutil.rmtree')
def test_lambda_handler_calls_download_charts_when_packet_c(shutil_rmtree, push_charts_to_s3, combine_associated_charts, unzip_charts, download_charts):
    packet = 'C'
    airac = '250417'
    
    unzip_charts.return_value = pathlib.Path('')
    download_charts.return_value = ('', '')

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    download_charts.assert_called_once_with(packet, airac)

@patch('app.chart_processor.download_charts')
@patch('app.chart_processor.unzip_charts')
@patch('app.chart_processor.combine_associated_charts')
@patch('app.chart_processor.push_charts_to_s3')
@patch('shutil.rmtree')
def test_lambda_handler_calls_download_charts_when_packet_d(shutil_rmtree, push_charts_to_s3, combine_associated_charts, unzip_charts, download_charts):
    packet = 'D'
    airac = '250417'
    
    unzip_charts.return_value = pathlib.Path('')
    download_charts.return_value = ('', '')

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    download_charts.assert_called_once_with(packet, airac)

@patch('app.chart_processor.download_charts')
@patch('app.chart_processor.unzip_charts')
@patch('app.chart_processor.insert_charts_to_dynamodb')
@patch('app.chart_processor.combine_associated_charts')
@patch('app.chart_processor.push_charts_to_s3')
@patch('shutil.rmtree')
def test_lambda_handler_calls_download_charts_when_packet_e(shutil_rmtree, push_charts_to_s3, combine_associated_charts, insert_charts_to_dynamodb, unzip_charts, download_charts):
    packet = 'E'
    airac = '250417'
    
    unzip_charts.return_value = pathlib.Path('')
    download_charts.return_value = ('', '')

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    download_charts.assert_called_once_with(packet, airac)

def generate_handler_event(packet, airac):
    return {
        'Records': [
            {
                'Sns': {
                    'MessageAttributes': {
                        'packet': {
                            'Type': 'S',
                            'Value': packet
                        },
                        'airac': {
                            'Type': 'S',
                            'Value': airac
                        }
                    }
                }
            }
        ]
    }

