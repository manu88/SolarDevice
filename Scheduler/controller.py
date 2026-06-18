import time
import datetime
from pythonosc import udp_client
from config.Config import Config


class Controller:
    def __init__(self, osc_addr: str, conf: Config) -> None:
        self.conf = conf
        self.osc_client = udp_client.SimpleUDPClient(
            osc_addr, 8012, allow_broadcast=True)
        self._stop_asked = False

    def run(self):
        self._stop_asked = False
        while self._stop_asked is False:
            now = datetime.datetime.now()
            self.osc_client.send_message("/clock", [now.hour, now.minute])
            time.sleep(5)
