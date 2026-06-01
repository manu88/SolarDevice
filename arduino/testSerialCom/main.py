import struct
import serial
import time


arduino = serial.Serial(port='/dev/cu.usbmodem1401',
                        baudrate=115200, timeout=.1)

pack_com_str = ">BB"
pack_recv_str = ">BBB"
payload_size = 18  # 6*3


def send_payload(payload):
    data_header = struct.pack(pack_com_str, 0XAF, payload_size)
    arduino.write(data_header)
    arduino.write(payload)


def main():

    i = 0
    payload = [0 for i in range(payload_size)]

    while True:
        payload[0] = i
        payload[1] = i
        payload[2] = i

        payload[3] = 255-i
        payload[4] = 255-i
        payload[5] = 255-i

        payload[12] = i
        payload[13] = i
        payload[14] = i

        payload[15] = 255-i
        payload[16] = 255-i
        payload[17] = 255-i
        send_payload(payload)

        while arduino.in_waiting:
            resp = arduino.readline().decode()
            print(resp)
#            _, val = resp.strip().split(":")
#            x = int(val, 16)
#            if x in send_payloads:
#                send_payloads.remove(x)
#                num_recv += 1

        i += 5
        if i >= 256:
            i = 0
        time.sleep(0.1)


if __name__ == "__main__":
    main()
