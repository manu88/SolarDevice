import argparse
import sys
from infoclimat.api import API


parser = argparse.ArgumentParser(prog='Meteo')


def test_api():
    api = API()
    resp = api.get()
    assert resp
    weather_entry = resp.get_current()
    print(weather_entry)
    print(
        f"nebu: {weather_entry.current_nebulosite()} -> {weather_entry.next_nebulosite()}")


if __name__ == "__main__":
    args = parser.parse_args()
    test_api()
    sys.exit(0)
