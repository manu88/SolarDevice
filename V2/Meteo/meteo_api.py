
"""
models.py — Structures de données météo Infoclimat
"""
from pickle import OBJ
from time import timezone
from Meteo import meteo_struct
from Meteo.meteo_struct import EntreeMeteo
import json
import datetime
import requests
from ManagerModule import ManagerModule
from SharedPacket import SharedPacket
import TimestampPrinter
import os
from pathlib import Path
from record_helper import record_helper

# ─────────────────────────────────────────────────────────────────────────────
# Réponse complète de l'API (ensemble d'entrées)
# ─────────────────────────────────────────────────────────────────────────────
class MeteoApi(ManagerModule) :


    BASE_URL = "http://www.infoclimat.fr/public-api/gfs/json"

    def __init__(self, auth, key , coords, update_refresh_rate_sec):
        super().__init__(update_refresh_rate_sec)
        self.__url = f"http://www.infoclimat.fr/public-api/gfs/json?_ll={coords[0]},{coords[1]}&_auth={auth}&_c={key}"
        self.__lastResponse = None
        return

    def get_request_json(self):        
        try:            
            r = requests.get(self.__url, timeout=15)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            print(f"[ERREUR HTTP] {e}")
        except requests.exceptions.ConnectionError:
            print("[ERREUR] Impossible de joindre l'API Infoclimat.")
        except requests.exceptions.JSONDecodeError:
            print("[ERREUR] La réponse n'est pas un JSON valide.")
        return None

    def get_last_data(self) :
        if self.__lastResponse == None :
            return None
        return self.__lastResponse.entree_actuelle()

    def on_start(self):
        print(f"INFOCLIMAT INIT :")
        print(f"\turl : {self.__url}")
        print(f"\tRefresh rate : {self.refresh_rate_s}sec")
        return

    

    def record(self) :  
        try :
            file_path = record_helper.get_meteo_filepath_from_date(datetime.datetime.now())
            meteo_struct.EntreeMeteo.write_array_in_file_path(file_path , self.__lastResponse.entrees)
            print(f"Meteo recorded in {file_path}")
        except Exception as e:
            return
        return   

    def retrieve_response_record_from_date(date):        
        try :            
            previous_file = record_helper.retrieve_meteo_record_filepath_from_date(date)
            if previous_file is not None :                
                with open(previous_file, "r") as f:
                    raw_list = json.load(f)
                entries = [EntreeMeteo.from_dict(item) for item in raw_list]
                return previous_file, entries
        except Exception as e :
            return None , []
        return None , []



    def on_update(self, shared_packet : SharedPacket):
        '''
        Used in the main update loop, will update each value from the internet if possible,
        if not possible will retrieve the last value avaiable
        '''

        last_json = self.get_request_json()
        if (last_json == None) :
            ## get the old data register if not a single entree found
            if self.__lastResponse is None : 
                ## retrieve from the backup folder
                ## not implemented yet
                self.__lastResponse = None 
                self.force_update_on_next = True ## to redo on the next update the request otherwise will wait X sec                
                ## get the backup file 
                file, self.__lastResponse = MeteoApi.retrieve_response_record_from_date(shared_packet.date)
                print(f"WARNING ! Meteo : http request failed, using meteo record from {file}")
            return
        else : 
            self.__lastResponse = meteo_struct.ReponseAPI(last_json)
            self.record()

        ## update the packet 
        current_entry =  self.__lastResponse.entree_actuelle()
        tomorrow_sun_entries = self.__lastResponse.entrees_entre_2_dates(shared_packet.lever_soleil_lendemain, shared_packet.coucher_soleil_lendemain)
        shared_packet.nebulosite_actuelle = round(current_entry.nebulosite.totale, 2)
        if (len(tomorrow_sun_entries) > 0) :
            ## get the tomorrow nebulosity         
            total_nebu = 0
            for t in tomorrow_sun_entries :
                total_nebu += t.nebulosite.totale
            nebu_lendemain = total_nebu / len(tomorrow_sun_entries)
            next_day_sun_sec = (shared_packet.coucher_soleil_lendemain - shared_packet.lever_soleil_lendemain).total_seconds()

            shared_packet.nebulosite_lendemain = nebu_lendemain
        else : 
            shared_packet.nebulosite_lendemain = 0.0

        if self.print_update == True : 
            print("-----------------------------------")
            print("METEO API updated ")
            print(self.__lastResponse)
            print(self.__lastResponse.entree_actuelle())
            print(f"Nebulosite lendemain : {shared_packet.nebulosite_lendemain}")
            print(f"Ensoleillement minute : {shared_packet.get_tomorrow_sunlight_duration_min()}min")
            print("-----------------------------------")
        return