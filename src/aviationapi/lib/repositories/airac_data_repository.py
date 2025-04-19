import os

import boto3

from aviationapi.lib.models.AiracData import AiracData
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ.get("AIRAC_TABLE_NAME", "aviationapi-airac")
TABLE = boto3.resource("dynamodb").Table(TABLE_NAME)


def get_airac(cycle_type="next", cycle_chart_type="charts"):
    airac_dict = _get({"cycle_type": cycle_type, "cycle_chart_type": cycle_chart_type})

    if airac_dict is None:
        return None

    return AiracData(airac_data_dict=airac_dict)


def get_airac_by_cycle_chart_type_and_airac(airac, cycle_chart_type):
    airac_dict = _get_airac_by_airac_name_and_chart_type({"airac": airac, "cycle_chart_type": cycle_chart_type})

    if airac_dict is None:
        return None

    return AiracData(airac_data_dict=airac_dict)


def put_airac(airac):
    _put(airac.db_dict())


def delete_airac(airac):
    _delete(
        {"cycle_type": airac.cycle_type, "cycle_chart_type": airac.cycle_chart_type}
    )


def _get(key, index=None):
    response = TABLE.get_item(Key=key)

    if "Item" in response:
        return response["Item"]

    return None

def _get_airac_by_airac_name_and_chart_type(key):
    response = TABLE.query(
        IndexName="airac_by_airac_name_and_chart_type",
        KeyConditionExpression=Key("airac").eq(key["airac"]) & Key("cycle_chart_type").eq(key["cycle_chart_type"])
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
