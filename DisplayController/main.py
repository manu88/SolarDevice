import argparse
from utils import serial_ports
from controller import Controller


def list_serial_ports():
    ports = serial_ports()
    for p in ports:
        print(p)


parser = argparse.ArgumentParser(
    prog='DisplayController')
parser.add_argument(
    "-l", "--list", help="list serial ports and exit", action="store_true")


def main():
    args = parser.parse_args()
    if args.list:
        list_serial_ports()
        return
    controller = Controller()
    controller.start()


if __name__ == "__main__":
    main()
