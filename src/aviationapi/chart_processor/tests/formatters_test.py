from xml.etree.ElementTree import Element

from aviationapi.chart_processor.app.format_chart_db_data import (
    START_EVENT,
    update_current_airport_tags,
)
from aviationapi.chart_processor.app.format_cs_db_data import update_current_tags
from aviationapi.lib.models.Airport import Airport
from aviationapi.lib.models.AirportChartSupplement import AirportChartSupplement


def test_update_current_airport_tags_sets_faa_country():
    airport = Airport("250417")
    element = Element(
        "airport_name",
        {
            "ID": "John F Kennedy",
            "apt_ident": "JFK",
            "icao_ident": "KJFK",
            "military": "N",
        },
    )

    update_current_airport_tags(airport, START_EVENT, element, "airport_name", "")

    assert airport.airport_data.country == "USA"


def test_update_current_tags_sets_faa_country_for_chart_supplement():
    airport = AirportChartSupplement("250417")
    airport_data = {"skip": False}

    update_current_tags(
        airport, airport_data, {}, "250417", "end", None, "aptid", "JFK"
    )

    assert airport.airport_data.country == "USA"
