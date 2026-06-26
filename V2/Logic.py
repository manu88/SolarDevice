import json
import datetime
import random
import requests
import time

from ManagerModule import ManagerModule
from SharedPacket import SharedPacket
##to receive the data from the bms
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client
import Logic_calcul

# ─────────────────────────────────────────────────────────────────────────────
# Réponse complète de l'API (ensemble d'entrées)
# ─────────────────────────────────────────────────────────────────────────────
class Logic(ManagerModule) :
    def __init__(self, config):
        super().__init__(refresh_rate_s = 0)


        self.__config = config

        self.__ip = config["pure_data"]["ip"]
        self.__port = config["pure_data"]["port"]

        self.__sendAllRefreshRate_s = config["pure_data"]["resend_all_every_sec"]

        self.print_data_output = config["pure_data"]["debut_print_osc"]


        self.__lastPacket = SharedPacket()        

        self.__lastLuminosity = -1
        self.__lastDutyCycleHigh_s = 0
        self.__lastDutyCycleLow_s = 4
        self.__lastResendAll_s = 0
        self.__lastDayIndex = -1
        self.__sender = udp_client.SimpleUDPClient(self.__ip, self.__port, allow_broadcast=True)

        return



    def on_start(self):
        print(f"LOGIC INIT :")
        print(f"\tPure data target : {self.__ip}:{self.__port}")
        return


    def __sendData(self , address , payload ): 
        try :
            self.__sender.send_message(address , payload)
            if self.print_data_output == True :        
                print(f"Send to {self.__ip}:{self.__port}: {address} : {payload}")
        except :
            pass
        return

    def on_update(self, packet_to_share):        
        t_s = time.time()
        if (t_s - self.__lastResendAll_s > self.__sendAllRefreshRate_s) : 
            self.__lastResendAll_s = t_s 
            self.__sendAllValues(packet_to_share)
        else :
            self.__send_all_different_value(packet_to_share)

        ## store the old packet
        self.__lastPacket = packet_to_share.clone()
        return

    def __sendAllValues(self, packet_to_share : SharedPacket) :
        
        self.__lastLuminosity = Logic_calcul.get_luminosity_from_packet(self.__config , packet_to_share)
        self.__sendData("/luminosity", self.__lastLuminosity )
        
        self.__lastDutyCycleHigh_s, self.__lastDutyCycleLow_s = self.__get_duty_cycle_low_high(packet_to_share)   
        self.__sendData("/duty_cycle", [int(self.__lastDutyCycleHigh_s * 1000) ,  int(self.__lastDutyCycleLow_s * 1000)] )

        self.__sendData("/nebulosity", round(packet_to_share.nebulosite_actuelle / 100.0 , 2) )
        self.__sendData("/clock", [packet_to_share.date.hour, packet_to_share.date.minute] )

        self.__lastDayIndex = Logic_calcul.get_day_index_from_packet(self.__config , packet_to_share)
        self.__sendData("/day", self.__lastDayIndex ) ## a definir

        if ( len(packet_to_share.vitesse_mendocinos_rpm) > 0 ) :
            sensor_idx = 0
            for array in packet_to_share.vitesse_mendocinos_rpm :
                for rpm in array : 
                    self.__sendData("/sensor", [sensor_idx, rpm])
                    sensor_idx +=1
        return

    def __get_duty_cycle_low_high(self, packet_to_share : SharedPacket ):
        duty_cycle_s = Logic_calcul.get_duty_cycle_duration_from_packet(self.__config , packet_to_share)
        duty_cycle_fill = Logic_calcul.get_duty_cycle_fill_rate_from_packet(self.__config , packet_to_share)
        high = duty_cycle_s * duty_cycle_fill
        if high < 0.3 :
            high = 0.3
        ## can never be under 0.3, if under mean luminosity == 0, managed into the pure data
        low = duty_cycle_s - high
        if low < 0.3 :
            low = 0.3
        return high , low

    def __send_all_different_value(self, packet_to_share : SharedPacket) :
        ## luminosité entre 0 et 1 je fais ma tambouille entre meteo et entrée batterie
        ## METEO
        lum = Logic_calcul.get_luminosity_from_packet(self.__config , packet_to_share)
        if (lum != self.__lastLuminosity) :
            self.__lastLuminosity = lum
            self.__sendData("/luminosity", lum )

        duty_high_s, duty_low_s = self.__get_duty_cycle_low_high(packet_to_share)        
        if (duty_high_s != self.__lastDutyCycleHigh_s or duty_low_s != self.__lastDutyCycleLow_s) :
            self.__lastDutyCycleHigh_s = duty_high_s
            self.__lastDutyCycleLow_s = duty_low_s
            self.__sendData("/duty_cycle", [int(duty_high_s * 1000) ,  int(duty_low_s * 1000)] )

        day_index = Logic_calcul.get_day_index_from_packet(self.__config , packet_to_share)
        if day_index != self.__lastDayIndex :
            self.__sendData("/day", round(packet_to_share.nebulosite_actuelle / 100.0, 2))
            self.__lastDayIndex = day_index

        if self.__lastPacket.nebulosite_actuelle != packet_to_share.nebulosite_actuelle :
            self.__sendData("/nebulosity", round(packet_to_share.nebulosite_actuelle / 100.0, 2))
        ## Horloge
        ## heure actuel pas besoin 
        if self.__lastPacket.date.minute != packet_to_share.date.minute:
            self.__sendData("/clock", [packet_to_share.date.hour, packet_to_share.date.minute] )


        ## ou vitesse par capteur
        old_vm_rpm = self.__lastPacket.vitesse_mendocinos_rpm
        new_vm_rpm = packet_to_share.vitesse_mendocinos_rpm        
        sensor_idx = 0
        for arduino_index in range (0, len(new_vm_rpm)) :
            ## one array by arduino
            for rpm_index in range (0,len(new_vm_rpm[arduino_index])) :
                ## one value by sensor
                ## if value doesn't exist or different than the last one we send it
                if arduino_index >= len(old_vm_rpm) or \
                rpm_index >= len (old_vm_rpm[arduino_index]) or \
                old_vm_rpm[arduino_index][rpm_index] != new_vm_rpm[arduino_index][rpm_index]:
                    self.__sendData("/sensor", [sensor_idx, new_vm_rpm[arduino_index][rpm_index]])

                sensor_idx += 1
        return

    ###########################################
    ###########################################
    ###########################################
