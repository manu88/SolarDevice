import struct
import time
import os
from typing import Optional
import serial
from serial import serialutil
from ui import UILeds
import signal


payload_size = 72


def checksum(data) -> int:
    ret: int = 0
    for d in data:
        ret = (ret+d) % 256
    return ret


class DisplayController:
    def __init__(self,  ui: Optional[UILeds] = None):
        self.min_ms_between_updates = 10
        self.ui = ui
        self.arduino: Optional[serial.Serial] = None
        self._should_stop = False
        self.pack_com_str = ">BBB"

        self.buffer1 = [0 for i in range(payload_size)]

        self.last_update_time = time.time()
        self.update_time_accum = 0
        self.num_updates = 0
        self.num_dropped_updates = 0
        signal.signal(signal.SIGTERM, self._on_sigterm)

    def _on_sigterm(self, signum, frame):
        print("Received SIGTERM, clear display")
        self.clear_buffer()
        self.update_display()
        os.kill(os.getpid(), signal.SIGKILL)

    def set_pix1(self, i: int, r: int, g: int, b: int):
        if i*3 >= len(self.buffer1):
            return
        # reverse order because strip is counter clockwise and offset from 0/noon
        i = (33-i) % 24
        self.buffer1[i*3] = r
        self.buffer1[(i*3)+1] = g
        self.buffer1[(i*3)+2] = b

    def clear_buffer(self):
        self.buffer1 = [0 for i in range(payload_size)]

    def set_all(self, r: int, g: int, b: int):
        for i in range(payload_size//3):
            self.buffer1[i*3] = r
            self.buffer1[(i*3)+1] = g
            self.buffer1[(i*3)+2] = b

    def _send_arduino(self, cmd: int, buffer):
        if self.arduino is None:
            return
        crc: int = checksum(buffer)
        assert 0 <= crc < 256

        data_header = struct.pack(
            self.pack_com_str, 0XAF, cmd, len(buffer))
        try:
            msg = data_header + bytes(buffer) + bytes([crc])
            self.arduino.write(msg)

        except serialutil.SerialException as e:
            print(f"send_payload:SerialException {e}")

    def send_motor(self, motor_id: int, duration: int):
        b0, b1 = duration.to_bytes(2)
        buf = [motor_id, 0, b1, b0]
        self._send_arduino(cmd=0XAF, buffer=buf)

    def update_display(self):
        buffer = self.buffer1

        update_time = time.time()
        diff = update_time - self.last_update_time
        if diff < self.min_ms_between_updates/1000:
            self.num_dropped_updates += 1
            return
        self.last_update_time = update_time
        self.update_time_accum += diff
        self.num_updates += 1

        if self.ui:
            self.ui.update_buff(buffer)
        self._send_arduino(cmd=0XBC, buffer=buffer)

    def dump(self):
        print("Buffer1:")
        for i in range(payload_size//3):
            print(
                f"{i}: r={self.buffer1[i*3]} g={self.buffer1[(i*3)+1]} b={self.buffer1[(i*3)+2]}")
        avg = self.update_time_accum / self.num_updates if self.num_updates != 0 else 0
        print(f"{self.num_updates} updates -> {avg*1000}ms")
        print(f"{self.num_dropped_updates} dropped updates | min_ms_between_updates={self.min_ms_between_updates} ms ")
        dropped_percent = 0
        if self.num_updates:
            dropped_percent = self.num_dropped_updates/self.num_updates
        print(f"dropped msg %: {dropped_percent*100:0.1f}%")

    def dump_arduino(self):
        if self.arduino:
            self._send_arduino(cmd=0XBD, buffer=[0])
