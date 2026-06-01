import struct
import serial
import time


arduino = serial.Serial(port='/dev/cu.usbmodem1401',
                        baudrate=115200, timeout=.1)

pack_com_str = ">BB"
pack_recv_str = ">BBB"


def main():
    payload_size = 72  # 24*3
    payload = list(range(payload_size))

    send_payloads = set()
    num_sent = 0
    num_recv = 0
    p_0 = 0
    while True:
        payload[0] = p_0
        print("send payload ", p_0)
        data_header = struct.pack(pack_com_str, 0XAF, payload_size)
        arduino.write(data_header)
        arduino.write(payload)
        send_payloads.add(p_0)
        num_sent += 1

        while arduino.in_waiting:
            resp = arduino.readline().decode()
            print(resp)
#            _, val = resp.strip().split(":")
#            x = int(val, 16)
#            if x in send_payloads:
#                send_payloads.remove(x)
#                num_recv += 1

        percent = num_recv / num_sent
        print(f"sent:{num_sent} recv:{num_recv} {percent:0.2}")
        time.sleep(0.2)
        p_0 += 1
        if p_0 > 256:
            payload = 0


if __name__ == "__main__":
    main()
