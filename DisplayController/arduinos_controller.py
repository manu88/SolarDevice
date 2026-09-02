import serial
from typing import Dict, Set
import traceback
import time
from threading import Thread
from sensor_reader import SensorReader
from osc_server_interface import OSCServerInterface
from display_controller import DisplayController

BAUD_RATE = 115200


class ArduinosController:
    def __init__(self, display_ctrl: DisplayController, serial_ports: list[str]) -> None:
        self.display_ctrl = display_ctrl
        self.osc_server: OSCServerInterface = None
        self.sensors = SensorReader()
        self._should_stop = False

        self.arduinos_to_remove_from_list: Set[str] = set()
        self.arduino_ports_to_open: Set[str] = set()
        self.arduinos: Dict[str, serial.Serial] = dict()
        for port in serial_ports:
            self.arduino_ports_to_open.add(port)
        self.board_ids: Dict[int, serial.Serial] = dict()

        self.read_thread = Thread(target=self._run_thread)

    def stop(self):
        self._should_stop = True
        print("Stopping arduinos controller")
        self.read_thread.join()

    def start(self):
        self.read_thread.start()

    def send_motor(self, board_id: int, motor_id: int, duration: int):
        if board_id not in self.board_ids:
            return
        arduino = self.board_ids[board_id]
        if board_id == 0:
            self.display_ctrl.send_motor(
                motor_id=motor_id+1, duration=duration)
            return
        cmd = f"{motor_id+1};{duration}\n"
        arduino.write(cmd.encode())

    def _process_arduino_msg(self, arduino: serial.Serial, l: str):
        line = l.strip()
        # print(f"received '{line}'")
        if line.startswith("BoardId="):
            board_id = int(line[8:])
            print(f"Board id is {board_id}")
            self.board_ids[board_id] = arduino
            if (board_id == 0):
                print(
                    f"Setting display controller to arduino at {arduino.port}")
                self.display_ctrl.arduino = arduino
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

    def get_board_id_from_arduino(self, arduino: serial.Serial) -> int:
        for key, val in self.board_ids.items():
            if val == arduino:
                return key
        return -1

    def _check_arduino(self, arduino: serial.Serial):
        try:
            self.read_arduino_msg(arduino)
        except OSError as e:
            board_id = self.get_board_id_from_arduino(arduino)
            print(
                f"Got OSError {e} for boar_id={board_id} port={arduino.port}")
            if board_id != -1:
                self._remove_board(board_id, arduino)

    def _remove_board(self, board_id: int, arduino: serial.Serial):
        print(
            f"remove port={arduino.port} boar_id={board_id} from board_ids")
        del self.board_ids[board_id]
        if board_id == 0:
            self.display_ctrl.arduino = None
        print(f"Add {arduino.port} to open list")
        self.arduino_ports_to_open.add(arduino.port)
        self.arduinos_to_remove_from_list.add(arduino.port)

    def _try_open(self, port: str) -> bool:
        print(f"Try reopen {port}")
        try:
            arduino = serial.Serial(
                port=port, baudrate=BAUD_RATE, timeout=.1)
        except Exception:
            return False
        self.arduinos[port] = arduino
        return True

    def _try_reopen_closed(self):
        ok_list = []
        for port in self.arduino_ports_to_open:
            if self._try_open(port):
                ok_list.append(port)
        for port in ok_list:
            self.arduino_ports_to_open.remove(port)

    def _handle_closed(self):
        for port in self.arduinos_to_remove_from_list:
            del self.arduinos[port]
        self.arduinos_to_remove_from_list.clear()

    def _run_thread(self):
        print("SecondaryController: start thread")
        while self._should_stop is False:
            self._try_reopen_closed()

            for arduino in self.arduinos.values():
                self._check_arduino(arduino)

            self._handle_closed()

            time.sleep(1)

        print("Cleanup")
        for arduino in self.arduinos.values():
            arduino.close()
