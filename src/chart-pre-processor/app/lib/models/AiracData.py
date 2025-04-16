from enum import Enum
from datetime import datetime


class Packets(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    CHART_SUPPLEMENT = "ChartSupplement"


class CycleTypes(Enum):
    CURRENT = "current"
    NEXT = "next"


class CycleChartTypes(Enum):
    CHARTS = "charts"
    CHART_SUPPLEMENT = "chart_supplement"


class AiracData:
    VALID_DATE_FORMAT = "%Y-%m-%d"

    def __init__(
        self,
        airac="",
        cycle_type=CycleTypes.CURRENT.value,
        cycle_chart_type=CycleChartTypes.CHARTS.value,
        valid_date=None,
        is_retrieveable=False,
        is_packet_processed={packet.value: False for packet in list(Packets)},
        airac_data_dict={},
    ):
        self.airac = airac
        self.cycle_type = cycle_type
        self.cycle_chart_type = cycle_chart_type
        self.valid_date = valid_date
        self.is_retrieveable = is_retrieveable
        self.is_packet_processed = is_packet_processed

        for k, v in airac_data_dict.items():
            if k == "valid_date":
                v = AiracData.date_str_to_datetime(v)

            self.__dict__[k] = v

    def date_str_to_datetime(date_str):
        return datetime.strptime(date_str, self.VALID_DATE_FORMAT)

    def valid_date_to_str(self):
        return self.valid_date.strftime(AiracData.VALID_DATE_FORMAT)

    def db_dict(self):
        self_dict = self.__dict__
        self_dict["valid_date"] = self.valid_date_to_str()

        return self_dict

    def __repr__(self):
        return str(self.__dict__)
