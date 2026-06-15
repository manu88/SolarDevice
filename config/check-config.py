import sys
import json

GENERAL_KEY = "General"
SEUILS_KEY = "Seuils"


def check_keys(data: dict, keys: list) -> bool:
    is_ok = True
    for key in keys:
        if key not in data:
            print(f"missing key '{key}'")
            is_ok = False
    return is_ok


def vet_list(data: any, expected_count: int, name: str) -> bool:
    ok = True
    if not isinstance(data, list):
        print(f"invalid format for '{name}': unknown value '{data}'")
        ok = False
    elif len(data) != expected_count:
        print(f"Expected 2 entries for '{name}', got {len(data)}")
        ok = False
    return ok


def vet_seuil_value(data: dict, typ, name: str) -> bool:
    ok = True
    if "value" not in data:
        print(f"Missing 'value' entry in '{name}'")
        ok = False
    elif isinstance(data["value"], typ) is False:
        print(
            f"Wrong value type for '{name}', expected {typ} got {type(data["value"])}")
        ok = False
    return ok


def check_general(data: dict) -> bool:
    GPS_KEY = "GPS"
    HEURES_KEY = "Heures"
    VERNISSAGE_KEY = "Vernissage"
    if not check_keys(data, [GPS_KEY, HEURES_KEY, VERNISSAGE_KEY]):
        return False

    vet_list(data[HEURES_KEY], 2, HEURES_KEY)
    vet_list(data[GPS_KEY], 2, GPS_KEY)

    return True


def check_seuils(data: dict) -> bool:
    SA1_KEY = "S-A-1"
    SA2_KEY = "S-A-2"
    SB_KEY = "S-B"
    SC_KEY = "S-C"
    if not check_keys(data, [SA1_KEY, SA2_KEY, SB_KEY, SC_KEY]):
        return False

    ok = True
    if not vet_seuil_value(data[SA1_KEY], float, SA1_KEY):
        ok = False

    if not vet_seuil_value(data[SA2_KEY], float, SA2_KEY):
        ok = False
    if not vet_seuil_value(data[SB_KEY], float, SB_KEY):
        ok = False
    if not vet_seuil_value(data[SC_KEY], float, SC_KEY):
        ok = False
    return ok


def main(config_path: str) -> bool:
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        print("--> Check global entries:")
        if not check_keys(data, [GENERAL_KEY, SEUILS_KEY]):
            return False

        ok = True
        print(f"--> Check '{GENERAL_KEY}' entry:")
        if not check_general(data[GENERAL_KEY]):
            print(f"Error(s) in '{GENERAL_KEY}'")
            ok = False

        print(f"--> Check '{SEUILS_KEY}' entry:")
        if not check_seuils(data[SEUILS_KEY]):
            print(f"Error(s) in '{SEUILS_KEY}'")
            ok = False

        return ok


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage python3 check-config.py filepath")
        sys.exit(1)
    config_path = sys.argv[1]
    ret = main(config_path)
    valid = "valid" if ret else "invalid"
    print(f"file config '{config_path}' is {valid}")
    sys.exit(0 if ret else 1)
