from display_controller import DisplayController
from colors import polylinear_gradient


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

    def paint(self,  sun_pos: int,  display_controller: DisplayController):
        self.draw_gradient_at(sun_pos, display_controller)

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
            if elapsed_ms >= self.time_waiting_until:
                self.time_waiting_until = 0
            return

        self.percent_pulse += self.target_inc
        if self.percent_pulse >= 100:
            self.percent_pulse = 100
            self.target_inc = -self.target_inc
            if self.time_waiting_until == 0:
                self.time_waiting_until = elapsed_ms + self.time_high_ms

        elif self.percent_pulse < 0:
            self.percent_pulse = 0
            self.target_inc = -self.target_inc
            if self.time_waiting_until == 0:
                self.time_waiting_until = elapsed_ms + self.time_low_ms
