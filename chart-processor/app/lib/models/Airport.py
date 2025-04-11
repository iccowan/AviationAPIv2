from botocore.exceptions import ClientError

from app.lib.logger import logError
from app.lib.models.AirportData import AirportData, AirportDataEncoder


class Airport:
    CHART_SECTIONS = {
        "airport_diagram": 0,
        "general": 1,
        "departure": 2,
        "arrival": 3,
        "approach": 4,
    }

    TABLE_NAME = "aviationapi-airports"

    def __init__(self, airac):
        self.airac = airac
        self.airport_data = AirportData()
        self.reset_for_next_airport()

    def reset_for_next_airport(self):
        self.airport_diagram = {f"airac_{self.airac}": []}

        self.general_charts = {f"airac_{self.airac}": []}

        self.departure_charts = {f"airac_{self.airac}": []}

        self.arrival_charts = {f"airac_{self.airac}": []}

        self.approach_charts = {f"airac_{self.airac}": []}

        self.chart_supplement = {f"airac_{self.airac}": []}

        self.airport_data.reset_airport_specific()

    def insert_new_chart(self, chart_group, chart):
        if chart_group == self.CHART_SECTIONS["airport_diagram"]:
            self.airport_diagram[f"airac_{self.airac}"].append(chart)
        if chart_group == self.CHART_SECTIONS["general"]:
            self.general_charts[f"airac_{self.airac}"].append(chart)
        if chart_group == self.CHART_SECTIONS["departure"]:
            self.departure_charts[f"airac_{self.airac}"].append(chart)
        if chart_group == self.CHART_SECTIONS["arrival"]:
            self.arrival_charts[f"airac_{self.airac}"].append(chart)
        if chart_group == self.CHART_SECTIONS["approach"]:
            self.approach_charts[f"airac_{self.airac}"].append(chart)

    def copy(self):
        new = Airport(self.airac)
        new.airport_data = self.airport_data.copy()
        new.airport_diagram = self.airport_diagram.copy()
        new.general_charts = self.general_charts.copy()
        new.departure_charts = self.departure_charts.copy()
        new.arrival_charts = self.arrival_charts.copy()
        new.approach_charts = self.approach_charts.copy()

        return new

    def to_dynamodb_dict(self):
        return self.airport_data.to_dynamodb_dict() | self.charts_to_dynamodb_dicts()

    def generate_dynamodb_key(self):
        id = self.airport_data.icao_ident
        if len(id) == 0:
            id = self.airport_data.faa_ident

        return {"unique_airport_id": {"S": id}}

    def charts_dynamodb_string(self):
        return (
            ""
            f"airport_diagram.airac_{self.airac} = :airport_diagram,"
            f"general_charts.airac_{self.airac} = :general_charts,"
            f"departure_charts.airac_{self.airac} = :departure_charts,"
            f"arrival_charts.airac_{self.airac} = :arrival_charts,"
            f"approach_charts.airac_{self.airac} = :approach_charts,"
            f"chart_supplement.airac_{self.airac} = :chart_supplement"
        )

    def charts_to_dynamodb_dicts(self):
        airac_key = f"airac_{self.airac}"

        return {
            ":airport_diagram": {
                "L": [
                    chart.format_for_dynamodb()
                    for chart in self.airport_diagram[airac_key]
                ]
            },
            ":general_charts": {
                "L": [
                    chart.format_for_dynamodb()
                    for chart in self.general_charts[airac_key]
                ]
            },
            ":departure_charts": {
                "L": [
                    chart.format_for_dynamodb()
                    for chart in self.departure_charts[airac_key]
                ]
            },
            ":arrival_charts": {
                "L": [
                    chart.format_for_dynamodb()
                    for chart in self.arrival_charts[airac_key]
                ]
            },
            ":approach_charts": {
                "L": [
                    chart.format_for_dynamodb()
                    for chart in self.approach_charts[airac_key]
                ]
            },
            ":chart_supplement": {
                "L": [
                    chart.format_for_dynamodb()
                    for chart in self.chart_supplement[airac_key]
                ]
            },
        }

    def init_new_airport(self, dynamodb_client):
        key = self.generate_dynamodb_key()
        update_expression = "SET airport_data = :airport_data, airport_diagram = :airport_diagram, general_charts = :general_charts, departure_charts = :departure_charts, arrival_charts = :arrival_charts, approach_charts = :approach_charts, chart_supplement = :chart_supplement"
        expression_attribute_values = {
            ":airport_data": {"M": {}},
            ":airport_diagram": {"M": {}},
            ":general_charts": {"M": {}},
            ":departure_charts": {"M": {}},
            ":arrival_charts": {"M": {}},
            ":approach_charts": {"M": {}},
            ":chart_supplement": {"M": {}},
        }
        conditional_expression = "attribute_not_exists(icao_ident)"

        try:
            dynamodb_client.update_item(
                TableName=self.TABLE_NAME,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ConditionExpression=conditional_expression,
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                pass
            logError(
                f"Error inserting new airport {self.airport_data.icao_ident} {self.airport_data.faa_ident}"
            )

    def update_dynamodb(self, dynamodb_client):
        self.init_new_airport(dynamodb_client)

        key = self.generate_dynamodb_key()
        update_expression = f"SET {self.airport_data.set_dynamodb_string()},{self.charts_dynamodb_string()}"
        expression_attribute_values = self.to_dynamodb_dict()

        dynamodb_client.update_item(
            TableName=self.TABLE_NAME,
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )

    def __str__(self):
        return str(
            {
                "airport_data": self.airport_data,
                "airport_diagram": self.airport_diagram,
                "general_chart": self.general_charts,
                "departure_charts": self.departure_charts,
                "arrival_charts": self.arrival_charts,
                "approach_charts": self.approach_charts,
            }
        )

    def __repr__(self):
        return self.__str__()
