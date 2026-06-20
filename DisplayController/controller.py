import struct
import time
from threading import Thread, Lock
from typing import Optional, List
import serial
from serial import serialutil
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client
from pythonosc import osc_server
from ui import UILeds

MIN_VERSION = (0, 0, 6)


def check_firmware_version(ver: str) -> bool:
    v_maj, v_min, v_patch = ver.split(".")
    v_maj = int(v_maj)
    v_min = int(v_min)
    v_patch = int(v_patch)
    print(f"Firmware version: {v_maj}.{v_min}.{v_patch}")
    if v_patch < MIN_VERSION[2] or v_min < MIN_VERSION[1] or v_maj < MIN_VERSION[0]:
        print(
            f"Warning: firmware version is too old, expected {".".join([str(v) for v in MIN_VERSION])}")
        return False
    return True


payload_size = 78


def checksum(data) -> int:
    ret: int = 0
    for d in data:
        ret = (ret+d) % 256

    return ret


def shift(key, array):
    return array[-key:] + array[:-key]


class Controller:
    def __init__(self, serial_port: Optional[str], osc_addr: str, ui: Optional[UILeds] = None):
        self.min_ms_between_updates = 10
        self.ui = ui
        self.arduino = None
        self.serial_port = serial_port
        self.firmware_version: str = ""
        if serial_port:
            self._open_arduino()
            self.arduino_lock = Lock()
        else:
            self.firmware_version = "STUB - no arduino"
        self._should_stop = False
        self.read_thread = None
        if serial_port:
            self.read_thread = Thread(target=self._run_thread)
        self.pack_com_str = ">BBB"

        self.buffer1 = [0 for i in range(payload_size)]

        self.dispatcher = Dispatcher()
        self.dispatcher.map("/ping", self.osc_ping)
        self.dispatcher.map("/pix1", self.osc_set_pix1)
        self.dispatcher.map("/all", self.osc_set_all)
        self.dispatcher.map("/clear1", self.osc_clear1)

        self.dispatcher.map("/dump", self.osc_dump)
        self.dispatcher.map("/update", self.osc_update)
        self.server = osc_server.ThreadingOSCUDPServer(
            ("", 8010), self.dispatcher)

        self.osc_client = udp_client.SimpleUDPClient(
            osc_addr, 8012, allow_broadcast=True)
        self.last_update_time = time.time()
        self.update_time_accum = 0
        self.num_updates = 0
        self.num_dropped_updates = 0
        self.do_test_install = False

    def _open_arduino(self):
        assert (self.serial_port)
        self.arduino = serial.Serial(
            port=self.serial_port, baudrate=115200, timeout=.1)

    def osc_ping(self, args):
        print(f"ping {args}")

    def set_pix1(self, i: int, r: int, g: int, b: int):
        self.buffer1[i*3] = r
        self.buffer1[(i*3)+1] = g
        self.buffer1[(i*3)+2] = b

    def osc_update(self, args):
        self.update_display()

    def osc_dump(self, args):
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
        print(f"firmware version {self.firmware_version}")
        if self.arduino:
            self._send_arduino(cmd=0XBD, buffer=[0])

    def osc_clear1(self, args):
        self.buffer1 = [0 for i in range(payload_size)]

    def osc_set_all(self, args, r: float, g: float, b: float):
        self.set_all(int(r), int(g), int(b))
        for i in range(payload_size//3):
            self.buffer1[i*3] = int(r)
            self.buffer1[(i*3)+1] = int(g)
            self.buffer1[(i*3)+2] = int(b)

    def set_all(self, r: int, g: int, b: int):
        for i in range(payload_size//3):
            self.buffer1[i*3] = r
            self.buffer1[(i*3)+1] = g
            self.buffer1[(i*3)+2] = b

    def osc_set_pix1(self, args, i: int, r: float, g: float, b: float):
        if i*3 >= len(self.buffer1):
            return
        if i == 24:
            self.do_test_install = True
        self.set_pix1(i, int(r), int(g), int(b))

    def _send_arduino(self, cmd: int, buffer):
        with self.arduino_lock:
            crc: int = checksum(buffer)
            assert 0 <= crc < 256

            data_header = struct.pack(
                self.pack_com_str, 0XAF, cmd, len(buffer))
            try:
                msg = data_header + bytes(buffer) + bytes([crc])
                self.arduino.write(msg)

            except serialutil.SerialException as e:
                print(f"send_payload:SerialException {e}")
                self.stop()

    def test_install(self, buffer: List) -> List:
        if self.do_test_install is False:
            return buffer

        self.do_test_install = False
        # Shift the buffer 2 places to make room for 2 leds that mimic the current hour' leds
        led_idx = int(buffer[24*3])
        if led_idx > 26*3:
            return buffer

        for i in range(6):
            buffer[i+24*3] = buffer[i+led_idx*3]

        b = shift(2*3, buffer)

        return b

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

        buffer = self.test_install(buffer)
        if self.ui:
            self.ui.update_buff(buffer)
        if self.arduino is None:
            return
        self._send_arduino(cmd=0XBC, buffer=buffer)

    def _process_arduino_msg(self, l: str):
        line = l.strip()
        if line.startswith("Version:"):
            ver = line.split(" ")[1]
            self.firmware_version = ver
            check_firmware_version(ver)
        if line.startswith("S") and len(line) > 2 and line[0].isdigit:
            toks = line.split(" ")
            if len(toks) < 2:
                print(f"malformed sensor str: '{line}'")
                return
            sensor_id = int(toks[0][1:])
            speed = float(toks[1])
            if speed < 3:
                self.osc_client.send_message("/sensor", [sensor_id, speed])

        else:
            print(line)

    def read_arduino_msg(self) -> bool:
        ret = False
        while self.arduino.in_waiting:
            lines = self.arduino.readlines()
            if len(lines) > 0:
                ret = True
            if len(lines):
                for l in lines:
                    try:
                        self._process_arduino_msg(l.decode())
                    except UnicodeDecodeError as err:
                        print(err)
        return ret

    def start(self):
        print("Serving on {}".format(self.server.server_address))
        if self.read_thread:
            self.read_thread.start()
        self.server.serve_forever()

    def stop(self):
        print("Stopping")
        self._should_stop = True
        self.server.shutdown()
        if self.read_thread:
            self.read_thread.join()
        if self.arduino:
            self.arduino.close()

    def _run_thread(self):
        received_nothing_count = 0
        while self._should_stop is False:
            received_something = self.read_arduino_msg()
            if received_something:
                received_nothing_count = 0
            else:
                received_nothing_count += 1
                if received_nothing_count > 3:
                    print("-> Reopen arduino")
                    with self.arduino_lock:
                        self.arduino.close()
                        self._open_arduino()
                    print("<- Done Reopen arduino")

            time.sleep(1)
        print("Read thread returned")


if __name__ == "__main__":
    assert check_firmware_version("0.0.5") is False
    assert check_firmware_version("0.0.6")
