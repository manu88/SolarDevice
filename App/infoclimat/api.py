import requests
import time
from typing import Optional, Dict
MAX_REQUESTS_IN_24H = 5000
MIN_INTERVAL_IN_SEC = 10
INFO_CLIMAT_URI = "http://www.infoclimat.fr/public-api/gfs/json?_ll=48.85341,2.3488&_auth=UUtTRFIsXH4DLgcwVyFReFgwV2IBdwMkUy9RMg1oUSxTOFY3Dm4EYlI8Ui9TfFZgVXhTMA02U2MAawpyAHIDYlE7Uz9SOVw7A2wHYld4UXpYdlc2ASEDJFM4UT4NflEzUzdWNQ5zBG5SP1IuU2FWYFVnUywNLVNqAGQKagBpA2JROlM1UjBcOANlB3pXeFFjWGJXZAE%2FAz1TNVFkDWlRMlNkVjQOZQRmUjxSLlNkVmBVZ1MzDTFTbgBgCm4AcgN%2FUUtTRFIsXH4DLgcwVyFReFg%2BV2kBag%3D%3D&_c=3e78244ea0bf448ae9762a84f47c7645"


class API:
    class Response:
        def __init__(self, data: Dict):
            self.data = data
            pass

        def __repr__(self) -> str:
            return str(self.data)

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
        self._last_rep = resp
        return resp
