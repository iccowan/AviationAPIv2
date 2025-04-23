import os
import random
from importlib import reload
from unittest.mock import patch

from aviationapi.chart_processor.app.lambda_function import lambda_handler


@patch("aviationapi.chart_processor.app.lambda_function.process_standard_chart_packets")
@patch(
    "aviationapi.lib.messengers.trigger_chart_post_processor.publish_success_message"
)
@patch("shutil.rmtree")
def test_lambda_handler_calls_process_standard_chart_packets_when_packet_abcd(
    shutil_rmtree, publish_success_message, process_standard_chart_packets
):
    packet = random.choice(["A", "B", "C", "D"])
    airac = "250417"

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    process_standard_chart_packets.assert_called_once_with(packet, airac)


"""
@patch("aviationapi.chart_processor.app.lambda_function.process_chart_packet_with_db_and_changes")
@patch("shutil.rmtree")
def test_lambda_handler_calls_process_chart_packet_with_db_and_changes_when_packet_e(
    shutil_rmtree, process_chart_packet_with_db_and_changes
):
    packet = "E"
    airac = "250417"

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    process_chart_packet_with_db_and_changes.assert_called_once_with(packet, airac)


@patch("aviationapi.chart_processor.app.lambda_function.process_chart_supplement")
@patch("shutil.rmtree")
def test_lambda_handler_calls_process_chart_supplement_when_packet_chart_supplement(
    shutil_rmtree, process_chart_supplement
):
    packet = "ChartSupplement"
    airac = "250417"

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    process_chart_supplement.assert_called_once_with(airac)


@patch("aviationapi.chart_processor.app.lambda_function.process_standard_chart_packets")
@patch("aviationapi.chart_processor.app.lambda_function.process_chart_packet_with_db_and_changes")
@patch("aviationapi.chart_processor.app.lambda_function.process_chart_supplement")
@patch("shutil.rmtree")
def test_lambda_handler_calls_shutil_remove_tree(
    shutil_rmtree,
    process_chart_supplement,
    process_chart_packet_with_db_and_changes,
    process_standard_chart_packets,
):
    download_path = "/tmp/test"
    set_env({"DOWNLOAD_PATH": download_path})

    packet = "ChartSupplement"
    airac = "250417"

    event = generate_handler_event(packet, airac)
    context = {}
    lambda_handler(event, context)

    shutil_rmtree.assert_called_once_with(pathlib.Path(download_path) / "data")


@patch("aviationapi.chart_processor.app.lambda_function.download_charts")
@patch("aviationapi.chart_processor.app.lambda_function.unzip_charts")
@patch("aviationapi.chart_processor.app.lambda_function.combine_associated_charts")
@patch("aviationapi.chart_processor.app.lambda_function.push_charts_to_s3")
def test_process_standard_chart_packets_calls_download_charts(
    push_charts_to_s3, combine_associated_charts, unzip_charts, download_charts
):
    packet = random.choice(["A", "B", "C", "D"])
    airac = "250417"
    zip_file_download_path = "/some/download/path"
    file_name = "some_file_name.zip"

    download_charts.return_value = (zip_file_download_path, file_name)

    process_standard_chart_packets(packet, airac)

    download_charts.assert_called_once_with(packet, airac)


@patch("aviationapi.chart_processor.app.lambda_function.download_charts")
@patch("aviationapi.chart_processor.app.lambda_function.unzip_charts")
@patch("aviationapi.chart_processor.app.lambda_function.combine_associated_charts")
@patch("aviationapi.chart_processor.app.lambda_function.push_charts_to_s3")
def test_process_standard_chart_packets_calls_unzip_charts(
    push_charts_to_s3, combine_associated_charts, unzip_charts, download_charts
):
    packet = random.choice(["A", "B", "C", "D"])
    airac = "250417"
    zip_file_download_path = "/some/download/path"
    file_name = "some_file_name.zip"
    charts_path = "/some/other/download/path"

    download_charts.return_value = (zip_file_download_path, file_name)
    unzip_charts.return_value = charts_path

    process_standard_chart_packets(packet, airac)

    unzip_charts.assert_called_once_with(zip_file_download_path, file_name)


@patch("aviationapi.chart_processor.app.lambda_function.download_charts")
@patch("aviationapi.chart_processor.app.lambda_function.unzip_charts")
@patch("aviationapi.chart_processor.app.lambda_function.combine_associated_charts")
@patch("aviationapi.chart_processor.app.lambda_function.push_charts_to_s3")
def test_process_standard_chart_packets_calls_combine_associated_charts(
    push_charts_to_s3, combine_associated_charts, unzip_charts, download_charts
):
    packet = random.choice(["A", "B", "C", "D"])
    airac = "250417"
    zip_file_download_path = "/some/download/path"
    file_name = "some_file_name.zip"
    charts_path = "/some/other/download/path"

    download_charts.return_value = (zip_file_download_path, file_name)
    unzip_charts.return_value = charts_path

    process_standard_chart_packets(packet, airac)

    combine_associated_charts.assert_called_once_with(charts_path)


@patch("aviationapi.chart_processor.app.lambda_function.download_charts")
@patch("aviationapi.chart_processor.app.lambda_function.unzip_charts")
@patch("aviationapi.chart_processor.app.lambda_function.combine_associated_charts")
@patch("aviationapi.chart_processor.app.lambda_function.push_charts_to_s3")
def test_process_standard_chart_packets_calls_push_charts_to_s3(
    push_charts_to_s3, combine_associated_charts, unzip_charts, download_charts
):
    packet = random.choice(["A", "B", "C", "D"])
    airac = "250417"
    zip_file_download_path = "/some/download/path"
    file_name = "some_file_name.zip"
    charts_path = "/some/other/download/path"

    download_charts.return_value = (zip_file_download_path, file_name)
    unzip_charts.return_value = charts_path

    process_standard_chart_packets(packet, airac)

    push_charts_to_s3.assert_called_once_with(airac, charts_path)

"""


def set_env(env):
    os.environ = env
    reload(app.chart_processor)


def generate_handler_event(packet, airac):
    return {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "packet": {"Type": "S", "Value": packet},
                        "airac": {"Type": "S", "Value": airac},
                    }
                }
            }
        ]
    }
