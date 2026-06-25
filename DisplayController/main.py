import time
import argparse
from threading import Thread
from typing import Optional
from utils import serial_ports
from controller import Controller
from ui import UILeds
import json


def list_serial_ports():
    ports = serial_ports()
    for p in ports:
        print(p)


def controller_loop(controller: Controller):
    print("Start controller_loop")
    try:
        controller.start()
    except KeyboardInterrupt:
        controller.stop()


def run(serial_port: Optional[str], osc_addr: str, ui: Optional[UILeds]):
    controller = Controller(serial_port=serial_port, osc_addr=osc_addr, ui=ui)

    if ui:
        thd = Thread(target=controller_loop, args=(controller,))
        thd.start()
        time.sleep(1)
        print("Start UI loop")
        ui.mainloop()
        controller.stop()
        thd.join()
    else:
        controller_loop(controller)


parser = argparse.ArgumentParser(
    prog='DisplayController')
parser.add_argument("serialport", nargs="?")
parser.add_argument(
    "-l", "--list", help="list serial ports and exit", action="store_true")
parser.add_argument(
    "-s", "--stub", help="no serial", action="store_true")
parser.add_argument(
    "-u", "--ui", help="show leds", action="store_true")
parser.add_argument("-c", "--conf", help="Use config file")


def load_conf(path: str) -> str:
    with open(path,  "r", encoding="utf-8") as f:
        data = json.load(f)
        serial_port = data["main_arduino"]["port_com"]
        return serial_port


def main():
    args = parser.parse_args()
    if args.list:
        list_serial_ports()
        return

    if args.conf:
        print(f"using conf file {args.conf}")
        args.serialport = load_conf(args.conf)

    use_ui = bool(args.ui)
    no_serial = bool(args.stub)
    if args.serialport is None and no_serial is False:
        print("missing serialport")
        parser.print_usage()
        return
    print(use_ui)
    if no_serial is False:
        print(f"using serial port '{args.serialport}'")

    ui = None
    if use_ui:
        ui = UILeds(num_leds=26)
    run(serial_port=args.serialport, osc_addr="192.168.1.255", ui=ui)


if __name__ == "__main__":
    main()
