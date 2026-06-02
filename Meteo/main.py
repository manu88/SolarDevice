import argparse
import sys
from infoclimat.api import API
from controller import Controller

parser = argparse.ArgumentParser(prog='Meteo')
parser.add_argument("oscaddr", nargs="?")


def test_api():
    api = API()
    resp = api.get()
    assert resp
    weather_entry = resp.get_current()
    print(weather_entry)
    print(
        f"nebu: {weather_entry.current_nebulosite()} -> {weather_entry.next_nebulosite()}")


def run_controller(osc_addr: str):
    controller = Controller(osc_addr=osc_addr)
    controller.run()


if __name__ == "__main__":
    args = parser.parse_args()
    osc_addr = args.oscaddr if args.oscaddr else "127.0.0.1"
    print(f"using osc address '{osc_addr}'")
    run_controller(osc_addr)
    # test_api()
    sys.exit(0)
