import struct
import time
import os
from typing import Optional
import serial
from serial import serialutil
from ui import UILeds
import signal


payload_size = 78


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
        if self.arduino is None:
            return
        self._send_arduino(cmd=0XBC, buffer=buffer)
