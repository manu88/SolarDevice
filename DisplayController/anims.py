from display_controller import DisplayController
from colors import polylinear_gradient
from conf import Config


class WelcomeAnim:
    def __init__(self) -> None:
        self.current_pos = 0
        self.last_change_time = 0
        self.time_to_change = 400
        self.done = False

    def reset(self):
        self.done = False
        self.last_change_time = 0

    def paint(self,  display_controller: DisplayController):
        if not self.done:
            display_controller.set_pix1(self.current_pos, 100, 100, 100)

    def update(self, elapsed_ms: int) -> bool:
        if elapsed_ms - self.last_change_time >= self.time_to_change:
            self.last_change_time = elapsed_ms
            self.current_pos += 1
            if self.current_pos >= 24:
                self.current_pos = 0
                self.done = True
                return True
        return False


class Chenillard:
    def __init__(self) -> None:
        self.current_pos = 0
        self.current_hour = 4
        self.last_change_time = 0
        self.time_to_change = 40
        self.ttl_ms = 1000
        self.start_time = 0
        self.remains = 0
        self.set_ttl(1000)

    def set_ttl(self, ttl: int):
        self.ttl_ms = min(ttl, 1200)
        self.time_to_change = self.ttl_ms/12

    def reset(self, start_time: int):
        self.last_change_time = 0
        self.current_pos = 0
        self.start_time = start_time
        self.remains = self.ttl_ms

    def paint(self, sun_pos: int,  display_controller: DisplayController):
        percent = min(self.remains/(self.ttl_ms*1.5), 1)
        if percent >= 1:
            return
        r = int(Config.CHENILLARD_COLOR[0]*(1-percent)**2)
        g = int(Config.CHENILLARD_COLOR[1]*(1-percent)**2)
        b = int(Config.CHENILLARD_COLOR[2]*(1-percent)**2)
        pix_pos = (sun_pos-self.current_pos) % 24
        display_controller.set_pix1(pix_pos, r, g, b)
        pix_pos = (sun_pos+self.current_pos+1) % 24
        display_controller.set_pix1(pix_pos, r, g, b)

    def update(self, elapsed_ms: int):
        if elapsed_ms - self.last_change_time >= self.time_to_change:
            self.remains = elapsed_ms - self.start_time
            self.last_change_time = elapsed_ms
            self.current_pos += 1
            if self.current_pos >= 24:
                self.current_pos = 0


class Pulse:
    def __init__(self, num_periods: int) -> None:
        self.percent_pulse = 0
        self.time_high_ms = 800
        self.time_low_ms = 300
        self.time_waiting_until = 0
        self.target_inc = 2

        self.current_period = 0
        self.num_periods = num_periods
        self.color = [255, 255, 255]

    def reset(self):
        self.percent_pulse = 0
        self.current_period = 0
        self.time_waiting_until = 0

    def paint(self,  display_controller: DisplayController):
        percent = float(self.percent_pulse/100)
        r = int(self.color[0] * percent)
        g = int(self.color[1] * percent)
        b = int(self.color[2] * percent)
        display_controller.set_all(r, g, b)

    def update(self, elapsed_ms: int) -> bool:
        if self.time_waiting_until > 0:
            if elapsed_ms >= self.time_waiting_until:
                self.time_waiting_until = 0
                if self.percent_pulse == 0:
                    self.current_period += 1
                    return self.current_period >= self.num_periods
            return False

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
        return False


