from Arduino.arduino_api import ArduinoApi
import serial
import time
    

class EffetHallApi(ArduinoApi) :
    def __init__(self,shared_packet_array_index, port_com, baudrate=9600, timeout=1 ):
        super().__init__(port_com, baudrate, timeout)
        self.__lastRpmArray = []
        self.__sharedArrayIndex = shared_packet_array_index
        return
    
    def on_start(self) :
        print(f"HALL SENSOR INIT  :")
        print(f"\tport com : {self.PortCom}")
        print(f"\tbaud rate : {self.BaudRate}")
        return

    def on_data_receive(self, orders , payload):        
        if orders == "RPM" and len(payload) >= 1 :
            rpm = []
            for i in range (0,len(payload)) :
                try :
                    value = float(payload[i])
                    rpm.append(round(value, 2))
                except Exception as e:
                    rpm.append(-1)
                    pass

            self.__lastRpmArray = rpm
        return
    

    def on_disconnect(self):
        for i in range(0,len(self.__lastRpmArray)) :
            self.__lastRpmArray[i] = -1
        return

    def on_update(self, shared_packet) :
        super().on_update(shared_packet)
        shared_packet.vitesse_mendocinos_rpm[self.__sharedArrayIndex] = self.__lastRpmArray
        return