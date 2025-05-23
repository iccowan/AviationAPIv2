from enum import Enum


class Chart:
    def __init__(self, chart_dict=None):
        self.chart_name = None
        self.chart_sequence = None
        self.pdf_name = None
        self.pdf_url = None
        self.did_change = False
        self.change_pdf_name = None
        self.change_pdf_url = None

        if chart_dict is not None:
            for k, v in chart_dict.items():
                setattr(self, k, v)

    def dict(self):
        dict_rep = {
            "chart_name": self.chart_name,
            "chart_sequence": self.chart_sequence,
            "pdf_name": self.pdf_name,
            "pdf_url": self.pdf_url,
            "did_change": self.did_change,
        }

        if self.did_change:
            dict_rep["change_pdf_name"] = self.change_pdf_name
            dict_rep["change_pdf_url"] = self.change_pdf_url

        return dict_rep

    def __repr__(self):
        return str(self.__dict__)


class ChartType(Enum):
    AIRPORT_DIAGRAM = "airport_diagram"
    GENERAL = "general"
    DEPARTURE = "departure"
    ARRIVAL = "arrival"
    APPROACH = "approach"
