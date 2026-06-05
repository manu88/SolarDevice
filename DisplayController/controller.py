import struct
import time
from threading import Thread
from typing import Optional
import serial
from serial import serialutil
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client
from pythonosc import osc_server
from ui import UILeds

payload_size = 72


def checksum(data) -> int:
    ret: int = 0
    for d in data:
        ret = (ret+d) % 256

    return ret


class Controller:
    def __init__(self, serial_port: Optional[str], osc_addr: str, ui: Optional[UILeds] = None):
        self.ui = ui
        self.arduino = None
        if serial_port:
            self.arduino = serial.Serial(
                port=serial_port, baudrate=115200, timeout=.1)

        self._should_stop = False
        self.read_thread = None
        if serial_port:
            self.read_thread = Thread(target=self._run_thread)
        self.pack_com_str = ">BB"

        self.payload = [0 for i in range(payload_size)]

        self.dispatcher = Dispatcher()
        self.dispatcher.map("/ping", self.osc_ping)
        self.dispatcher.map("/pix", self.osc_set_pix)
        self.dispatcher.map("/pix2", self.osc_set_pix2)
        self.dispatcher.map("/all", self.osc_set_all)
        self.dispatcher.map("/clear", self.osc_clear)
        self.dispatcher.map("/dump", self.osc_dump)
        self.dispatcher.map("/update", self.osc_update)
        self.server = osc_server.ThreadingOSCUDPServer(
            ("", 8010), self.dispatcher)

        self.osc_client = udp_client.SimpleUDPClient(
            osc_addr, 8012, allow_broadcast=True)

    def osc_ping(self, args):
        print(f"ping {args}")

    def set_pix(self, i: int, r: int, g: int, b: int):
        self.payload[i*3] = r
        self.payload[(i*3)+1] = g
        self.payload[(i*3)+2] = b

    def osc_update(self, args):
        self.update_display(self.payload)

    def osc_dump(self, args):
        for i in range(72//3):
            print(
                f"{i}: r={self.payload[i*3]} g={self.payload[(i*3)+1]} b={self.payload[(i*3)+2]}")

    def osc_clear(self, args):
        self.set_all(0, 0, 0)
        self.update_display(self.payload)

    def osc_set_all(self, args, r: float, g: float, b: float):
        self.set_all(int(r), int(g), int(b))
        for i in range(72//3):
            self.payload[i*3] = int(r)
            self.payload[(i*3)+1] = int(g)
            self.payload[(i*3)+2] = int(b)

    def set_all(self, r: int, g: int, b: int):
        for i in range(72//3):
            self.payload[i*3] = r
            self.payload[(i*3)+1] = g
            self.payload[(i*3)+2] = b

    def osc_set_pix2(self, args, i: int, r: float, g: float, b: float):
        if i*3 >= len(self.payload):
            return
        self.set_pix(i, int(r), int(g), int(b))
        self.update_display(self.payload)

    def osc_set_pix(self, args, i: int, r: float, g: float, b: float):
        if i*3 >= len(self.payload):
            return
        self.set_pix(i, int(r), int(g), int(b))

    def update_display(self, payload: list):
        if self.ui:
            self.ui.update_buff(payload)
        if self.arduino is None:
            return
        crc: int = checksum(payload)
        assert 0 <= crc < 256
        data_header = struct.pack(self.pack_com_str, 0XAF, len(payload))
        try:
            self.arduino.write(data_header)
            self.arduino.write(payload)
            self.arduino.write(bytes([crc]))
        except serialutil.SerialException as e:
            print(f"send_payload:SerialException {e}")
            self.stop()

    def _process_arduino_msg(self, l: str):
        line = l.strip()
        if line.startswith("S") and len(line) > 2 and line[0].isdigit:
            toks = line.split(" ")
            if len(toks) < 3:
                print(f"malformed sensor str: '{line}'")
                return
            sensor_id = int(toks[0][1:])
            speed = float(toks[1])
            if speed < 3:
                print(f"Got sensor id={sensor_id} speed={speed}")
                self.osc_client.send_message("/sensor", [sensor_id, speed])

        else:
            print(line)

    def read_arduino_msg(self):
        while self.arduino.in_waiting:
            lines = self.arduino.readlines()
            if len(lines):
                for l in lines:
                    self._process_arduino_msg(l.decode())

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
        while self._should_stop is False:
            self.read_arduino_msg()
            time.sleep(1)
        print("Read thread returned")
