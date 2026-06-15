import time
from typing import Tuple
from pythonosc import udp_client
from Meteo.infoclimat.api import API
from Meteo.ephemerides.api import SolarAPI


class Controller:
    def __init__(self, osc_addr: str, coords: Tuple[float, float]) -> None:
        self.osc_client = udp_client.SimpleUDPClient(
            osc_addr, 8011, allow_broadcast=True)
        self.weather_api = API(coords=coords)
        self.solar_api = SolarAPI(coords=coords)
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self._get_state()
            time.sleep(10)

    def _get_state(self):
        weather_resp = self.weather_api.get()
        assert weather_resp
        weather_entry = weather_resp.get_current()

        solar_resp = self.solar_api.get()
        print(solar_resp)
        self.send_state(weather_entry.current_nebulosite(),
                        weather_entry.next_nebulosite())

    def send_state(self, current_nebulosite: float, next_nebulosite: float):
        self.osc_client.send_message(
            "/nebulosite", [current_nebulosite, next_nebulosite])
