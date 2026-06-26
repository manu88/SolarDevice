

import sys
import math
import datetime
import ephem  # pip install ephem
from Logic import SharedPacket
from ManagerModule import ManagerModule


# ─────────────────────────────────────────────────────────────────────────────
# API utilisant ephem directement
# ─────────────────────────────────────────────────────────────────────────────
class EphemerideAPI(ManagerModule) :


    def __init__(self, coords, update_refresh_rate_sec):
        super().__init__(update_refresh_rate_sec)
        self.__coords = coords
        self.__lastData = (None, None , 0)
        return

    def get_ephemeride_soleil(self, date : datetime) :
        soleil = ephem.Sun()
        try:
            obs_lever = ephem.Observer()
            obs_lever.lat, obs_lever.lon = str(self.__coords[0]), str(self.__coords[1])

            obs_lever.date = ephem.Date(datetime.datetime(date.year, date.month, date.day, 0, 0, 0))
            obs_lever.horizon = "-0:34"  # réfraction standard

            lever_sol_utc  = obs_lever.next_rising(soleil).datetime().replace(tzinfo=datetime.timezone.utc)
            coucher_sol_utc = obs_lever.next_setting(soleil).datetime().replace(tzinfo=datetime.timezone.utc)

            lever_sol_loc   = lever_sol_utc.astimezone(date.tzinfo)
            coucher_sol_loc = coucher_sol_utc.astimezone(date.tzinfo)
            duree_jour = coucher_sol_utc - lever_sol_utc
            return (lever_sol_loc, coucher_sol_loc , duree_jour.total_seconds() )
        except ephem.AlwaysUpError:
            lever_sol_loc = coucher_sol_loc = None
        except ephem.NeverUpError:
            lever_sol_loc = coucher_sol_loc = None
        return (None, None , 0)

    def on_start(self):
        print("EPHEMERIDE INIT :")
        print(f"\tRefresh rate : {self.refresh_rate_s}sec")
        return

    def on_update(self, shared_packet : SharedPacket):
        '''
        Used in the main update loop, to get the ephemeride of the next day
        '''
        current_day_lever, current_day_coucher, current_day_sun_sec = self.get_ephemeride_soleil(shared_packet.date)
        
        shared_packet.lever_soleil = current_day_lever 
        shared_packet.coucher_soleil = current_day_coucher

        tomorrow = datetime.datetime.now() +  datetime.timedelta(days=1)
        next_day_lever, next_day_coucher, next_day_sun_sec = self.get_ephemeride_soleil(tomorrow)

        
        shared_packet.lever_soleil_lendemain = current_day_lever 
        shared_packet.coucher_soleil_lendemain = current_day_coucher


        if next_day_lever != self.__lastData : 
            if self.print_update == True : 
                print("-----------------------------------")
                print(f"Ephemeride API updated for date {tomorrow}")
                if (self.__lastData[2] > 0 ) :
                    print(f"Previous sunlight duration : {EphemerideAPI.__seconde_to_hh_mm(self.__lastData[2])}" )
                if (next_day_lever is not None ) :
                    print(f"New sunlight duration : {EphemerideAPI.__seconde_to_hh_mm(next_day_sun_sec)}" )
                else :
                    print(f"New sunlight duration : None" )
                print("-----------------------------------")
            self.__lastData = (next_day_lever, next_day_coucher, next_day_sun_sec )
        return

    def __seconde_to_hh_mm(seconde) :
        minute = seconde / 60
        h = int(minute / 60)
        m = int(minute % 60)
        if h < 10 :
            to_return = f"0{h}:"
        else :
            to_return = f"{h}:"

        if m < 10 :
            to_return += f"0{m}"
        else :
            to_return += f"{m}"
        return to_return