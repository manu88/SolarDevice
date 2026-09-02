from typing import Optional
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from arduinos_controller import ArduinosController
from osc_server_interface import OSCServerInterface


class OSCServer(OSCServerInterface):
    def __init__(self, osc_client_addr: str) -> None:
        self.secondary_ctlr: Optional[ArduinosController] = None
        self.osc_client = udp_client.SimpleUDPClient(
            osc_client_addr, 8012, allow_broadcast=True)
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/servo", self.osc_servo)

        self.dispatcher.map("/ping", self.osc_ping)
        self.dispatcher.map("/update", self.osc_update)
        self.dispatcher.map("/pix1", self.osc_set_pix1)
        self.dispatcher.map("/all", self.osc_set_all)
        self.dispatcher.map("/clear1", self.osc_clear1)

        self.server = osc_server.ThreadingOSCUDPServer(
            ("", 8010), self.dispatcher)

    def osc_ping(self, args):
        print(f"ping {args}")

    def osc_update(self, args):
        print("Update")
        self.secondary_ctlr.display_ctrl.update_display()

    def osc_clear1(self, args):
        print("clear1")
        self.secondary_ctlr.display_ctrl.clear_buffer()

    def osc_set_all(self, args, r: float, g: float, b: float):
        print("set_all")
        self.secondary_ctlr.display_ctrl.set_all(int(r), int(g), int(b))

    def osc_set_pix1(self, args, i: int, r: float, g: float, b: float):
        print("set_pix1")
        self.secondary_ctlr.display_ctrl.set_pix1(i, int(r), int(g), int(b))

    def osc_servo(self, _, servo_idx: int, duration_ms: int):
        print(f"osc_servo servo_idx={servo_idx} duration_ms={duration_ms}")
        real_servo_idx = servo_idx % 3
        board_id = servo_idx//3
        print(
            f"Sending to board={board_id} real_servo_idx={real_servo_idx} duration={duration_ms}")
        self.secondary_ctlr.send_motor(board_id, real_servo_idx, duration_ms)

    def start(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

    def send_sensor(self, index: int, value: float, is_rotating: int):
        self.osc_client.send_message(
            "/sensor", [index, value, is_rotating])
