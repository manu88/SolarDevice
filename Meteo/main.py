import argparse
import sys
import datetime
from Meteo.controller import Controller
from Meteo.infoclimat.api import API
from Meteo.ephemerides.api import SolarAPI
from config.Config import Config

parser = argparse.ArgumentParser(prog='Meteo')
parser.add_argument("config", help="json-config path")
parser.add_argument("oscaddr", nargs="?")
parser.add_argument("-t", action="store_true")
parser.add_argument("-v", "--v", action="store_true", help="verbose")
parser.add_argument("-p", "--port", type=int, default=8012,
                    help="osc sending port, default to 8012")


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

    conf = Config.from_json_file(args.config)
    if not conf.is_valid:
        print(f"invalid config at '{args.config}'")
        sys.exit(1)
    osc_addr = args.oscaddr if args.oscaddr else "127.0.0.1"
    print(f"using osc address '{osc_addr}':{args.port}")
    controller = Controller(
        osc_addr=osc_addr, coords=conf.get_gps_coords(), verbose=args.v)
    controller.run()
    sys.exit(0)
