import argparse
import sys
from infoclimat.api import API
from display.mire import gen_mire
from app.app import App


parser = argparse.ArgumentParser(prog='SolarDevice')
parser.add_argument('-m', '--mire',
                    action='store_true')

parser.add_argument('-c', '--conf')


def test_api():
    api = API()
    resp = api.get()
    assert resp
    weatherEntry = resp.get_current()
    print(weatherEntry)
    print(
        f"nebu: {weatherEntry.current_nebulosite()} -> {weatherEntry.next_nebulosite()}")


def run_app(conf_file_path: str):
    app = App(conf_file_path)
    app.run()


if __name__ == "__main__":
    args = parser.parse_args()
    if args.mire:
        gen_mire()
        sys.exit(0)
    run_app(args.conf if args.conf else "")
