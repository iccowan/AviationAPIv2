import os

import boto3
from boto3.dynamodb.conditions import Key

from aviationapi.lib.chart_provider_keys import (
    DEFAULT_CHART_PROVIDER,
    build_provider_cycle_chart_type,
    parse_provider_cycle_chart_type,
)
from aviationapi.lib.models.AiracData import AiracData

TABLE_NAME = os.environ.get("AIRAC_TABLE_NAME", "aviationapi-airac")
TABLE = boto3.resource("dynamodb").Table(TABLE_NAME)


def _normalize_airac_dict(airac_dict):
    normalized_airac_dict = airac_dict.copy()
    parsed_cycle_chart_type = parse_provider_cycle_chart_type(
        normalized_airac_dict["cycle_chart_type"]
    )
    normalized_airac_dict["provider"] = normalized_airac_dict.get(
        "provider",
        normalized_airac_dict.get("source", parsed_cycle_chart_type["provider"]),
    )
    normalized_airac_dict.pop("source", None)
    normalized_airac_dict["cycle_chart_type"] = parsed_cycle_chart_type[
        "cycle_chart_type"
    ]

    return normalized_airac_dict


def _build_storage_cycle_chart_type(provider, cycle_chart_type):
    return build_provider_cycle_chart_type(provider, cycle_chart_type)


def _build_airac_lookup_keys(cycle_type, cycle_chart_type, provider):
    lookup_keys = [
        {
            "cycle_type": cycle_type,
            "cycle_chart_type": _build_storage_cycle_chart_type(
                provider, cycle_chart_type
            ),
        }
    ]

    if provider == DEFAULT_CHART_PROVIDER:
        lookup_keys.append(
            {"cycle_type": cycle_type, "cycle_chart_type": cycle_chart_type}
        )

    return lookup_keys


def _build_airac_query_cycle_chart_types(cycle_chart_type, provider):
    cycle_chart_types = [_build_storage_cycle_chart_type(provider, cycle_chart_type)]

    if provider == DEFAULT_CHART_PROVIDER:
        cycle_chart_types.append(cycle_chart_type)

    return cycle_chart_types


def _to_airac_data(airac_dict):
    if airac_dict is None:
        return None

    return AiracData(airac_data_dict=_normalize_airac_dict(airac_dict))


def _matches_provider(airac_dict, provider):
    return _normalize_airac_dict(airac_dict)["provider"] == provider


def _is_source_aware_airac_dict(airac_dict):
    return "::" in airac_dict["cycle_chart_type"]


def get_airac(
    cycle_type="next",
    cycle_chart_type="charts",
    provider=DEFAULT_CHART_PROVIDER,
):
    airac_dict = None
    for lookup_key in _build_airac_lookup_keys(cycle_type, cycle_chart_type, provider):
        airac_dict = _get(lookup_key)
        if airac_dict is not None:
            break

    if airac_dict is None:
        return None

    return _to_airac_data(airac_dict)


def get_airac_by_cycle_chart_type_and_airac(
    airac,
    cycle_chart_type,
    provider=DEFAULT_CHART_PROVIDER,
):
    airac_dict = None
    for query_cycle_chart_type in _build_airac_query_cycle_chart_types(
        cycle_chart_type, provider
    ):
        airac_dict = _get_airac_by_airac_name_and_chart_type(
            {"airac": airac, "cycle_chart_type": query_cycle_chart_type}
        )
        if airac_dict is not None:
            break

    if airac_dict is None:
        return None

    return _to_airac_data(airac_dict)


def get_all_airac(cycle_type, provider=DEFAULT_CHART_PROVIDER):
    airac_data_list = _query({"cycle_type": cycle_type})

    if airac_data_list is None:
        return None

    if type(airac_data_list) is not list:
        airac_data_list = [airac_data_list]

    selected_airac_data = {}
    for airac_data in airac_data_list:
        if not _matches_provider(airac_data, provider):
            continue

        normalized_airac_dict = _normalize_airac_dict(airac_data)
        cycle_chart_type = normalized_airac_dict["cycle_chart_type"]

        if cycle_chart_type not in selected_airac_data:
            selected_airac_data[cycle_chart_type] = airac_data
            continue

        if _is_source_aware_airac_dict(airac_data):
            selected_airac_data[cycle_chart_type] = airac_data

    normalized_airac_data = [
        _to_airac_data(airac_data) for airac_data in selected_airac_data.values()
    ]

    if len(normalized_airac_data) == 0:
        return None

    if len(normalized_airac_data) == 1:
        return normalized_airac_data[0]

    return normalized_airac_data


def put_airac(airac):
    airac_dict = airac.dict()
    airac_dict["cycle_chart_type"] = _build_storage_cycle_chart_type(
        airac.provider, airac.cycle_chart_type
    )
    _put(airac_dict)


def delete_airac(airac):
    _delete(
        {
            "cycle_type": airac.cycle_type,
            "cycle_chart_type": _build_storage_cycle_chart_type(
                airac.provider, airac.cycle_chart_type
            ),
        }
    )


def _get(key):
    response = TABLE.get_item(Key=key)

    if "Item" in response:
        return response["Item"]

    return None


def _query(key):
    key_condition = None

    for k, v in key.items():
        if key_condition is None:
            key_condition = Key(k).eq(v)
            continue

        key_condition = key_condition & Key(k).eq(v)

    response = TABLE.query(KeyConditionExpression=key_condition)

    items = response["Items"]
    if len(items) == 1:
        return items[0]

    if len(items) == 0:
        return None

    return items


def _get_airac_by_airac_name_and_chart_type(key):
    response = TABLE.query(
        IndexName="airac_by_airac_name_and_chart_type",
        KeyConditionExpression=Key("airac").eq(key["airac"])
        & Key("cycle_chart_type").eq(key["cycle_chart_type"]),
    )

    items = response["Items"]
    if len(items) == 1:
        return items[0]

    if len(items) == 0:
        return None

    return items


def _put(airac_dict):
    TABLE.put_item(Item=airac_dict)


def _delete(key):
    TABLE.delete_item(Key=key)
