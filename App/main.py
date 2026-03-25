from infoclimat.api import API


if __name__ == "__main__":
    api = API()
    resp = api.get()
    assert resp
    resp.get_current()
