from threading import Thread
import time
from enum import Enum
from display_controller import DisplayController
from colors import linear_gradient, hex_to_rgb, polylinear_gradient


class AnimState(Enum):
    UNDEFINED = 0
    WELCOME_ANIM = 1
    PULSES = 2
    ON_THE_CLOCK = 3


class Pulse:
    def __init__(self) -> None:
        self.percent_pulse = 0
        self.time_high_ms = 800
        self.time_low_ms = 300
        self.time_waiting_until = 0
        self.target_inc = 5
        self.start_col = [245, 241, 235]  # sun color
        self.mid_col = [105, 96, 254]
        self.end_col = [3, 7, 87]
        self.grad_size = 12
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=self.grad_size)

    def set_pulse_times(self, high: int, low: int):
        self.time_high_ms = high
        self.time_low_ms = low

    def set_start_color(self, r: int, g: int, b: int):
        self.start_col = [r, g, b]
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=self.grad_size)

    def set_mid_color(self, r: int, g: int, b: int):
        self.mid_col = [r, g, b]
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=self.grad_size)

    def set_end_color(self, r: int, g: int, b: int):
        self.end_col = [r, g, b]
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=self.grad_size)

    def set_size(self, size: int):
        self.grad_size = size
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=self.grad_size)

    def paint(self, elapsed_ms: int, display_controller: DisplayController):
        self

    def draw_gradient_at(self, start_idx: int, display_controller: DisplayController):
        percent = float(self.percent_pulse/100)
        for i in range(self.grad_size):
            r = int(self.gradient[i][0] * percent)
            g = int(self.gradient[i][1] * percent)
            b = int(self.gradient[i][2] * percent)
            sun_0_pos = (start_idx+i) % 24
            sun_1_pos = (start_idx-i+1) % 24
            display_controller.set_pix1(sun_0_pos, r, g, b)
            display_controller.set_pix1(sun_1_pos, r, g, b)

    def update(self, elapsed_ms: int):
        if self.time_waiting_until > 0:
            if (elapsed_ms >= self.time_waiting_until):
                self.time_waiting_until = 0
                print(f"Done waiting at {elapsed_ms}")
            return

        self.percent_pulse += self.target_inc
        if self.percent_pulse >= 100:
            self.percent_pulse = 100
            self.target_inc = -self.target_inc
            if self.time_waiting_until == 0:
                self.time_waiting_until = elapsed_ms + self.time_high_ms
                print(
                    f"HIGH: at {elapsed_ms} sleep until {self.time_waiting_until} self.target_inc={self.target_inc}")

        elif self.percent_pulse < 0:
            self.percent_pulse = 0
            self.target_inc = -self.target_inc
            if self.time_waiting_until == 0:
                self.time_waiting_until = elapsed_ms + self.time_low_ms
                print(
                    f"LOW: at {elapsed_ms} sleep until {self.time_waiting_until} self.target_inc={self.target_inc}")


class LogicController:
    def __init__(self, display_controller: DisplayController) -> None:
        self.display_controller = display_controller
        self.thread = Thread(target=self._run)
        self._should_run = False
        self.anim_state = AnimState.UNDEFINED
        self.next_state = AnimState.WELCOME_ANIM

        self.update_delay_ms = 40
        self.pulse = Pulse()

        self.sun_pos: int = 0

    def start(self):
        self._should_run = True
        self.thread.start()

    def stop(self):
        self._should_run = False
        self.thread.join()

    def _run(self):
        elapsed = 0
        while self._should_run:
            self.display_controller.clear_buffer()
            self.paint(elapsed)
            self.display_controller.update_display()
            time.sleep(self.update_delay_ms/1000)
            elapsed += self.update_delay_ms
        print("logic returned")

    def paint(self, elapsed_ms):
        self.pulse.update(elapsed_ms)
        self.pulse.draw_gradient_at(self.sun_pos, self.display_controller)

    def set_grad_size(self, size: int):
        self.pulse.set_size(size)

    def set_grad_color(self, typ: int, r: float, g: float, b: float):
        print(f"Test logic typ={typ} r={r} g={g} b={b}")
        if typ == 0:
            self.pulse.set_start_color(int(r), int(g), int(b))
        elif typ == 1:
            self.pulse.set_mid_color(int(r), int(g), int(b))
        elif typ == 2:
            self.pulse.set_end_color(int(r), int(g), int(b))

    def set_pulse_times(self, high: float, low: float):
        self.pulse.set_pulse_times(int(high), int(low))
