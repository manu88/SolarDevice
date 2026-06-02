import time
from pythonosc import udp_client
from infoclimat.api import API


class Controller:
    def __init__(self, osc_addr: str) -> None:
        self.osc_client = udp_client.SimpleUDPClient(
            osc_addr, 8011, allow_broadcast=True)
        self.api = API()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self._get_state()
            time.sleep(10)

    def _get_state(self):
        resp = self.api.get()
        assert resp
        weather_entry = resp.get_current()
        self.send_state(weather_entry.current_nebulosite(),
                        weather_entry.next_nebulosite())

    def send_state(self, current_nebulosite: float, next_nebulosite: float):
        self.osc_client.send_message(
            "/nebulosite", [current_nebulosite, next_nebulosite])
