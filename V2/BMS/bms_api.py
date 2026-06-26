from ast import Return
from ManagerModule import ManagerModule
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
import time

class BMSApi(ManagerModule) :

    ADDRESS_BATTERY = "/battery" 
    ADDRESS_POWER_INPUT = "/power_input" 
    ADDRESS_POWER_OUTPUT = "/power_output" 
    ADDRESS_MINUTE_REMAINING = "/minute_remaining" 

    def __init__(self, config):
        super().__init__(refresh_rate_s= 0)
        self.__ip = config["bms_api"]["ip"]
        self.__port = config["bms_api"]["port"]

        self.__debug_osc_print = config["bms_api"]["debut_print_osc"]

        self._server = None
        self._thread = None

        self.__battery_percent = -1.0
        self.__power_output_watt = -1.0
        self.__power_input_watt = -1.0

        ## only 60 values done
        ## will check every minute the battery level and store it, we will get the consumption with this value
        self.__check_battery_values_every_X_sec = 60
        self.__lastBatteryCheckValues_s = 0
        self.__battery_consumption_max_size = 120
        self.__consumption_historics = []


        self._dispatcher = dispatcher.Dispatcher()
        if self.__debug_osc_print == True : 
            self._dispatcher.set_default_handler(self._on_message)

        self._dispatcher.map(BMSApi.ADDRESS_BATTERY , self.__on_message_battery)
        self._dispatcher.map(BMSApi.ADDRESS_POWER_INPUT , self.__on_message_power_input)
        self._dispatcher.map(BMSApi.ADDRESS_POWER_OUTPUT , self.__on_message_power_output)
        return
    

    def on_update(self, packet_to_share):
        packet_to_share.charge_batterie_pourcent = self.__battery_percent
        packet_to_share.power_input_watt = self.__power_input_watt
        packet_to_share.power_output_watt = self.__power_output_watt
        #packet_to_share.consommation_charge_watt = self.__consumption_watt
        packet_to_share.consommation_charge_watt = round(self.get_mean_consumptions(),2)

        ## get the mean consumption
        t_s = time.time()
        if (self.__battery_percent > 0 and \
            t_s - self.__lastBatteryCheckValues_s > self.__lastBatteryCheckValues_s) : 
            ## check if the value is different than the last one to register it,
            ## otherwise we don't register it since it won't be usefull to the measurement
            if len(self.__consumption_historics) <= 0 or self.__consumption_historics[-1][1] != self.__battery_percent :
                self.__lastBatteryCheckValues_s = t_s
                self.__consumption_historics.append( (t_s, self.__battery_percent) )
                if (len(self.__consumption_historics) > self.__battery_consumption_max_size) :
                    self.__consumption_historics.pop(0)
        return
    
    def get_mean_consumptions(self) :
        if len(self.__consumption_historics) <= 1 :
            return -1.0

        dt_s = self.__consumption_historics[-1][0] - self.__consumption_historics[0][0]
        d_percent = self.__consumption_historics[-1][1] - self.__consumption_historics[0][1]
        return d_percent / dt_s

    def start(self):
        self._server = osc_server.ThreadingOSCUDPServer(
            (self.__ip, self.__port),
            self._dispatcher
        )

        self._thread = threading.Thread(
            target=self._server.serve_forever,
            daemon=True
        )

        self._thread.start()
        print(f"BMS OSC Listening on {self.__ip}:{self.__port}")
        return

    def on_start(self):
        print(f"BMS INIT :")
        print(f"\tOSC listening on : {self.__ip}:{self.__oscPort}")
        print(f"\tDebug printing : {self.__debug_osc_print}")
        self.start()
        return    
    
    def _on_message(self, address, *args):
        print(f"OSC received and not mapped {args}")
        return
    
    def __on_message_battery(self, address, *args):  
        value = BMSApi.__getFloatFromMessage(args)
        if value >= 0 :
            self.__battery_percent = round(value,2)
        if self.__debug_osc_print == True : 
            print(f"BMS Osc battery value received : {value}")
        return

    def __on_message_power_input(self, address, *args):  
        value = BMSApi.__getFloatFromMessage(args)
        if value >= 0 :
            self.__power_input_watt = round(value,2)
        if self.__debug_osc_print == True : 
            print(f"BMS Osc power input value received : {value}")
        return

    def __on_message_power_output(self, address, *args):  
        value = BMSApi.__getFloatFromMessage(args)
        if value >= 0 :
            self.__power_output_watt = round(value,2)
        if self.__debug_osc_print == True : 
            print(f"BMS Osc power output value received : {value}")
        return

    def __getFloatFromMessage(args) :
        if not args:
            return -1
        value = args[0]
        try:
            return float(value)
        except (ValueError, TypeError):
            return -1
    
    # --------------------------
    # Stop server
    # --------------------------
    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server.server_close()