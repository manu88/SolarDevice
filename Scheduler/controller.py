import time
import datetime
from pythonosc import udp_client


class Controller:
    def __init__(self, osc_addr: str) -> None:
        self.osc_client = udp_client.SimpleUDPClient(
            osc_addr, 8012, allow_broadcast=True)
        self._stop_asked = False

    def run(self):
        self._stop_asked = False
        while self._stop_asked is False:
            time.sleep(1)
            now = datetime.datetime.now()
            self.osc_client.send_message("/clock", [now.hour, now.minute])
