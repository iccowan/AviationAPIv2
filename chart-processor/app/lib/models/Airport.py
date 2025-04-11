from app.lib.models.AirportData import AirportData

class Airport:
    CHART_SECTIONS = {
        'airport_diagram': 0,
        'general': 1,
        'departure': 2,
        'arrival': 3,
        'approach': 4
    }

    def __init__(self, airac):
        self.airac = airac
        self.airport_data = AirportData()
        self.reset_for_next_airport()

    def reset_for_next_airport(self):
        self.airport_diagram = {
            f'airac_{self.airac}': []
        }

        self.general_charts = {
            f'airac_{self.airac}': []
        }

        self.departure_charts = {
            f'airac_{self.airac}': []
        }

        self.arrival_charts = {
            f'airac_{self.airac}': []
        }

        self.approach_charts = {
            f'airac_{self.airac}': []
        }

        self.airport_data.reset_airport_specific()

    def insert_new_chart(self, chart_group, chart):
        if chart_group == self.CHART_SECTIONS['airport_diagram']:
            self.airport_diagram[f'airac_{self.airac}'].append(chart)
        if chart_group == self.CHART_SECTIONS['general']:
            self.general_charts[f'airac_{self.airac}'].append(chart)
        if chart_group == self.CHART_SECTIONS['departure']:
            self.departure_charts[f'airac_{self.airac}'].append(chart)
        if chart_group == self.CHART_SECTIONS['arrival']:
            self.arrival_charts[f'airac_{self.airac}'].append(chart)
        if chart_group == self.CHART_SECTIONS['approach']:
            self.approach_charts[f'airac_{self.airac}'].append(chart)

    def copy(self):
        new = Airport(self.airac)
        new.airport_data = self.airport_data.copy()
        new.airport_diagram = self.airport_diagram.copy()
        new.general_charts = self.general_charts.copy()
        new.departure_charts = self.departure_charts.copy()
        new.arrival_charts = self.arrival_charts.copy()
        new.approach_charts = self.approach_charts.copy()

        return new

    def __str__(self):
        return str({
            'airport_data': self.airport_data,
            'airport_diagram': self.airport_diagram,
            'general_chart': self.general_charts,
            'departure_charts': self.departure_charts,
            'arrival_charts': self.arrival_charts,
            'approach_charts': self.approach_charts
        })

    def __repr__(self):
        return self.__str__()

