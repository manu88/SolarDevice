from abc import ABC, abstractmethod


class OSCServerInterface(ABC):
    @abstractmethod
    def send_sensor(self, index: int, value: float, is_rotating: int):
        assert (0)
