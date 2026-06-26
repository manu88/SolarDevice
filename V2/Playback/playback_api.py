import sys
import math
import datetime
from Logic import SharedPacket
from ManagerModule import ManagerModule
import os
import time
from record_helper import record_helper
from SharedPacketHelper import SharedPacketHelper
# ─────────────────────────────────────────────────────────────────────────────
# API utilisant ephem directement
# ─────────────────────────────────────────────────────────────────────────────
class PlaybackApi(ManagerModule) :
    def __init__(self, starting_date: datetime.datetime, speed : float) :
        super().__init__(0)
        self.__speed = speed
        self.__startDate = starting_date
        self.__currentFilePath = ""
        self.__currentEntries = []
        return


    def on_start(self):
        print("PLAYBACK INIT :")
        print(f"\tStarting date : {self.__startDate}sec")
        print(f"\tSpeed: {self.__speed}sec")
        self.__startingTime_s = time.time()
        return

    def get_closest_packet(self) :
        return

    def on_update(self, packet_to_share):
        return

    def get_current_recorded_packet(self) -> SharedPacket :
        date_to_read = self.__get_current_date_to_read()
        filepath = record_helper.get_shared_packet_filepath_from_date(date_to_read)
        if filepath is None : 
            return None
        if filepath != self.__currentFilePath : 
            try : 
                self.__currentEntries = SharedPacketHelper.load_packets(filepath)
                self.__currentFilePath = filepath
            except : 
                return None
        ## get the closest entry 
        return PlaybackApi.__get_closest_date_entry_from_array(self.__currentEntries, date_to_read)

    def __get_current_date_to_read(self):
        dt_s = (time.time() - self.__startingTime_s) * self.__speed
        return self.__startDate + datetime.timedelta(seconds=dt_s)

    def __get_closest_date_entry_from_array(array:list[SharedPacket], date_to_look : datetime.datetime) -> SharedPacket :
        candidates = [obj for obj in array if obj.date < date_to_look]
        if not candidates:
            return None
        return max(candidates, key=lambda obj: obj.date)


    