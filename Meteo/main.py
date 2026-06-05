import argparse
import sys
import datetime
from typing import Tuple
from controller import Controller
from infoclimat.api import API
from ephemerides.api import SolarAPI

parser = argparse.ArgumentParser(prog='Meteo')
parser.add_argument("oscaddr", nargs="?")
parser.add_argument("-t", action="store_true")

COORDS = (43.29695, 5.38107)  # marseille
COORDS = (48, 0.2)  # le snam
COORDS = (48.866669, 2.433330)  # montreuil


def run_controller(osc_addr: str, coords: Tuple[float, float]):
    controller = Controller(osc_addr=osc_addr, coords=coords)
    controller.run()


def get_mean_nebu_for(data: API.Response, ts_in: datetime.datetime, ts_out: datetime.datetime):
    print(f"Getting mean between {ts_in.time()} and {ts_out.time()}")
    entries = data.get_time_entries(ts_in.date())
    print(entries)
    return


def test():
    print("test")
    coords = (48.866669, 2.433330)  # montreuil
    weather_api = API(coords=coords)
    solar_api = SolarAPI(coords=coords)

    today, tomorrow = solar_api.get()
    print(tomorrow)
    resp = weather_api.get()
    get_mean_nebu_for(resp, tomorrow.sunrise, tomorrow.sunset)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.t:
        test()
        sys.exit(0)
    osc_addr = args.oscaddr if args.oscaddr else "127.0.0.1"
    print(f"using osc address '{osc_addr}'")
    run_controller(osc_addr, coords=COORDS)
    sys.exit(0)
