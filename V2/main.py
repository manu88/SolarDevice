import datetime
import time
from pathlib import Path
import os
import sys

import Logic_calcul
from Playback.playback_api import PlaybackApi
from SharedPacketHelper import SharedPacketHelper
from record_helper import record_helper

from Arduino import arduino_api
from SharedPacket import SharedPacket
import TimestampPrinter
# Override the default print to use the TimestampPrinter
sys.stdout = TimestampPrinter.TimestampPrinter()





'''
The logic is extremly slow, because we don't need any speed,
All the serial com will be read at each loop update, so the refresh rate will be equal to 
MAIN_LOOP_SLEEP_TIME_S
And could be slow down by the other update call of each module.

We have a SharedPacket, which will be created at each loop update and each module will fill it s part
Once everything is filled, it will go into the logic and it will send the correct data to pure data
'''
MAIN_LOOP_SLEEP_TIME_S = 1.0
### loading the config file path
import config
config_file_path = os.path.join(record_helper.ROOT_PATH, "config.init")
#config_json = config.DEFAULT_CONFIG
config_json = config.load_config(config_file_path)




### general parameter
from zoneinfo import ZoneInfo
timezone = ZoneInfo(config_json["timezone"])
coords = config_json["coordinate"]

from Playback import playback_api
playback_mode = config_json["playback"]["activate"]
use_real_battery_data = config_json["playback"]["use_plugged_battery_data"]
date_str = config_json["playback"]["starting_date_iso_format"]
playback_starting_date =  datetime.datetime.fromisoformat(date_str)

playback_speed =  config_json["playback"]["playback_speed"]
PlaybackManager = PlaybackApi( starting_date= playback_starting_date , speed = playback_speed)
PlaybackManager.enable = playback_mode

## EPHEM API USING EPHEM library
from Ephemeride.ephemeride_api import EphemerideAPI
ephemeride_refresh_rate_s = config_json["ephemeride_api"]["refresh_rate_sec"]
EphemerideManager = EphemerideAPI(coords, update_refresh_rate_sec=ephemeride_refresh_rate_s)
EphemerideManager.enable = playback_mode == False ## doesn't use internet, data could not be saved and this enable, but saved and set to False for simplicity
############################

## METEO API USING INFO CLIMAT
from Meteo.meteo_api import MeteoApi
meteo_auth = config_json["info_climat_api"]["authentification"]
meteo_key = config_json["info_climat_api"]["key"]
meteo_refresh_rate_s = config_json["info_climat_api"]["refresh_rate_sec"]

MeteoManager = MeteoApi( meteo_auth, meteo_key , coords, update_refresh_rate_sec=meteo_refresh_rate_s)
MeteoManager.enable = playback_mode == False
###############################

## BMS API library
from BMS.bms_api import BMSApi
BMSManager = BMSApi(config_json)
BMSManager.enable = playback_mode == False or use_real_battery_data == True
############################

## Hall sensor library
from Arduino.effet_hall_api import EffetHallApi
effet_hall_ports_com_raw_text = config_json["hall_sensor_arduino"]["port_com"]
## formated as "COMX COMY"
if effet_hall_ports_com_raw_text != "" and effet_hall_ports_com_raw_text is not None :
    effet_hall_ports_com = effet_hall_ports_com_raw_text.split()
else : 
    effet_hall_ports_com = []

effet_hall_baudrate = config_json["hall_sensor_arduino"]["baudrate"]
ArduinoEffetHallManager = []
if (len(effet_hall_ports_com) == 0) :
    print("No hall sensor in config file")
for i in range (0, len(effet_hall_ports_com)) :
    effet_hall = EffetHallApi(shared_packet_array_index = i, port_com = effet_hall_ports_com[i], baudrate=effet_hall_baudrate )
    effet_hall.enable = playback_mode == False
    ArduinoEffetHallManager.append(effet_hall)
############################


## Logic behind everything
from Logic import Logic
LogicManager = Logic(config_json)
'''
Logique assez basique, une boucle principale updatant chacun des modules gerants la meteo, la bms, et les capteurs a effets hall
Chacun des modules lors de leurs updates vont mettre a jour le packet et le mettre a jour au besoin
'''
## usefull to get all update
## THE ORDER MUST NOT BE CHANGED ! PLAYBACK MUST BE IN FIRST
AllModules = [PlaybackManager , EphemerideManager, MeteoManager, BMSManager] ## ephemeride MUST be before meteo manager
for aefm in ArduinoEffetHallManager : 
    AllModules.append(aefm)

## LOGIC MUST BE AT THE END ! 
AllModules.append(LogicManager)

## DEBUG
# MeteoManager.enable = False
# EphemerideManager.enable = False
record_every_s = config_json["record_every_s"]
last_record_s = 0
######################################


###############
if __name__ == "__main__":
    ## list all port coms : 

    arduino_api.list_all_port_com()
    print("------------------------------------------------\n")

    ## packet used to share every data amon the software
    current_packet_to_share = SharedPacket() 
    ## create the velocity array to store all the value
    v_array =  []
    for i in range (0, len(ArduinoEffetHallManager)):
        v_array.append([])
    current_packet_to_share.vitesse_mendocinos_rpm =v_array
    ###### 

    print("Starting phase")
    for m in AllModules : 
        m.start()
    print("------------------------------------------------\n")
    print("Loop started : ")
    while True : 
        t_s = time.time()
        if playback_mode == False :
            current_packet_to_share.date = datetime.datetime.now(timezone)
        else : 
            current_packet_to_share = PlaybackManager.get_current_recorded_packet()

        ## update all values of each modules
        for m in AllModules : 
            m.update(current_packet_to_share)
        #########################

        ##recording shared packet
        if playback_mode == False and t_s - last_record_s > record_every_s : 
            file_path = record_helper.get_shared_packet_filepath_from_date(current_packet_to_share.date)
            SharedPacketHelper.append_packet(file_path , current_packet_to_share)
            last_record_s = t_s
        #########################
        time.sleep(MAIN_LOOP_SLEEP_TIME_S)
        continue
