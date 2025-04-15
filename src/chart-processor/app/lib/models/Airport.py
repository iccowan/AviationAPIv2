from botocore.exceptions import ClientError

from app.lib.logger import logError
from app.lib.models.AirportData import AirportData
from app.lib.models.Chart import ChartType


class Airport:
    TABLE_NAME = "aviationapi-airports"

    def __init__(self, airac):
        self.airac = airac
        self.airport_data = AirportData()
        self.charts = {}
        self.reset_for_next_airport()

    def reset_for_next_airport(self):
        for chart_type in list(ChartType):
            self.charts[chart_type.value] = []

        self.airport_data.reset_airport_specific()

    def copy(self):
        new = Airport(self.airac)
        new.airport_data = self.airport_data.copy()
        new.airport_diagram = self.airport_diagram.copy()
        new.general_charts = self.general_charts.copy()
        new.departure_charts = self.departure_charts.copy()
        new.arrival_charts = self.arrival_charts.copy()
        new.approach_charts = self.approach_charts.copy()

        return new

    def db_dict(self):
        charts_dict = {}
        for k, v in self.charts.items():
            charts_dict[k] = [chart.db_dict() for chart in v]

        return {"airport_data": self.airport_data.db_dict(), "charts": charts_dict}

    def __repr__(self):
        return str(self.__dict__)
