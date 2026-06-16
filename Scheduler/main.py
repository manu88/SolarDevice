import sys
import argparse
from Scheduler.controller import Controller
from config.Config import Config


parser = argparse.ArgumentParser(prog='Scheduler')
parser.add_argument("config", help="json-config path")

if __name__ == "__main__":
    args = parser.parse_args()
    conf = Config.from_json_file(args.config)
    if not conf.is_valid:
        print(f"invalid config at '{args.config}'")
        sys.exit(1)
    c = Controller("192.168.1.255", conf=conf)
    c.run()
