import sys
import json

GENERAL_KEY = "General"
SEUILS_KEY = "Seuils"


def main(config_path: str) -> int:
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        required_keys = [GENERAL_KEY, SEUILS_KEY]

        is_ok = True
        for key in required_keys:
            if key not in data:
                print(f"missing key '{key}'")
                is_ok = False
        if not is_ok:
            return 1

        print("Got keys")
        return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage python3 check-config.py filepath")
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
