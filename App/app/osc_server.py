from pythonosc import osc_server, udp_client
from pythonosc.dispatcher import Dispatcher
import threading


class OSCServer:
    def __init__(self, dispatcher: Dispatcher, ip: str, port: int) -> None:
        self._thread = threading.Thread(target=self._start)
        self.osc_server = osc_server.ThreadingOSCUDPServer(
            (ip, port), dispatcher)
        self.client = udp_client.SimpleUDPClient("127.0.0.1", 5006)
        self._thread.start()

    def stop(self):
        print("OSCServer: shutdowning osc_server")
        self.osc_server.shutdown()
        print("OSCServer: shutdowning osc_server done")
        print("OSCServer: joining thread")
        self._thread.join()
        print("OSCServer: joining thread done")

    def _start(self):
        print("OSCServer: serving")
        self.osc_server.serve_forever()
        print("OSCServer: after serve_forever")
