from ManagerModule import ManagerModule
from abc import abstractmethod
import serial
import time
from serial.tools import list_ports
    
def list_all_port_com() :
    ports = list_ports.comports()
    if (ports is None or len(ports) <= 0) :
        print("No port com device connected")
        return

    toprint ="All port com device connected"
    for port in ports:
        toprint += f"\n\t{port.device} - ID : {port.hwid} - {port.description}"
    print(toprint)
    return


class ArduinoApi(ManagerModule) :
    def __init__(self, port_com , baudrate = 9600, timeout = 1):
        super().__init__(refresh_rate_s = 0)

        self.PortCom = port_com
        self.BaudRate = baudrate
        self.Timeout = timeout

        self.serial = None
        self.connected = False

        self.last_order = None
        self.last_payload_0 = None
        self.last_payload_1 = None

        self.__lastError = None
        return
    

    def on_update(self, shared_packet) :
        """
        Reads one full line from serial.
        If error occurs, attempts reconnect and retries once.
        """
        if not self.connected:
            self.connect()
            if not self.connected:
                return

        try:
            line = self.serial.readline().decode("utf-8").strip()
            if not line:
                return  # nothing received
            ### parsing the data
            parts = line.split(";")
            if len(parts) == 1 :
                self.on_data_receive(parts[0], [])
            else :
                self.on_data_receive(parts[0], parts[1:])
            #######################################

        except Exception as e:
            # Any read/parse error -> reconnect and retry once
            print(f"{self.PortCom} - Error: {e}, reconnecting...")
            self.connect()

            try:
                line = self.serial.readline().decode("utf-8").strip()
                if line:
                    self._parse_line(line)
            except Exception as e2:
                print(f"{self.PortCom} - Retry failed: {e2}")
                self.connected = False
                self.on_disconnect()
        return

    
    # -------------------------
    # Connection handling
    # -------------------------

    def connect(self):
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()

            self.serial = serial.Serial(
                self.PortCom,
                self.BaudRate,
                timeout=self.Timeout
            )

            time.sleep(2)  # Arduino reset delay
            self.connected = True
            self.__lastError = ""
            print(f"{self.PortCom} opened")
            self.on_connect()

        except Exception as e:
            self.connected = False
            msg = str(e)
            if self.__lastError != msg :
                self.__lastError = msg
                print(f"{self.PortCom} : Connection failed {msg}")

    def disconnect(self):
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()
        finally:
            self.__lastError = ""
            self.connected = False
            self.on_disconnect()
            print(f"{self.PortCom} Disconnected")

    @abstractmethod
    def on_data_receive(self, order, payload) :
        return
    
    def on_connect(self) :
        return

    def on_disconnect(self) :
        return

    def stop(self): 
        self.disconnect()
        return
    def _build_message(self, order, *args):
        parts = [str(order)] + [str(a) for a in args]
        return ";".join(parts)

    def send_data(self, order , *args) :
        if self.connected == False :
            return False
        try:
            msg = self._build_message(order, *args)
            self.serial.write((msg + "\n").encode("utf-8"))
            return True
        except Exception as e:
            print(f"{self.PortCom} Send error: {e}")
            self.connected = False
            return False
        return False
