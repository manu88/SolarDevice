from typing import Optional, Dict


def _compute_nebulosite(data_entry=Optional[Dict]) -> float:
    if data_entry is None:
        return -1
    if "nebulosite" not in data_entry:
        return -1
    # val is a percentage. eg 21 -> 21%
    if "totale" not in data_entry["nebulosite"]:
        return -1
    return data_entry["nebulosite"]["totale"] / 100


class WeatherState:
    def __init__(self, current_date: str, next_date: str, current_entry=Optional[Dict], next_entry=Optional[Dict]):
        self.current_entry = current_entry
        self.next_entry = next_entry
        self.current_date = current_date
        self.next_date = next_date

    def __repr__(self) -> str:
        return f"WeatherState between {self.current_date} and {self.next_date}"

    # returns a percentage value [0,1]
    def current_nebulosite(self) -> float:
        return _compute_nebulosite(self.current_entry)

    # returns a percentage value [0,1]
    def next_nebulosite(self) -> float:
        return _compute_nebulosite(self.next_entry)
