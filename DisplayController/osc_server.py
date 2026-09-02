from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from secondary_controller import SecondaryController
from osc_server_interface import OSCServerInterface


class OSCServer(OSCServerInterface):
    def __init__(self, osc_client_addr: str) -> None:
        self.secondary_ctlr: SecondaryController = None
        self.osc_client = udp_client.SimpleUDPClient(
            osc_client_addr, 8012, allow_broadcast=True)
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/servo", self.osc_servo)
        self.server = osc_server.ThreadingOSCUDPServer(
            ("", 8010), self.dispatcher)

    def osc_servo(self, _, servo_idx: int, duration_ms: int):
        print(f"osc_servo servo_idx={servo_idx} duration_ms={duration_ms}")
        real_servo_idx = servo_idx % 3
        board_id = servo_idx//3
        print(
            f"Sending to board={board_id} real_servo_idx={real_servo_idx} duration={duration_ms}")
        self.secondary_ctlr.send_motor(board_id, real_servo_idx, duration_ms)

    def start(self):
        self.server.serve_forever()

    def send_sensor(self, index: int, value: float, is_rotating: int):
        self.osc_client.send_message(
            "/sensor", [index, value, is_rotating])
