import struct
import serial
import time


arduino = serial.Serial(port='/dev/cu.usbmodem1401',
                        baudrate=19200, timeout=.1)

pack_com_str = ">BBB"
pack_recv_str = ">BBB"


def main():
    payload = 0
    while True:
        data = struct.pack(pack_com_str, 0XAF, 1, payload)
        print("send", data.hex(sep=" "))
        arduino.write(data)
        time.sleep(1)
        while arduino.in_waiting:
            resp = arduino.readline()
            print(resp)

        payload += 1
        if payload > 256:
            payload = 0


if __name__ == "__main__":
    main()
