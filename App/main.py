from infoclimat.api import API
from display.display import Display
from display.mire import gen_mire
import pygame
from app.app import App


def test_api():
    api = API()
    resp = api.get()
    assert resp
    weatherEntry = resp.get_current()
    print(weatherEntry)
    print(
        f"nebu: {weatherEntry.current_nebulosite()} -> {weatherEntry.next_nebulosite()}")


def test_display():
    app = App()
    app.run()


if __name__ == "__main__":
    # gen_mire()
    test_display()
