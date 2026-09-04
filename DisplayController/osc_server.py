from typing import Optional
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from arduinos_controller import ArduinosController
from osc_server_interface import OSCServerInterface
from logic_controller import LogicController


class OSCServer(OSCServerInterface):
    def __init__(self, osc_client_addr: str, logic: LogicController) -> None:
        self.logic = logic
        self.secondary_ctlr: Optional[ArduinosController] = None
        self.osc_client = udp_client.SimpleUDPClient(
            osc_client_addr, 8012, allow_broadcast=True)
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/ping", self.osc_ping)
        self.dispatcher.map("/dump", self.osc_dump)
        self.dispatcher.map("/dump-arduinos", self.osc_dump_arduino)
        self.dispatcher.map("/clock", self.osc_clock)
        self.dispatcher.map("/realtime", self.osc_set_realtime)

        # to sort, mostly debug/tests
        self.dispatcher.map("/servo", self.osc_servo)
        self.dispatcher.map("/update", self.osc_update)
        self.dispatcher.map("/pix1", self.osc_set_pix1)
        self.dispatcher.map("/all", self.osc_set_all)
        self.dispatcher.map("/clear1", self.osc_clear1)
        self.dispatcher.map("/set-grad-color", self.osc_set_grad_color)
        self.dispatcher.map("/set-grad-spread", self.osc_set_grad_spread)
        self.dispatcher.map("/set-sun", self.osc_set_sun)
        self.dispatcher.map("/set-state", self.osc_set_state)
        self.dispatcher.map("/start-all", self.osc_start_all)

        self.server = osc_server.ThreadingOSCUDPServer(
            ("", 8010), self.dispatcher)

    def osc_clock(self, _, hh: float, mm: float):
        self.logic.on_clock(int(hh), int(mm))

    def osc_set_realtime(self, _, use_realtime: float):
        self.logic.set_use_realtime(int(use_realtime))

    def osc_ping(self, args):
        print(f"ping {args}")

    def osc_dump(self, _):
        self.secondary_ctlr.display_ctrl.dump()

    def osc_dump_arduino(self, _):
        self.secondary_ctlr.display_ctrl.dump_arduino()

    def osc_update(self, _):
        # print("osc_update")
        self.secondary_ctlr.display_ctrl.update_display()

    def osc_clear1(self, _):
        # print("clear1")
        self.secondary_ctlr.display_ctrl.clear_buffer()

    def osc_set_all(self, _, r: float, g: float, b: float):
        # print("set_all")
        self.secondary_ctlr.display_ctrl.set_all(int(r), int(g), int(b))

    def osc_set_pix1(self, _, i: int, r: float, g: float, b: float):
        # print("set_pix1")
        self.secondary_ctlr.display_ctrl.set_pix1(i, int(r), int(g), int(b))

    def osc_servo(self, _, servo_idx: int, duration_ms: int):
        self.secondary_ctlr.set_motor(servo_idx, duration_ms)

    def start(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

    def send_hour(self, hour: int):
        self.osc_client.send_message("/clock", [hour, 0])

    def send_current_sensor(self, index: int, value: float, is_rotating: int):
        self.osc_client.send_message(
            "/current-sensor", [index, value, is_rotating])

    def send_sensor(self, index: int, value: float, is_rotating: int):
        self.osc_client.send_message(
            "/sensor", [index, value, is_rotating])

    def osc_set_grad_color(self, _, typ: int, r: float, g: float, b: float):
        self.logic.set_grad_color(typ, r, g, b)

    def osc_set_state(self, _, state: float):
        self.logic.set_next_state(int(state))

    def osc_set_sun(self, _,  pos: float):
        self.logic.sun_pos = int(pos)

    def osc_set_grad_spread(self, _, size: float):
        self.logic.set_grad_size(int(size))

    def osc_set_pulse_times(self, _, high: float, low: float):
        self.logic.set_pulse_times(high, low)

    def osc_start_all(self, _):
        print("Start all mendocinos")
        self.secondary_ctlr.set_all(500)
