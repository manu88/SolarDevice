import datetime
import random

from ephem import hour


class SharedPacket :
    '''
    The data shared with the software among all different module
    '''
    def __init__(self ):
        self.date = None ## F -> Heure actuelle en format date time
        
        ## BMS 
        self.charge_batterie_pourcent = 0 ## A -> Charge de la batterie (pourcentage) en Watt 
        self.power_input_watt = 0 ## B -> Irradiance solaire en Watt
        self.power_output_watt = 0 ## B -> Irradiance solaire en Watt
        self.consommation_charge_watt = 0 ## C => consommation charge en watt

        ## meteo module 
        self.nebulosite_actuelle = 0 ##  D -> en pourcent de 0 a 100  E
        self.nebulosite_lendemain = 0 ##  D -> en pourcent de 0 a 100  E
        
        #horloge 
        self.lever_soleil = None ##  Éphéméride
        self.coucher_soleil = None ##  Éphéméride
        
        self.lever_soleil_lendemain = None ##  Éphéméride
        self.coucher_soleil_lendemain = None ##  Éphéméride

        # capteur effet hall
        self.vitesse_mendocinos_rpm = [] ## X moteurs
        return

    def is_day_packet(self) -> bool : 
        return self.lever_soleil <= self.date <= self.coucher_soleil
    
    def get_tomorrow_sunlight_duration_sec(self) -> int :
        next_day_sun_sec = (self.coucher_soleil_lendemain - self.lever_soleil_lendemain).total_seconds()
        if next_day_sun_sec <= 0 :
            return 0
        brightness = (100.0 - self.nebulosite_lendemain) / 100.0 
        if brightness <= 0 :
            brightness = 0
        return round(brightness * next_day_sun_sec, 0)

    def get_tomorrow_sunlight_duration_min(self)  -> int :
        return round(self.get_tomorrow_sunlight_duration_sec() / 60, 0)

    def get_tomorrow_sunlight_duration_hour(self) -> float  :
        return round(self.get_tomorrow_sunlight_duration_sec() / 3600, 2)

    def clone(self) :
        clone = SharedPacket()

        ## BMS 
        clone.charge_batterie_pourcent = self.charge_batterie_pourcent
        clone.power_input_watt = self.power_input_watt
        clone.power_output_watt = self.power_output_watt
        clone.consommation_charge_watt = self.consommation_charge_watt

        ## meteo module 
        clone.nebulosite_actuelle = self.nebulosite_actuelle
        clone.nebulosite_lendemain = self.nebulosite_lendemain

        #horloge 
        clone.date = self.date
        clone.lever_soleil = self.lever_soleil
        clone.coucher_soleil = self.coucher_soleil
        
        clone.lever_soleil_lendemain = self.lever_soleil_lendemain
        clone.coucher_soleil_lendemain = self.coucher_soleil_lendemain

        # capteur effet hall, reproduit le vecteur
        clone.vitesse_mendocinos_rpm = []
        for ar in self.vitesse_mendocinos_rpm :
            new_v_array = []
            for v in ar : 
                new_v_array.append(v)
            clone.vitesse_mendocinos_rpm.append(new_v_array)
        return clone


    def get_speed_mean(self) :
        total = 0
        number = 0
        for ar in self.vitesse_mendocinos_rpm :
            for v in ar : 
                total += v
                number += 1
        if number == 0 :
            return -1
        return total / number