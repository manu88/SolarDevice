import serial
from typing import Dict
import traceback
import time
from threading import Thread
from sensor_reader import SensorReader
from osc_server_interface import OSCServerInterface


class SecondaryController:
    def __init__(self, serial_ports: list[str]) -> None:
        self.osc_server: OSCServerInterface = None
        self.sensors = SensorReader()
        self._should_stop = False

        self.arduinos: Dict[str, serial.Serial] = dict()
        for ports in serial_ports:
            arduino = serial.Serial(
                port=ports, baudrate=115200, timeout=.1)
            self.arduinos[ports] = arduino
        self.board_ids: Dict[int, serial.Serial] = dict()

        self.read_thread = Thread(target=self._run_thread)

    def start(self):
        self.read_thread.start()

    def _run_thread(self):
        print("SecondaryController: start thread")
        while self._should_stop is False:
            for arduino in self.arduinos.values():
                self._check_arduino(arduino)

    def send_motor(self, board_id: int, motor_id: int, duration: int):
        if board_id not in self.board_ids:
            return
        arduino = self.board_ids[board_id]
        cmd = f"{motor_id+1};{duration}\n"
        arduino.write(cmd.encode())

    def _process_arduino_msg(self, arduino: serial.Serial, l: str):
        line = l.strip()
        # print(f"received '{line}'")
        if line.startswith("BoardId="):
            board_id = int(line[8:])
            print(f"Board id is {board_id}")
            self.board_ids[board_id] = arduino
            print(f"setting arduino at {arduino.port} as board id {board_id}")
        elif line.startswith("S") and len(line) > 2 and line[0].isdigit:
            received_idx = self.sensors.on_sensor_line(line)
            for idx in received_idx:
                self.osc_server.send_sensor(
                    idx, self.sensors.sensors[idx], self.sensors.is_rotating[idx])

    def read_arduino_msg(self, arduino: serial.Serial) -> bool:
        ret = False
        if arduino.in_waiting:
            lines = arduino.readlines()
            if len(lines) > 0:
                ret = True
            if len(lines):
                for l in lines:
                    try:
                        self._process_arduino_msg(arduino, l.decode())
                    except Exception as err:
                        print(err)
                        print(traceback.format_exc())

        return ret

    def _check_arduino(self, arduino: serial.Serial):
        received_nothing_count = 0

        received_something = self.read_arduino_msg(arduino)
        if received_something:
            received_nothing_count = 0
        else:
            received_nothing_count += 1
            if received_nothing_count > 3:
                print("-> Reopen arduino")
                # with self.arduino_lock:
                #    self.arduino.close()
                #    self._open_arduino()
                print("<- Done Reopen arduino")

            time.sleep(1)
