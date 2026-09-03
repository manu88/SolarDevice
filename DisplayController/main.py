
import argparse
import time
from threading import Thread
from typing import Optional, List
from utils import serial_ports
from display_controller import DisplayController
from arduinos_controller import ArduinosController
from ui import UILeds
from osc_server import OSCServer


def list_serial_ports():
    ports = serial_ports()
    for p in ports:
        print(p)


def run_server(server: OSCServer):
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    server.stop()
    print("OSC server Returned")


def run_server_thread(server: OSCServer):
    thd = Thread(target=run_server, args=(server,))
    thd.start()
    return thd


def run(serial_ports: List[str], osc_client_addr: str, ui: Optional[UILeds]):
    display_controller = DisplayController(ui=ui)
    arduinos_controller = ArduinosController(display_controller, serial_ports)
    # ["/dev/cu.usbmodem213101","/dev/cu.usbmodem1401"])

    server = OSCServer(osc_client_addr=osc_client_addr)
    server.secondary_ctlr = arduinos_controller
    arduinos_controller.osc_server = server

    arduinos_controller.start()

    if ui:
        thread = run_server_thread(server)
        print("Start UI loop")
        time.sleep(1)
        ui.mainloop()
        server.stop()
        thread.join()
    run_server(server)
    arduinos_controller.stop()


parser = argparse.ArgumentParser(
    prog='DisplayController')
parser.add_argument("serialports", nargs="+")
parser.add_argument(
    "-l", "--list", help="list serial ports and exit", action="store_true")
parser.add_argument("-a", "--addr", help="Address to broadcast osc to")
parser.add_argument(
    "-u", "--ui", help="show leds", action="store_true")


def main():
    args = parser.parse_args()
    if args.list:
        list_serial_ports()
        return

    if args.addr is None:
        print("missing addr")
        parser.print_usage()
        return

    if args.serialports is None:
        print("missing serialports")
        parser.print_usage()
        return
    print(args.serialports)

    ui = None
    use_ui = bool(args.ui)
    if use_ui:
        ui = UILeds(num_leds=24)
    osc_addr = args.addr
    print(f"Sending osc data on {osc_addr}")
    run(serial_ports=args.serialports, osc_client_addr=osc_addr, ui=ui)


if __name__ == "__main__":
    main()
