import requests
import time
from typing import Optional, Dict, Any, Iterable, Tuple
import datetime


MAX_REQUESTS_IN_24H = 5000
MIN_INTERVAL_IN_SEC = 10
INFO_CLIMAT_URI = "http://www.infoclimat.fr/public-api/gfs/json?_ll=43.29695,5.38107&_auth=ABpXQFMtACICL1ZhBHIGL1gwUmcJfwEmA39VNlwyBHkHZlU4DmsHbFY8VClVegAxWHUPbF1qCDFRMlc3AHIFeQBhVzpTOQBnAmlWMgQ9Bi1YdFIvCTcBJgN%2FVTpcOQR5B2VVNg5qB3tWMVQ0VXsANlhpD25dfQgvUTNXNwBqBWIAYVc7UzMAagJlVjMEKwYtWG1SOwllATgDZlVhXDcEMQdlVWAOaQc3VjlUN1V7ADBYbg9tXWUIMFE6VzQAaAV5AHxXSlNDAH8CLVZ2BGEGdFh2UmcJaAFt&_c=5843c5d3fb19aea4ac430f5585a78c6d"


def _get_date_str(date: Optional[datetime.date] = None) -> str:
    if date is None:
        date = datetime.datetime.now().date()
    assert isinstance(date, datetime.date)
    return date.strftime("%Y-%m-%d")


def _current(hour: int, hours: Iterable[int]) -> int:
    for v in sorted(hours, key=lambda x: (abs(hour-x), x)):
        if v <= hour:
            return v
    return -1


def _next(hour: int, hours: Iterable[int]) -> int:
    for v in sorted(hours, key=lambda x: (abs(hour-x), x)):
        if v > hour:
            return v
    return -1


def _get_interval_entries(hour: int, times: dict[int, str]) -> Tuple[int, int]:
    return (_current(hour, times.keys()), _next(hour, times))


class API:
    class Response:
        def __init__(self, data: Dict[str, Any]):
            self.data = data
            pass

        def __repr__(self) -> str:
            return str(self.data)

        def is_valid(self) -> bool:
            return self.data["request_state"] == 200

        def _get_bounds_dates(self, current_datetime: datetime.datetime, just_check_current: bool = False) -> Tuple[str, str]:
            date = _get_date_str(current_datetime.date()) + " "
            times = {}

            for entry in self.data.keys():
                if entry.startswith(date):
                    hour = int(entry[len(date):][0:2])
                    times[hour] = entry

            current_entry, next_entry = _get_interval_entries(
                current_datetime.hour, times)

            if current_entry == -1 and next_entry == -1:
                return "", ""
            if current_entry == -1:
                # check previous day, 11pm-ish
                prev_day = current_datetime - datetime.timedelta(days=1)
                prev_day = prev_day.replace(hour=23)
                current_entry, _ = self._get_bounds_dates(
                    prev_day, just_check_current=True)
                return current_entry, times[next_entry]
            if next_entry == -1 and just_check_current is False:
                # check next day, midnight-ish
                next_day = current_datetime + datetime.timedelta(days=1)
                next_day = next_day.replace(hour=0)
                _, next_entry = self._get_bounds_dates(next_day)
                return times[current_entry], next_entry
            return times[current_entry] if current_entry != -1 else "", times[next_entry] if next_entry != -1 else ""

        def get_current(self, current_datetime: Optional[datetime.datetime] = None):
            if current_datetime is None:
                current_datetime = datetime.datetime.now()

            return self._get_bounds_dates(current_datetime)

    def __init__(self) -> None:
        self.last_req_time = 0
        self._last_rep: Optional[API.Response] = None

    def get(self) -> Optional[Response]:
        current = time.time()
        delta = current - self.last_req_time
        if delta <= MIN_INTERVAL_IN_SEC:
            return self._last_rep
        ret = requests.get(INFO_CLIMAT_URI)
        if ret.status_code != 200:
            print(f"got bad response code: {ret.status_code}")
            return self._last_rep
        self.last_req_time = current
        resp = API.Response(ret.json())
        if not resp.is_valid():
            print("Invalid response")
            return None
        self._last_rep = resp
        return resp


if __name__ == "__main__":
    resp = API.Response({
        "2026-03-25 01:00:00": {},
        "2026-03-25 04:00:00": {},
        "2026-03-25 07:00:00": {},
        "2026-03-25 10:00:00": {},
        "2026-03-25 13:00:00": {},
        "2026-03-25 16:00:00": {},
        "2026-03-25 19:00:00": {},
        "2026-03-25 22:00:00": {},
        "2026-03-26 01:00:00": {},
    })

    assert resp.get_current(datetime.datetime(2026, 3, 25, 17, 22, 4)) == (
        "2026-03-25 16:00:00", "2026-03-25 19:00:00")

    assert resp.get_current(datetime.datetime(2026, 3, 25, 1, 22, 4)) == (
        "2026-03-25 01:00:00", "2026-03-25 04:00:00")

    assert resp.get_current(datetime.datetime(2026, 3, 25, 23, 22, 4)) == (
        "2026-03-25 22:00:00", "2026-03-26 01:00:00")

    assert resp.get_current(datetime.datetime(2026, 3, 26, 00, 22, 4)) == (
        "2026-03-25 22:00:00", "2026-03-26 01:00:00")

    print("----------------------")
    current_entry, next_entry = resp.get_current(
        datetime.datetime(2026, 3, 26, 00, 22, 4))
    print(f"between {current_entry} and {next_entry}")
