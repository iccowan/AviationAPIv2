from botocore.exceptions import ClientError

from aviationapi.lib.logger import logError
from aviationapi.lib.models.AirportData import AirportData
from aviationapi.lib.models.Chart import Chart, ChartType


class Airport:
    def __init__(self, airac, airport_dict={}):
        self.airac = airac
        self.airport_data = AirportData()
        self.charts = {}
        self.reset_for_next_airport()

        for k, v in airport_dict.items():
            if k == "airport_data":
                self.airport_data = AirportData(v)
                continue

            if k == "charts":
                charts_dict = {}
                for chart_type, chart_list in v.items():
                    charts_dict[chart_type] = [Chart(chart) for chart in chart_list]

                self.charts = charts_dict
                continue


            setattr(self, k, v)

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

    def dict(self):
        charts_dict = {}
        for k, v in self.charts.items():
            charts_dict[k] = [chart.dict() for chart in v]

        return {"airport_data": self.airport_data.dict(), "charts": charts_dict}

    def __repr__(self):
        return str(self.__dict__)
