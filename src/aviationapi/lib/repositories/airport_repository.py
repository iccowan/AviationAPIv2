import os
from datetime import datetime, timedelta

import boto3

from aviationapi.lib.chart_provider_keys import (
    DEFAULT_CHART_PROVIDER,
    build_airport_data_key,
)
from aviationapi.lib.models.Airport import Airport
from aviationapi.lib.models.AirportChartSupplement import AirportChartSupplement

TABLE_NAME = os.environ.get("AIRPORTS_TABLE_NAME", "aviationapi-airports")
TABLE = boto3.resource("dynamodb").Table(TABLE_NAME)
EXPIRATION_TIMESTAMP = int((datetime.now() + timedelta(days=120)).timestamp())


def _get_airport_provider(airport):
    return getattr(airport, "provider", DEFAULT_CHART_PROVIDER)


def _get_entry_type_for_airport(airport):
    if type(airport).__name__ == "AirportChartSupplement":
        return "cs"

    return "tpp"


def _build_airport_key(unique_airport_id, chart_type, airac, provider):
    return {
        "unique_airport_id": unique_airport_id,
        "chart_type::airac": build_airport_data_key(provider, chart_type, airac),
    }


def generate_key(airport):
    id = airport.airport_data.icao_ident
    if id is None or len(id) == 0:
        id = airport.airport_data.faa_ident

    return _build_airport_key(
        id,
        _get_entry_type_for_airport(airport),
        airport.airac,
        _get_airport_provider(airport),
    )


def _get_legacy_airport_key(unique_airport_id, chart_type, airac):
    return {
        "unique_airport_id": unique_airport_id,
        "chart_type::airac": f"{chart_type}::{airac}",
    }


def _build_airport_lookup_keys(airport_name, airac, chart_type, provider):
    unique_airport_id = airport_name.upper()
    lookup_keys = [_build_airport_key(unique_airport_id, chart_type, airac, provider)]

    if provider == DEFAULT_CHART_PROVIDER:
        lookup_keys.append(
            _get_legacy_airport_key(unique_airport_id, chart_type, airac)
        )

    return lookup_keys


def get_airport(airport_name, airac, chart_type, provider=DEFAULT_CHART_PROVIDER):
    airport_dict = None
    for lookup_key in _build_airport_lookup_keys(
        airport_name, airac, chart_type, provider
    ):
        airport_dict = _get(lookup_key)
        if airport_dict is not None:
            break

    if airport_dict is None:
        return None

    if chart_type == "cs":
        airport = AirportChartSupplement(airac, airport_dict)
    else:
        airport = Airport(airac, airport_dict)

    airport.provider = airport_dict.get(
        "provider", airport_dict.get("source", provider)
    )

    return airport


def put_airport(airport):
    _put(
        airport.dict()
        | generate_key(airport)
        | {
            "provider": _get_airport_provider(airport),
            "expire_at": EXPIRATION_TIMESTAMP,
        }
    )


def _get(key):
    response = TABLE.get_item(Key=key)

    if "Item" in response:
        return response["Item"]

    return None


def _put(airport_dict):
    TABLE.put_item(Item=airport_dict)
