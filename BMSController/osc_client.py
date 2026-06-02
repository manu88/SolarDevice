from pythonosc import udp_client


class OSCClient:
    def __init__(self, addr: str, port: int) -> None:
        self.osc_client = udp_client.SimpleUDPClient(
            addr, port, allow_broadcast=True)

    def send_status(self, percent):
        self.osc_client.send_message("/battery", percent)
