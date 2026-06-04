import argparse
import sys
from typing import Tuple
from controller import Controller

parser = argparse.ArgumentParser(prog='Meteo')
parser.add_argument("oscaddr", nargs="?")


COORDS = (43.29695, 5.38107)  # marseille
COORDS = (48, 0.2)  # le snam
COORDS = (48.866669, 2.433330)  # montreuil


def run_controller(osc_addr: str, coords: Tuple[float, float]):
    controller = Controller(osc_addr=osc_addr, coords=coords)
    controller.run()


if __name__ == "__main__":
    args = parser.parse_args()
    osc_addr = args.oscaddr if args.oscaddr else "127.0.0.1"
    print(f"using osc address '{osc_addr}'")
    run_controller(osc_addr, coords=COORDS)
    sys.exit(0)