class PulsedAnimation:
    def __init__(self) -> None:
        self.gradient = PulsedGradient()
        self.anim = Chenillard()

    def set_size(self, size: int):
        self.gradient.set_size(size)

    def set_start_color(self, r: int, g: int, b: int):
        self.gradient.set_start_color(r, g, b)

    def set_mid_color(self, r: int, g: int, b: int):
        self.gradient.set_mid_color(r, g, b)

    def set_end_color(self, r: int, g: int, b: int):
        self.gradient.set_end_color(r, g, b)

    def set_day_state(self, day_state: int):
        self.gradient.set_day_state(day_state)

    def reset(self):
        self.gradient.reset()
        self.anim.reset(0)

    def paint(self,  sun_pos: int, sun_val: int, display_controller: DisplayController):
        self.gradient.paint(sun_pos, sun_val, display_controller)
        self.anim.paint(sun_pos, display_controller)

    def update(self, elapsed_ms: int):
        if self.gradient.update(elapsed_ms):
            self.anim.reset(elapsed_ms)
        self.anim.update(elapsed_ms)

    def set_duty_cycle(self, on: int, off: int):
        self.gradient.set_duty_cycle(on, off)
        self.anim.set_ttl(on + off)


class PulsedGradient:
    def __init__(self) -> None:
        self.hide = False
        self.percent_pulse = 0
        self.time_high_ms = 800
        self.time_low_ms = 300
        self.time_waiting_until = 0
        self.target_inc = 8
        self.start_col = [245, 241, 235]  # sun color
        self.mid_col = [105, 96, 254]
        self.end_col = [3, 7, 87]
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=4)
        self.done_sent = False

    def set_duty_cycle(self, on: int, off: int):
        self.time_high_ms = on
        self.time_low_ms = off

    def set_day_state(self, day_state: int):
        colors = Config.GRADIENT_COLORS[day_state]
        self.start_col = colors[0]
        self.mid_col = colors[1]
        self.end_col = colors[2]
        self._rebuild_grad()

    def reset(self):
        self.percent_pulse = 0
        self.time_waiting_until = 0

    def _rebuild_grad(self):
        size = len(self.gradient)
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=size)

    def set_start_color(self, r: int, g: int, b: int):
        self.start_col = [r, g, b]
        self._rebuild_grad()

    def set_mid_color(self, r: int, g: int, b: int):
        self.mid_col = [r, g, b]
        self._rebuild_grad()

    def set_end_color(self, r: int, g: int, b: int):
        self.end_col = [r, g, b]
        self._rebuild_grad()

    def set_size(self, size: int):
        if size == 0:
            self.hide = True
        else:
            self.hide = False
        if size == len(self.gradient):
            return
        self.gradient = polylinear_gradient(
            [self.start_col, self.mid_col,  self.end_col], n=size)

    def paint(self,  sun_pos: int, sun_val: int, display_controller: DisplayController):
        self.draw_gradient_at(sun_pos, sun_val, display_controller)

    def draw_gradient_at(self, start_idx: int, sun_val: int, display_controller: DisplayController):
        percent = float(self.percent_pulse/100)
        if not self.hide:
            for i, color in enumerate(self.gradient):
                r = int(color[0] * percent)
                g = int(color[1] * percent)
                b = int(color[2] * percent)
                sun_0_pos = (start_idx-i) % 24
                sun_1_pos = (start_idx+i+1) % 24
                display_controller.set_pix1(sun_0_pos, r, g, b)
                display_controller.set_pix1(sun_1_pos, r, g, b)
        sun_val = int(percent * sun_val)
        display_controller.set_pix1(start_idx, sun_val, sun_val, sun_val)
        display_controller.set_pix1((start_idx+1) %
                                    24, sun_val, sun_val, sun_val)

    def update(self, elapsed_ms: int) -> bool:
        if self.time_waiting_until > 0:
            if elapsed_ms >= self.time_waiting_until:
                self.time_waiting_until = 0
            return False
        ret = False
        self.percent_pulse += self.target_inc
        if self.percent_pulse > 70 and self.done_sent is False:
            ret = True
            self.done_sent = True
        if self.percent_pulse >= 100:
            self.percent_pulse = 100
            self.target_inc = -self.target_inc
            if self.time_waiting_until == 0:
                self.time_waiting_until = elapsed_ms + self.time_high_ms

        elif self.percent_pulse < 0:
            self.percent_pulse = 0
            self.done_sent = False
            self.target_inc = -self.target_inc
            if self.time_waiting_until == 0:
                self.time_waiting_until = elapsed_ms + self.time_low_ms
        return ret
