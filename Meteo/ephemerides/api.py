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
        print(f"Using URL '{self.uri}' for sunrise-sunset.org")
        self.cache: dict[datetime.date, dict] = dict()

    def get(self) -> Optional[Tuple[Result, Result]]:
        today = datetime.datetime.now()
        return self._get(today)

    def _get(self, date: datetime.datetime) -> Optional[Tuple[Result, Result]]:
        day_after = date + datetime.timedelta(days=1)

        today_resp = self._do_get(self.uri, date.date())
        if today_resp is None:
            return None
        tomorrow_resp = self._do_get(self.uri, day_after.date())
        if tomorrow_resp is None:
            return None
        e0 = _process(today_resp)
        e1 = _process(tomorrow_resp)
        if e0 is not None and e1 is not None:
            return e0, e1
        return None

    def _do_get(self, base_uri: str, day: datetime.date) -> Optional[dict]:
        if day in self.cache:
            return self.cache[day]
        uri = base_uri + f"&date={day}"
        ret = requests.get(uri, timeout=10)
        if ret.status_code != 200:
            print(f"got bad response code: {ret.status_code}")
            return None
        resp = ret.json()
        self.cache[day] = resp
        return resp


if __name__ == "__main__":
    COORDS = (48.866669, 2.433330)  # montreuil
    api = SolarAPI(COORDS)
    ret = api.get()
    print(ret)
