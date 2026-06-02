import struct
import serial
from serial import serialutil
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


payload_size = 72


class Controller:
    def __init__(self, serial_port: str):
        self.arduino = serial.Serial(
            port=serial_port, baudrate=115200, timeout=.1)

        self.pack_com_str = ">BB"

        self.payload = [0 for i in range(payload_size)]

        self.dispatcher = Dispatcher()
        self.dispatcher.map("/pix", self.osc_set_pix)
        self.dispatcher.map("/all", self.osc_set_all)
        self.dispatcher.map("/update", self.osc_update)
        self.server = osc_server.ThreadingOSCUDPServer(
            ("127.0.0.1", 8010), self.dispatcher)

    def set_pix(self,  i: int, r: int, g: int, b: int):
        self.payload[i*3] = r
        self.payload[(i*3)+1] = g
        self.payload[(i*3)+2] = b
        # self.send_payload(self.payload)

    def osc_update(self, args):
        self.send_payload(self.payload)

    def osc_set_all(self, args, r: float, g: float, b: float):
        for i in range(72//3):
            self.payload[i*3] = int(r)
            self.payload[(i*3)+1] = int(g)
            self.payload[(i*3)+2] = int(b)
        # self.send_payload(self.payload)

    def osc_set_pix(self, args, i: int, r: float, g: float, b: float):
        if i*3 >= len(self.payload):
            return
        self.set_pix(i, int(r), int(g), int(b))

    def send_payload(self, payload: list):
        data_header = struct.pack(self.pack_com_str, 0XAF, len(payload))
        try:
            self.arduino.write(data_header)
            self.arduino.write(payload)
        except serialutil.SerialException as e:
            print(f"send_payload:SerialException {e}")
            self.stop()

    def start(self):
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()

    def stop(self):
        print("Stopping")
        self.server.shutdown()
        self.arduino.close()
