import sys
import serial


class SensorReader:
    def __init__(self) -> None:
        self.sensors = [0.0 for i in range(12)]

    def on_sensor_line(self, line: str):
        # print(line)
        toks = line.split(" ")
        if len(toks) != 4:
            print(f"Skipping '{line}': {len(toks)}")
            return
        if toks[0][0] != "S":
            print(f"Skipping '{line}': invalid start")
        board_id = int(toks[0][1:])
        v0, v1, v2 = toks[1:]
        idx_start = board_id * 3
        self.sensors[idx_start] = float(v0)
        self.sensors[idx_start+1] = float(v1)
        self.sensors[idx_start+2] = float(v2)
        print(self.sensors)


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
