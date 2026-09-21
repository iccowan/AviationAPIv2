from abc import ABC, abstractmethod


class ChartProvider(ABC):
    provider = ""

    @abstractmethod
    def process_packet(self, packet, airac):
        pass
