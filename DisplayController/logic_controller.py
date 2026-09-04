from threading import Thread, Lock
import time
from enum import Enum
from display_controller import DisplayController
from anims import PulsedGradient, WelcomeAnim, Pulse


class AnimState(Enum):
    UNDEFINED = 0
    WELCOME_ANIM = 1
    PULSES = 2
    ON_THE_CLOCK = 3


class LogicController:
    def __init__(self, display_controller: DisplayController) -> None:
        self.display_controller = display_controller
        self.thread = Thread(target=self._run)
        self._should_run = False
        self.anim_state = AnimState.UNDEFINED
        self.anim_start_started_at_ms = 0
        self.next_state = AnimState.ON_THE_CLOCK
        self.update_delay_ms = 40
        self.welcome_anim = WelcomeAnim()
        self.pulse_anim = PulsedGradient()
        self.clock_anim = Pulse(num_periods=3)

        self.sun_pos: int = 0
        self.update_lock = Lock()

    def start(self):
        self._should_run = True
        self.thread.start()

    def stop(self):
        self._should_run = False
        self.thread.join()

    # self.update_lock IS ALREADY LOCKED
    def _check_state(self, elapsed: int):
        if self.anim_state != self.next_state:
            print(
                f"Change state from {self.anim_state} to {self.next_state}")
            self.anim_state = self.next_state
            self.anim_start_started_at_ms = elapsed
            if self.anim_state == AnimState.PULSES:
                self.pulse_anim.reset()

    def _run(self):
        elapsed = 0
        while self._should_run:
            self.display_controller.clear_buffer()
            with self.update_lock:
                self._check_state(elapsed)
                self.update(elapsed)
                self.paint()
            self.display_controller.update_display()
            time.sleep(self.update_delay_ms/1000)
            elapsed += self.update_delay_ms
        print("logic returned")

    # self.update_lock IS ALREADY LOCKED
    def paint(self):
        if self.anim_state == AnimState.WELCOME_ANIM:
            self.welcome_anim.paint(display_controller=self.display_controller)
        elif self.anim_state == AnimState.ON_THE_CLOCK:
            self.clock_anim.paint(display_controller=self.display_controller)
        elif self.anim_state == AnimState.PULSES:
            self.pulse_anim.paint(sun_pos=self.sun_pos,
                                  display_controller=self.display_controller)
        else:
            print(f"paint: Undefined anim state {self.anim_state}")

    # self.update_lock IS ALREADY LOCKED
    def update(self, elapsed_ms):
        if self.anim_state == AnimState.WELCOME_ANIM:
            if self.welcome_anim.update(elapsed_ms):
                print("Welcom anim done")
                self.next_state = AnimState.PULSES
                self.welcome_anim.reset()
        elif self.anim_state == AnimState.ON_THE_CLOCK:
            if self.clock_anim.update(elapsed_ms):
                print("CLOCK ANIM Done")
                self.next_state = AnimState.PULSES
                self.clock_anim.reset()
        elif self.anim_state == AnimState.PULSES:
            self.pulse_anim.update(elapsed_ms)
        else:
            print(
                f"update: Undefined anim state {self.anim_state}, resetting to PULSES")
            self.next_state = AnimState.PULSES

    def set_grad_size(self, size: int):
        with self.update_lock:
            self.pulse_anim.set_size(size)

    def set_grad_color(self, typ: int, r: float, g: float, b: float):
        with self.update_lock:
            if typ == 0:
                self.pulse_anim.set_start_color(int(r), int(g), int(b))
            elif typ == 1:
                self.pulse_anim.set_mid_color(int(r), int(g), int(b))
            elif typ == 2:
                self.pulse_anim.set_end_color(int(r), int(g), int(b))

    def set_pulse_times(self, high: float, low: float):
        with self.update_lock:
            self.pulse_anim.set_pulse_times(int(high), int(low))

    def set_next_state(self, anim_state: int):
        with self.update_lock:
            self.next_state = AnimState(anim_state)
