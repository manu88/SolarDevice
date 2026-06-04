import struct
import time
from threading import Thread
import serial
from serial import serialutil
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


payload_size = 72


def checksum(data):
    ret = 0
    for d in data:
        ret += d
        if ret >= 0XFFFF:
            ret = 0
    return ret


class Controller:
    def __init__(self, serial_port: str):
        self.arduino = serial.Serial(
            port=serial_port, baudrate=115200, timeout=.1)

        self._should_stop = False
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
        crc = checksum(payload)
        data_header = struct.pack(self.pack_com_str, 0XAF, len(payload))
        try:
            self.arduino.write(data_header)
            self.arduino.write(payload)
        except serialutil.SerialException as e:
            print(f"send_payload:SerialException {e}")
            self.stop()

    def _process_arduino_msg(self, l: str):
        print(l)

    def read_arduino_msg(self):
        lines = self.arduino.readlines()
        if len(lines):
            for l in lines:
                self._process_arduino_msg(l.decode())

    def start(self):
        print("Serving on {}".format(self.server.server_address))
        self.read_thread.start()
        self.server.serve_forever()

    def stop(self):
        print("Stopping")
        self._should_stop = True
        self.server.shutdown()
        self.read_thread.join()
        self.arduino.close()

    def _run_thread(self):
        while self._should_stop is False:
            self.read_arduino_msg()
            time.sleep(1)
        print("Read thread returned")
