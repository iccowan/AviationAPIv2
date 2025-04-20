import os
import xml.etree.ElementTree as ElementTree

import aviationapi.lib.repositories.airport_repository as AirportRepository
from aviationapi.lib.logger import logInfo
from aviationapi.lib.models.Airport import Airport
from aviationapi.lib.models.Chart import Chart, ChartType

CHART_BASE_URL = os.environ.get("CHART_BASE_URL", "")
START_EVENT = "start"
END_EVENT = "end"


def update_current_airport_tags(current_airport, event, element, tag, text):
    if event == START_EVENT and tag == "state_code":
        current_airport.airport_data.state_abbr = element.attrib["ID"]
        current_airport.airport_data.state_full = element.attrib["state_fullname"]
    if event == START_EVENT and tag == "city_name":
        current_airport.airport_data.city = element.attrib["ID"]
    if event == START_EVENT and tag == "airport_name":
        current_airport.airport_data.airport_name = element.attrib["ID"]
        current_airport.airport_data.faa_ident = element.attrib["apt_ident"]
        current_airport.airport_data.icao_ident = element.attrib["icao_ident"]
        current_airport.airport_data.is_military = element.attrib["military"] == "M"


def update_current_chart_tags(
    current_chart, current_chart_data, airac, event, tag, text
):
    if event == END_EVENT and tag == "chartseq":
        current_chart.chart_sequence = text
    if event == END_EVENT and tag == "chart_name":
        current_chart.chart_name = text
    if event == END_EVENT and tag == "pdf_name":
        if "_C" in text or "DELETED_JOB.PDF" in text or "DEL_APT_SERVED.PDF" in text:
            current_chart_data["skip_chart"] = True

        current_chart.pdf_name = text.lower()
        current_chart.pdf_url = f"{CHART_BASE_URL}/{airac}/{text.lower()}"
    if event == END_EVENT and tag == "useraction":
        current_chart_data["chart_change"] = text == "C"
    if event == END_EVENT and tag == "chart_code":
        match text:
            case "APD":
                current_chart_data["current_chart_section"] = (
                    ChartType.AIRPORT_DIAGRAM.value
                )
            case "DP" | "DAU":
                current_chart_data["current_chart_section"] = ChartType.DEPARTURE.value
            case "STAR":
                current_chart_data["current_chart_section"] = ChartType.ARRIVAL.value
            case "IAP" | "CVFP":
                current_chart_data["current_chart_section"] = ChartType.APPROACH.value
            case _:
                current_chart_data["current_chart_section"] = ChartType.GENERAL.value


def insert_chart_to_airport(current_airport, current_chart, current_chart_data):
    if current_chart_data["chart_change"]:
        current_chart.did_change = True
        current_chart.change_pdf_name = (
            current_chart.pdf_name[:-4] + "_cmp" + current_chart.pdf_name[-4:]
        )
        current_chart.change_pdf_url = (
            current_chart.pdf_url[:-4] + "_cmp" + current_chart.pdf_url[-4:]
        )

    if not current_chart_data["skip_chart"]:
        current_airport.charts[current_chart_data["current_chart_section"]].append(
            current_chart
        )


def process_xml_db(xml_document, airac):
    airports = 0

    current_airport = Airport(airac)
    current_chart = Chart()
    current_chart_data = {
        "current_chart_section": "",
        "skip_chart": False,
        "chart_change": False,
    }

    for event, element in xml_document:
        tag = element.tag.strip()
        text = element.text.strip() if element.text is not None else ""

        update_current_airport_tags(current_airport, event, element, tag, text)
        update_current_chart_tags(
            current_chart, current_chart_data, airac, event, tag, text
        )

        if event == END_EVENT and tag == "record":
            insert_chart_to_airport(current_airport, current_chart, current_chart_data)

            current_chart_data["skip_chart"] = False
            current_chart_data["chart_change"] = False
            current_chart = Chart()

        if event == END_EVENT and tag == "airport_name":
            AirportRepository.put_airport(current_airport)

            airports += 1
            current_airport.reset_for_next_airport()

    return airports


def process_data(airac, files_path):
    logInfo("Beginning to process airport chart data for DynamoDB")
    try:
        file = open(files_path / "d-TPP_Metafile.xml")
    except FileNotFoundError:
        logError(f"No airport DB file d-TPP_Metafile.xml found in {files_path}")
    else:
        xml_document = ElementTree.iterparse(file, [START_EVENT, END_EVENT])
        airports = process_xml_db(xml_document, airac)

        logInfo(f"Finished processing data for {str(airports)} airports")
    finally:
        file.close()
