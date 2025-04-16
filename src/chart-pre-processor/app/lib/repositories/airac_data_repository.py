import os

import boto3

from app.lib.models.AiracData import AiracData

TABLE_NAME = os.environ.get("AIRAC_DB_NAME", "aviationapi-airac")
TABLE = boto3.resource("dynamodb").Table(TABLE_NAME)


def get_airac(cycle_type="next", cycle_chart_type="charts"):
    airac_dict = _get({"cycle_type": cycle_type, "cycle_chart_type": cycle_chart_type})

    if airac_dict is None:
        return None

    return AiracData(airac_data_dict=airac_dict)


def put_airac(airac):
    _put(airac.db_dict())


def delete_airac(airac):
    _delete(
        {"cycle_type": airac.cycle_type, "cycle_chart_type": airac.cycle_chart_type}
    )


def _get(key):
    response = TABLE.get_item(Key=key)
    if "Item" in response:
        return response["Item"]

    return None


def _put(airac_dict):
    TABLE.put_item(Item=airac_dict)


def _delete(key):
    TABLE.delete_item(Key=key)
