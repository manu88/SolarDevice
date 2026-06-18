import sys
import argparse
from Scheduler.controller import Controller
from config.Config import Config


parser = argparse.ArgumentParser(prog='Scheduler')
parser.add_argument("config", help="json-config path")
parser.add_argument(
    "--addr", help="network address to send msgs to", default="127.0.0.1")

if __name__ == "__main__":
    args = parser.parse_args()
    print(f"sending msgs to '{args.addr}'")
    conf = Config.from_json_file(args.config)
    if not conf.is_valid:
        print(f"invalid config at '{args.config}'")
        sys.exit(1)
    c = Controller(args.addr, conf=conf)
    c.run()
