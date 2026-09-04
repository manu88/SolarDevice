from threading import Thread, Lock
import time
import datetime
from enum import Enum
from display_controller import DisplayController
from arduinos_controller import ArduinosController
from anims import PulsedGradient, WelcomeAnim, Pulse
from conf import Config
from osc_server_interface import OSCServerInterface


class AnimState(Enum):
    UNDEFINED = 0
    WELCOME_ANIM = 1
    PULSES = 2
    ON_THE_CLOCK = 3


class MotorChecker:
    def __init__(self, arduinos_controller: ArduinosController) -> None:
        self.arduinos_controller = arduinos_controller
        self.check_every_ms = Config.CHECK_IF_RUNNING_EVERY_MS
        self.last_check_ms = 0
        self.indices_to_check = []
        self._motors_to_start = set()

    def check(self, index: int):
        self._motors_to_start.clear()
        self.indices_to_check = [index]

    def check_all(self):
        self._motors_to_start.clear()
        self.indices_to_check = list(range(12))

    def check_none(self):
        self._motors_to_start.clear()
        self.indices_to_check = []

    def _do_check_motor(self, index: int):
        print(f"_do_check_motor on index {index}")
        speed = self.arduinos_controller.sensors.sensors[index]
        is_rotating = self.arduinos_controller.sensors.is_rotating[index]
        if is_rotating:
            return
        if speed < Config.RESTART_IF_UNDER_SPEED:
            print(f"queuing index={index}")
            self._motors_to_start.add(index)

    def _do_check_motors(self):
        for i in self.indices_to_check:
            self._do_check_motor(i)

    def update(self, elapsed_ms: int):
        if len(self._motors_to_start):
            idx = self._motors_to_start.pop()
            print(f"Restart motor {idx}")
            self.arduinos_controller.set_motor(idx, 500)
        if elapsed_ms - self.last_check_ms >= self.check_every_ms:
            self.last_check_ms = elapsed_ms
            print(f"Time to check motors :{self.indices_to_check}")
            self._do_check_motors()


class LogicController:
    def __init__(self, display_controller: DisplayController, arduinos_controller: ArduinosController) -> None:
        self.osc_server: OSCServerInterface = None
        self.display_controller = display_controller
        self.arduinos_controller = arduinos_controller
        self.thread = Thread(target=self._run)
        self._should_run = False
        self.anim_state = AnimState.UNDEFINED
        self.anim_start_started_at_ms = 0
        self.next_state = AnimState.PULSES
        self.update_delay_ms = Config.LOGIC_FRAME_DURATION_MS
        self.welcome_anim = WelcomeAnim()
        self.pulse_anim = PulsedGradient()
        self.clock_anim = Pulse(num_periods=Config.ON_THE_CLOCK_NUM_PERIODS)
        self.motor_checker = MotorChecker(
            arduinos_controller)

        self.current_hour = datetime.datetime.now().hour
        self.update_lock = Lock()
        self.realtime = True
        self.last_time_sent_sensor = 0
        self.last_time_sent_hour = 0

    def start(self):
        self._should_run = True
        self.thread.start()

    def stop(self):
        self._should_run = False
        self.thread.join()

    def set_use_realtime(self, use_realtime: int):
        with self.update_lock:
            self.realtime = bool(use_realtime)
            print(f"set clockmode realtime={self.realtime}")

    def on_clock(self, hh: int, mm: int):
        with self.update_lock:
            if hh != self.current_hour:
                print(f"Hour changed from {self.current_hour} to {hh}")
                self.current_hour = hh
                # self.motor_checker.check_all()
                self.motor_checker.check_all()
                self.next_state = AnimState.ON_THE_CLOCK

    # self.update_lock IS ALREADY LOCKED
    def _check_state(self, elapsed: int):
        if self.anim_state != self.next_state:
            print(
                f"Change state from {self.anim_state} to {self.next_state}")
            self.anim_state = self.next_state
            self.state_changed()
            self.anim_start_started_at_ms = elapsed
            if self.anim_state == AnimState.PULSES:
                self.pulse_anim.reset()
                self.motor_checker.check(self.current_hour % 12)

    def _run(self):
        elapsed = 0
        while self._should_run:
            # try:
            self.display_controller.clear_buffer()
            with self.update_lock:
                self._check_state(elapsed)
                self.update(elapsed)
                self.paint()
            self.display_controller.update_display()
            time.sleep(self.update_delay_ms/1000)
            elapsed += self.update_delay_ms
        # except Exception as e:
        #    print(f"Got exception in main logic loop: {e}")
        print("logic returned")

    # self.update_lock IS ALREADY LOCKED
    def state_changed(self):
        print(f"NEW STATE {self.anim_state}")
        # if self.anim_state == AnimState.ON_THE_CLOCK:
        #    self.arduinos_controller.set_all(1000)

    # self.update_lock IS ALREADY LOCKED
    def paint(self):
        if self.anim_state == AnimState.WELCOME_ANIM:
            self.welcome_anim.paint(display_controller=self.display_controller)
        elif self.anim_state == AnimState.ON_THE_CLOCK:
            self.clock_anim.paint(display_controller=self.display_controller)
        elif self.anim_state == AnimState.PULSES:
            self.pulse_anim.paint(sun_pos=(self.current_hour % 12)*2,
                                  display_controller=self.display_controller)
        else:
            print(f"paint: Undefined anim state {self.anim_state}")
    # self.update_lock IS ALREADY LOCKED

    def update_on_the_clock(self, elapsed_ms):
        if self.clock_anim.update(elapsed_ms):
            print("CLOCK ANIM Done")
            self.next_state = AnimState.PULSES
            self.clock_anim.reset()

    # self.update_lock IS ALREADY LOCKED
    def send_osc_data(self, elapsed_ms):
        if elapsed_ms - self.last_time_sent_sensor >= Config.SEND_CURRENT_SPEED_EVERY_MS:
            self.last_time_sent_sensor = elapsed_ms
            index_sensor = self.current_hour % 12
            value = self.arduinos_controller.sensors.sensors[index_sensor]
            is_rotating = self.arduinos_controller.sensors.is_rotating[index_sensor]
            self.osc_server.send_current_sensor(
                index_sensor, value, is_rotating)
        if elapsed_ms - self.last_time_sent_hour >= Config.SEND_CURRENT_HOUR_EVERY_MS:
            self.last_time_sent_hour = elapsed_ms
            print("Send hour")
            self.osc_server.send_hour(self.current_hour)

    # self.update_lock IS ALREADY LOCKED
    def update(self, elapsed_ms):
        self.send_osc_data(elapsed_ms)
        self.motor_checker.update(elapsed_ms)
        if self.realtime:
            current_hour = datetime.datetime.now().hour
            if current_hour != self.current_hour:
                print(
                    f"Hour changed from {self.current_hour} to {current_hour}")
                self.current_hour = current_hour
                self.next_state = AnimState.ON_THE_CLOCK
                return
        if self.anim_state == AnimState.WELCOME_ANIM:
            if self.welcome_anim.update(elapsed_ms):
                print("Welcom anim done")
                self.next_state = AnimState.PULSES
                self.welcome_anim.reset()
        elif self.anim_state == AnimState.ON_THE_CLOCK:
            self.update_on_the_clock(elapsed_ms)
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
