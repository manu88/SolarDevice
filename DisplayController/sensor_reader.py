import sys
from typing import Dict, Set, List
import time
import serial

MAX_BOARD_TIMEOUT_S = 6
NUM_BOARDS = 4
NUM_SENSORS = 12


class SensorReader:
    def __init__(self) -> None:
        self.sensors = [0.0 for i in range(NUM_SENSORS)]
        self.is_rotating = [0 for i in range(NUM_SENSORS)]
        self.board_ids: Dict[int, float] = {
            0: 0, 1: 0, 2: 0, 3: 0}
        self.unresponsive_boards: Set[int] = set([0, 1, 2, 3])

    def _check_boards_ok(self):
        now = time.time()
        for d_id, last_time in self.board_ids.items():
            delta = now - last_time
            if delta > MAX_BOARD_TIMEOUT_S and d_id not in self.unresponsive_boards:
                print(f"No response from board{d_id}")
                self.unresponsive_boards.add(d_id)

    def dump(self):
        print("Sensors:")
        print(self.sensors)
        print("Unresponsive boards:")
        print(self.unresponsive_boards)

    def on_sensor_line(self, line: str) -> List[int]:
        ret = []
        toks = line.split(" ")
        if len(toks) != 7:
            print(f"Skipping '{line}': {len(toks)}")
            return []
        if toks[0][0] != "S":
            print(f"Skipping '{line}': invalid start")
            return []
        board_id = int(toks[0][1:])
        if board_id < 0 or board_id >= NUM_BOARDS:
            print(f"Invalid board_id {board_id}")
            return []
        self.board_ids[board_id] = time.time()
        if board_id in self.unresponsive_boards:
            print(f"Board {board_id} is back online")
            self.unresponsive_boards.remove(board_id)

        # format float byte float byte float byte
        values = toks[1:]
        if len(values) != 6:
            print(f"expected 6 values, got {len(values)}")
        v0, r0, v1, r1, v2, r2 = toks[1:]
        idx_start = board_id * 3
        if idx_start < 0 or idx_start >= NUM_SENSORS:
            print(f"invalid idx_start {idx_start}")
            return []
        try:
            self.sensors[idx_start] = float(v0)
            self.sensors[idx_start+1] = float(v1)
            self.sensors[idx_start+2] = float(v2)
            self.is_rotating[idx_start] = int(r0)
            self.is_rotating[idx_start+1] = int(r1)
            self.is_rotating[idx_start+2] = int(r2)
            ret.append(idx_start)
            ret.append(idx_start+1)
            ret.append(idx_start+2)
        except ValueError as e:
            print(f"ValueError on board {board_id}: {e}")
        self._check_boards_ok()
        return ret


if __name__ == "__main__":
    arduino = serial.Serial(port=sys.argv[1], baudrate=9600, timeout=.1)
    sensors = SensorReader()
    while True:
        while arduino.in_waiting:
            lines = arduino.readlines()
            for l in lines:
                try:
                    sensors.on_sensor_line(l.decode().strip())
                except UnicodeDecodeError:
                    pass
