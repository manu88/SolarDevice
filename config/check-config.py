import sys
import json
from config.Config import Config


def main(config_path: str) -> bool:
    conf = Config.from_json_file(config_path)
    return conf.is_valid


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage python3 check-config.py filepath")
        sys.exit(1)
    config_path = sys.argv[1]
    ret = main(config_path)
    valid = "valid" if ret else "invalid"
    print(f"file config '{config_path}' is {valid}")
    sys.exit(0 if ret else 1)
