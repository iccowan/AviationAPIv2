from datetime import datetime
from enum import Enum

from aviationapi.lib.chart_provider_keys import DEFAULT_CHART_PROVIDER


class CycleTypes(Enum):
    CURRENT = "current"
    NEXT = "next"


class CycleChartTypes(Enum):
    CHARTS = "charts"
    CHART_SUPPLEMENT = "chart_supplement"


class AiracData:
    VALID_DATE_FORMAT = "%Y-%m-%d"

    @staticmethod
    def create_packet_processing_state(expected_jobs=None):
        if expected_jobs is None:
            expected_jobs = []

        return {job: False for job in expected_jobs}

    def __init__(
        self,
        airac="",
        provider=DEFAULT_CHART_PROVIDER,
        cycle_type=CycleTypes.CURRENT.value,
        cycle_chart_type=CycleChartTypes.CHARTS.value,
        valid_date=None,
        is_retrieveable=False,
        expected_jobs=None,
        airac_data_dict=None,
    ):
        self.airac = airac
        self.provider = provider
        self.cycle_type = cycle_type
        self.cycle_chart_type = cycle_chart_type
        self.valid_date = valid_date
        self.is_retrieveable = is_retrieveable

        self.is_packet_processed = AiracData.create_packet_processing_state(
            expected_jobs
        )

        if airac_data_dict is None:
            airac_data_dict = {}

        for k, v in airac_data_dict.items():
            if k == "valid_date":
                v = AiracData.date_str_to_datetime(v)

            setattr(self, k, v)

    def date_str_to_datetime(date_str):
        return datetime.strptime(date_str, AiracData.VALID_DATE_FORMAT)

    def valid_date_to_str(self):
        return self.valid_date.strftime(AiracData.VALID_DATE_FORMAT)

    def dict(self):
        self_dict = self.__dict__.copy()
        self_dict["valid_date"] = self.valid_date_to_str()

        return self_dict

    def api_dict(self):
        self_dict = self.dict()
        del self_dict["is_packet_processed"]

        return self_dict

    def __repr__(self):
        return str(self.__dict__)
