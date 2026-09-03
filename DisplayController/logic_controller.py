from threading import Thread
import time
from display_controller import DisplayController
from colors import linear_gradient, hex_to_rgb, polylinear_gradient


class LogicController:
    def __init__(self, display_controller: DisplayController) -> None:
        self.display_controller = display_controller
        self.thread = Thread(target=self._run)
        self._should_run = False
        self.update_delay_ms = 40
        self.percent_pulse = 0
        self.time_high_ms = 1500
        self.time_low_ms = 500
        self.time_waiting_until = 0
        self.target_inc = 5
        self.sun_pos = 0
        self.start_col = [245, 241, 235]  # sun color
        self.mid_col = [105, 96, 254]
        self.end_col = [3, 7, 87]
        self.grad_size = 12
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=self.grad_size)

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

    def draw_gradient_at(self, start_idx: int, percent: float):
        for i in range(self.grad_size):
            r = int(self.gradient[i][0] * (self.percent_pulse/100))
            g = int(self.gradient[i][1] * (self.percent_pulse/100))
            b = int(self.gradient[i][2] * (self.percent_pulse/100))
            sun_0_pos = (start_idx+i) % 24
            sun_1_pos = (start_idx-i+1) % 24
            self.display_controller.set_pix1(sun_0_pos, r, g, b)
            self.display_controller.set_pix1(sun_1_pos, r, g, b)

    def update_pulse(self, elapsed_ms):
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

    def paint(self, elapsed_ms):
        self.update_pulse(elapsed_ms)
        percent = float(self.percent_pulse/100)
        self.draw_gradient_at(self.sun_pos, percent)

    def set_grad_size(self, size: int):
        self.grad_size = size
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=self.grad_size)

    def set_grad_color(self, typ: int, r: float, g: float, b: float):
        print(f"Test logic typ={typ} r={r} g={g} b={b}")
        if typ == 0:
            self.start_col[0] = int(r)
            self.start_col[1] = int(g)
            self.start_col[2] = int(b)
        elif typ == 1:
            self.mid_col[0] = int(r)
            self.mid_col[1] = int(g)
            self.mid_col[2] = int(b)
        elif typ == 2:
            self.end_col[0] = int(r)
            self.end_col[1] = int(g)
            self.end_col[2] = int(b)
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=self.grad_size)
        return
        self.display_controller.clear_buffer()
        if self.percent_pulse == 0:
            self.percent_pulse = 100

        else:
            self.percent_pulse = 0
        self.display_controller.update_display()
