from abc import ABC, abstractmethod


class OSCServerInterface(ABC):
    @abstractmethod
    def send_sensor(self, index: int, value: float, is_rotating: int):
        assert (0)

    @abstractmethod
    def send_hour(self, hour: int):
        assert (0)
