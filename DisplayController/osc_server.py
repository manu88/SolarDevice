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
        self.dispatcher.map("/clock2", self.osc_clock2)
        self.dispatcher.map("/day", self.osc_day)
        self.dispatcher.map("/realtime", self.osc_set_realtime)

        self.dispatcher.map("/luminosity", self.osc_luminosity)
        self.dispatcher.map("/nebulosity", self.osc_nebulosity)

        # to sort, mostly debug/tests
        self.dispatcher.map("/set-grad-color", self.osc_set_grad_color)
        self.dispatcher.map("/set-sun", self.osc_set_sun)
        self.dispatcher.map("/set-state", self.osc_set_state)

        self.server = osc_server.ThreadingOSCUDPServer(
            ("", 8010), self.dispatcher)

    def osc_nebulosity(self, _, neb: float):

        # max spread = 13
        spread = int(13*(1-neb))
        print(f"Got nebulosity {neb} -> spread= {spread}")
        self.logic.set_grad_size(spread)

    def osc_luminosity(self, _, lum: float):
        self.osc_client.send_message("/luminosity", [lum])

    def osc_day(self, _, state: float):
        self.logic.set_day_state(int(state))

    def osc_clock(self, _, hh: float, mm: float):
        self.logic.on_clock(int(hh), int(mm))

    def osc_clock2(self, _, hh: float, mm: float):
        self.logic.on_clock2(int(hh), int(mm))

    def osc_set_realtime(self, _, use_realtime: float):
        self.logic.set_use_realtime(int(use_realtime))

    def osc_ping(self, args):
        print(f"ping {args}")

    def osc_dump(self, _):
        self.secondary_ctlr.display_ctrl.dump()

    def osc_dump_arduino(self, _):
        self.secondary_ctlr.display_ctrl.dump_arduino()

    def start(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

    def send_hour(self, hour: int):
        self.osc_client.send_message("/clock", [hour, 0])

    def send_current_sensor(self, index: int, value: float, is_rotating: int):
        try:
            self.osc_client.send_message(
                "/current-sensor", [index, value, is_rotating])
        except Exception:
            pass

    def send_sensor(self, index: int, value: float, is_rotating: int):
        try:
            self.osc_client.send_message(
                "/sensor", [index, value, is_rotating])
        except Exception:
            pass

    def osc_set_grad_color(self, _, typ: int, r: float, g: float, b: float):
        self.logic.set_grad_color(typ, r, g, b)

    def osc_set_state(self, _, state: float):
        self.logic.set_next_state(int(state))

    def osc_set_sun(self, _,  pos: float):
        self.logic.sun_pos = int(pos)

    def osc_set_pulse_times(self, _, high: float, low: float):
        self.logic.set_pulse_times(high, low)
