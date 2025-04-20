import os

import boto3
from boto3.dynamodb.conditions import Key

from aviationapi.lib.models.AiracData import AiracData

TABLE_NAME = os.environ.get("AIRAC_TABLE_NAME", "aviationapi-airac")
TABLE = boto3.resource("dynamodb").Table(TABLE_NAME)


def get_airac(cycle_type="next", cycle_chart_type="charts"):
    airac_dict = _get({"cycle_type": cycle_type, "cycle_chart_type": cycle_chart_type})

    if airac_dict is None:
        return None

    return AiracData(airac_data_dict=airac_dict)


def get_airac_by_cycle_chart_type_and_airac(airac, cycle_chart_type):
    airac_dict = _get_airac_by_airac_name_and_chart_type(
        {"airac": airac, "cycle_chart_type": cycle_chart_type}
    )

    if airac_dict is None:
        return None

    return AiracData(airac_data_dict=airac_dict)


def get_all_airac(cycle_type):
    airac_data_list = _query({"cycle_type": cycle_type})

    if airac_data_list is None:
        return None

    if type(airac_data_list) is not list:
        return AiracData(airac_data_dict=airac_data_list)

    return [AiracData(airac_data_dict=airac_data) for airac_data in airac_data_list]


def put_airac(airac):
    _put(airac.dict())


def delete_airac(airac):
    _delete(
        {"cycle_type": airac.cycle_type, "cycle_chart_type": airac.cycle_chart_type}
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
