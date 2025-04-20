import os
from datetime import datetime, timedelta

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from aviationapi.lib.logger import logError
from aviationapi.lib.models.Airport import Airport
from aviationapi.lib.models.AirportChartSupplement import AirportChartSupplement
from aviationapi.lib.models.Chart import Chart

TABLE_NAME = os.environ.get("AIRPORTS_TABLE_NAME", "aviationapi-airports")
TABLE = boto3.resource("dynamodb").Table(TABLE_NAME)
EXPIRATION_TIMESTAMP = int((datetime.now() + timedelta(days=120)).timestamp())


def generate_key(airport):
    id = airport.airport_data.icao_ident
    if len(id) == 0:
        id = airport.airport_data.faa_ident

    entry_type = "tpp"
    if type(airport).__name__ == "AirportChartSupplement":
        entry_type = "cs"

    return {
        "unique_airport_id": id,
        "chart_type::airac": f"{entry_type}::{airport.airac}",
    }

def get_airport(airport_name, airac, chart_type):
    airport_dict = _get({
        "unique_airport_id": airport_name,
        "chart_type::airac": f"{chart_type}::{airac}"
    })

    if airport_dict is None:
        return None

    if chart_type == "cs":
        return AirportChartSupplement(airac, airport_dict)

    return Airport(airac, airport_dict)


def put_airport(airport):
    _put(
        airport.dict() | generate_key(airport) | {"expire_at": EXPIRATION_TIMESTAMP}
    )

def _get(key):
    response = TABLE.get_item(Key=key)
    
    if "Item" in response:
        return response["Item"]

    return None


def _put(airport_dict):
    TABLE.put_item(Item=airport_dict)
