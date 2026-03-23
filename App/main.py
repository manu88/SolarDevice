from infoclimat.api import API


if __name__ == "__main__":
    api = API()
    resp = api.get()
    print(resp)
