import json
from numbers import Number

GENERAL_KEY = "General"
SEUILS_KEY = "Seuils"
GPS_KEY = "GPS"
HEURES_KEY = "Heures"
VERNISSAGE_KEY = "Vernissage"
SA1_KEY = "S-A-1"
SA2_KEY = "S-A-2"
SB_KEY = "S-B"
SC_KEY = "S-C"


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
    return vet_percent_0_1(data["value"], name)


def vet_percent_0_1(value, name) -> bool:
    if 0 <= value <= 1:
        return True
    print(f"Value '{name}' not in [0,1]: {value}")
    return False


def check_general(data: dict) -> bool:
    if not check_keys(data, [GPS_KEY, HEURES_KEY, VERNISSAGE_KEY]):
        return False

    vet_list(data[HEURES_KEY], 2, HEURES_KEY)
    vet_list(data[GPS_KEY], 2, GPS_KEY)

    return True


def check_seuils(data: dict) -> bool:
    if not check_keys(data, [SA1_KEY, SA2_KEY, SB_KEY, SC_KEY]):
        return False

    ok = True
    if not vet_seuil_value(data[SA1_KEY], Number, SA1_KEY):
        ok = False

    if not vet_seuil_value(data[SA2_KEY], Number, SA2_KEY):
        ok = False
    if not vet_seuil_value(data[SB_KEY], Number, SB_KEY):
        ok = False
    if not vet_seuil_value(data[SC_KEY], Number, SC_KEY):
        ok = False
    return ok


class Config:
    @staticmethod
    def from_json_file(path: str) -> 'Config':
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Config(data)
        return None

    def __init__(self, data: dict):
        self.data = data
        self.is_valid = False
        self.is_checked = False
        self.vet()
        assert self.is_checked

    def get_gps_coords(self) -> tuple[float, float]:
        return self.data[GENERAL_KEY][GPS_KEY]

    def vet(self) -> bool:
        if self.is_checked:
            return self.is_valid
        self.is_valid = self._do_vet()
        self.is_checked = True
        return self.is_valid

    def _do_vet(self) -> bool:
        print("--> Check global entries:")
        if not check_keys(self.data, [GENERAL_KEY, SEUILS_KEY]):
            return False

        ok = True
        print(f"--> Check '{GENERAL_KEY}' entry:")
        if not check_general(self.data[GENERAL_KEY]):
            print(f"Error(s) in '{GENERAL_KEY}'")
            ok = False

        print(f"--> Check '{SEUILS_KEY}' entry:")
        if not check_seuils(self.data[SEUILS_KEY]):
            print(f"Error(s) in '{SEUILS_KEY}'")
            ok = False

        return ok
