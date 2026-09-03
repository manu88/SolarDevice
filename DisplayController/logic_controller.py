from threading import Thread
import time
from display_controller import DisplayController
from colors import linear_gradient, hex_to_rgb


class LogicController:
    def __init__(self, display_controller: DisplayController) -> None:
        self.display_controller = display_controller
        self.thread = Thread(target=self._run)
        self._should_run = False
        self.update_delay_ms = 40
        self.target_val = 0
        self.target_inc = 5
        start_col = "#6E9B15"

        end_col = "#E7164B"
        self.gradient = linear_gradient(
            hex_to_rgb(start_col),  hex_to_rgb(end_col), n=24)
        print(self.gradient)
        assert (len(self.gradient) == 24)

    def start(self):
        self._should_run = True
        self.thread.start()

    def stop(self):
        self._should_run = False
        self.thread.join()

    def _run(self):
        while self._should_run:
            self.display_controller.clear_buffer()
            self.paint()
            self.display_controller.update_display()
            time.sleep(self.update_delay_ms/1000)
        print("logic returned")

    def paint(self):
        self.target_val += self.target_inc
        if self.target_val >= 100:
            self.target_val = 100
            self.target_inc = -self.target_inc
        elif self.target_val < 0:
            self.target_val = 0
            self.target_inc = -self.target_inc
        for i in range(24):
            r = int(self.gradient[i][0] * (self.target_val/100))
            g = int(self.gradient[i][1] * (self.target_val/100))
            b = int(self.gradient[i][2] * (self.target_val/100))
            self.display_controller.set_pix1(i, r, g, b)

    def test_logic(self):
        print("Test logic")
        self.display_controller.clear_buffer()
        if self.target_val == 0:
            self.target_val = 100

        else:
            self.target_val = 0
        self.display_controller.update_display()
