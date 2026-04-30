from abc import ABC, abstractmethod


class ChartProvider(ABC):
    provider = ""

    @abstractmethod
    def get_expected_jobs(self, cycle_chart_type):
        pass

    @abstractmethod
    def process_packet(self, packet, airac):
        pass
