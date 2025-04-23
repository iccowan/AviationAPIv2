from aviationapi.lib.models.AirportData import AirportData


class AirportChartSupplement:
    def __init__(self, airac, airport_dict={}):
        self.airac = airac
        self.airport_data = AirportData()
        self.charts = []

        for k, v in airport_dict.items():
            if k == "airport_data":
                self.airport_data = AirportData(v)
                continue

            setattr(self, k, v)

    def reset_for_next_airport(self):
        self.charts = []
        self.airport_data.reset_airport_specific()
        self.airport_data.is_military = None

    def copy(self):
        new = AirportChartSupplement(self.airac)
        new.airac = self.airac
        new.charts = self.charts

        return new

    def dict(self):
        return {"airport_data": self.airport_data.dict(), "charts": self.charts}

    def __repr__(self):
        return str(self.__dict__)
