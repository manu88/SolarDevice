import argparse
from utils import serial_ports
from controller import Controller


def list_serial_ports():
    ports = serial_ports()
    for p in ports:
        print(p)


parser = argparse.ArgumentParser(
    prog='DisplayController')
parser.add_argument("serialport", nargs="?")
parser.add_argument(
    "-l", "--list", help="list serial ports and exit", action="store_true")
parser.add_argument(
    "-s", "--stub", help="no serial", action="store_true")


def main():
    args = parser.parse_args()
    if args.list:
        list_serial_ports()
        return

    no_serial = bool(args.stub)
    if args.serialport is None and no_serial is False:
        print("missing serialport")
        parser.print_usage()
        return
    print(no_serial)
    if no_serial is False:
        print(f"using serial port '{args.serialport}'")
    controller = Controller(serial_port=args.serialport,
                            osc_addr="192.168.1.255")
    try:
        controller.start()
    except KeyboardInterrupt:
        controller.stop()


if __name__ == "__main__":
    main()
