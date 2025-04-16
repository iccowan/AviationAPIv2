import os
import xml.etree.ElementTree as ElementTree

import app.lib.repositories.airport_repository as AirportRepository
from app.lib.logger import logInfo
from app.lib.models.AirportChartSupplement import AirportChartSupplement

CHART_BASE_URL = os.environ.get("CHART_BASE_URL", "")
START_EVENT = "start"
END_EVENT = "end"


def update_current_tags(
    current_airport, airport_data, airport_codes, airac, event, element, tag, text
):
    if event == END_EVENT and tag == "aptid":
        if text == "":
            airport_data["skip"] = True

        current_airport.airport_data.faa_ident = text
        if text in airport_codes:
            current_airport.airport_data.icao_ident = airport_codes[text]

    if event == END_EVENT and tag == "pdf":
        current_airport.charts.append(
            {
                "pdf_name": text.lower(),
                "pdf_url": f"{CHART_BASE_URL}/{airac}/{text.lower()}",
            }
        )


def process_xml_db(xml_document, airac, airport_codes):
    airports = 0

    current_airport = AirportChartSupplement(airac)
    airport_data = {"skip": False}

    for event, element in xml_document:
        tag = element.tag.strip()
        text = element.text.strip() if element.text is not None else ""

        update_current_tags(
            current_airport,
            airport_data,
            airport_codes,
            airac,
            event,
            element,
            tag,
            text,
        )

        if event == END_EVENT and tag == "airport":
            if not airport_data["skip"]:
                AirportRepository.put_airport(current_airport)
                airports += 1

            current_airport.reset_for_next_airport()
            airport_data["skip"] = False

    return airports


def insert_cs_to_dynamodb(airac, files_path, airport_codes, months):
    year = airac[0:2]
    month = months[airac[2:4]].upper()
    day = airac[4:6]

    logInfo("Beginning to process chart supplement data for DynamoDB")
    try:
        file = open(files_path / f"afd_{day}{month}20{year}.xml")
    except FileNotFoundError:
        logError(
            f"No airport DB file afd_{day}{month}20{year}.xml found in {files_path}"
        )
    else:
        xml_document = ElementTree.iterparse(file, [START_EVENT, END_EVENT])
        airports = process_xml_db(xml_document, airac, airport_codes)

        logInfo(f"Finished processing data for {str(airports)} airports")
    finally:
        file.close()
