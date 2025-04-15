from app.lib.models.AirportData import AirportData


class AirportChartSupplement:
    TABLE_NAME = "aviationapi-airports"

    def __init__(self, airac):
        self.airac = airac
        self.airport_data = AirportData()
        self.charts = []

    def reset_for_next_airport(self):
        self.charts = []
        self.airport_data.reset_airport_specific()
        self.airport_data.is_military = None

    def copy(self):
        new = AirportChartSupplement(self.airac)
        new.airac = self.airac
        new.charts = self.charts

        return new

    def db_dict(self):
        return {"airport_data": self.airport_data.db_dict(), "charts": self.charts}

    def __repr__(self):
        return str(self.__dict__)
