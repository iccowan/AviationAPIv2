from json import JSONEncoder


class Chart:
    def __init__(self, dict=None):
        self.chart_name = ""
        self.chart_sequence = ""
        self.pdf_name = ""
        self.pdf_url = ""
        self.did_change = False
        self.change_pdf_name = None
        self.change_pdf_url = None

        if dict is not None:
            for k, v in dict.items():
                setattr(self, k, v)

    def format_for_dynamodb(self):
        changes = {}
        if self.did_change:
            changes = {
                "change_pdf_name": {"S": self.change_pdf_name},
                "change_pdf_url": {"S": self.change_pdf_url},
            }

        return {
            "M": {
                "chart_name": {"S": self.chart_name},
                "chart_sequence": {"S": self.chart_sequence},
                "pdf_name": {"S": self.pdf_name},
                "pdf_url": {"S": self.pdf_url},
                "did_change": {"BOOL": self.did_change},
            }
            | changes
        }

    def __str__(self):
        return str(
            {
                "chart_name": self.chart_name,
                "chart_sequence": self.chart_sequence,
                "pdf_name": self.pdf_name,
                "pdf_url": self.pdf_url,
                "did_change": self.did_change,
                "change_pdf_name": self.change_pdf_name,
                "change_pdf_url": self.change_pdf_url,
            }
        )

    def __repr__(self):
        return self.__str__()


class ChartEncoder(JSONEncoder):
    def default(self, chart):
        return chart.__dict__

    def decode(self, json_object):
        return Chart(json_object)
