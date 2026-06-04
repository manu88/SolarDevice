from dateutil import parser
import datetime
from typing import Optional, Tuple
import requests


class Result:
    def __init__(self, sunset: datetime.time, sunrise: datetime.time) -> None:
        self.sunset = sunset
        self.sunrise = sunrise

    def __repr__(self) -> str:
        return f"sunrise:{self.sunrise} sunset:{self.sunset}"


def _get(base_uri: str, day: datetime.date) -> Optional[dict]:
    uri = base_uri + f"&date={day}"
    ret = requests.get(uri, timeout=10)
    if ret.status_code != 200:
        print(f"got bad response code: {ret.status_code}")
        return None
    return ret.json()


def _process(data: dict) -> Optional[Result]:
    if data["status"] != "OK":
        return None
    if "results" not in data:
        return None
    entries = data["results"]
    sunrise_str = entries["sunrise"]
    sunset_str = entries["sunset"]

    sunrise = parser.parse(sunrise_str).time()
    sunset = parser.parse(sunset_str).time()
    return Result(sunset=sunset, sunrise=sunrise)


class SolarAPI:
    def __init__(self, coords: Tuple[float, float]):
        self.uri = f"https://api.sunrise-sunset.org/json?lat={coords[0]}&lng={coords[1]}"
        print(f"Using URL '{self.uri}'")

    def get(self) -> Optional[Tuple[Result, Result]]:
        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        print("Tomorrow=", tomorrow.date())

        today_resp = _get(self.uri, today.date())
        if today_resp is None:
            return None
        tomorrow_resp = _get(self.uri, tomorrow.date())
        if tomorrow_resp is None:
            return None
        e0 = _process(today_resp)
        e1 = _process(tomorrow_resp)
        if e0 is not None and e1 is not None:
            return e0, e1
        return


if __name__ == "__main__":
    COORDS = (48.866669, 2.433330)  # montreuil
    api = SolarAPI(COORDS)
    ret = api.get()
    print(ret)
