from infoclimat.api import API


if __name__ == "__main__":
    api = API()
    resp = api.get()
    assert resp
    weatherEntry = resp.get_current()
    print(weatherEntry)
    print(
        f"nebu: {weatherEntry.current_nebulosite()} -> {weatherEntry.next_nebulosite()}")
