from abc import ABC, abstractmethod


class ChartProvider(ABC):
    source = ""

    @abstractmethod
    def process_packet(self, packet, airac):
        pass
