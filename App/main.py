import argparse
import sys
from infoclimat.api import API
from display.mire import gen_mire
from app.app import App


parser = argparse.ArgumentParser(prog='SolarDevice')
parser.add_argument('-m', '--mire',
                    action='store_true')
parser.add_argument('-a', '--api',
                    action='store_true')

parser.add_argument('--show-source',
                    action='store_true')

parser.add_argument('-c', '--conf')


def test_api():
    api = API()
    resp = api.get()
    assert resp
    weather_entry = resp.get_current()
    print(weather_entry)
    print(
        f"nebu: {weather_entry.current_nebulosite()} -> {weather_entry.next_nebulosite()}")


def run_app(args):
    conf_file_path = args.conf if args.conf else ""
    app = App(conf_file_path, show_source=args.show_source)
    app.run()


if __name__ == "__main__":
    args = parser.parse_args()
    if args.api:
        test_api()
        sys.exit(0)
    if args.mire:
        gen_mire()
        sys.exit(0)
    run_app(args)
