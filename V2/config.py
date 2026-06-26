import json
import os
import json_encoder

default_meteo_auth = "ABpXQFMtACICL1ZhBHIGL1gwUmcJfwEmA39VNlwyBHkHZlU4DmsHbFY8VClVegAxWHUPbF1qCDFRMlc3AHIFeQBhVzpTOQBnAmlWMgQ9Bi1YdFIvCTcBJgN%2FVTpcOQR5B2VVNg5qB3tWMVQ0VXsANlhpD25dfQgvUTNXNwBqBWIAYVc7UzMAagJlVjMEKwYtWG1SOwllATgDZlVhXDcEMQdlVWAOaQc3VjlUN1V7ADBYbg9tXWUIMFE6VzQAaAV5AHxXSlNDAH8CLVZ2BGEGdFh2UmcJaAFt"
default_meteo_key = "5843c5d3fb19aea4ac430f5585a78c6d"

DEFAULT_CONFIG = {
    "coordinate": [48.8566, 2.3522], ## paris
    #"coordinate": [48.8566, 2.3522], ## montreuil
    "timezone": "Europe/Paris",
    "record_every_s": 10,

    "pure_data": {   ## communication between port data an I
        "ip": "127.0.0.1",
        "port": 8012,
        "resend_all_every_sec" : 10,
        "debut_print_osc" : True
    },

    "main_arduino": { ## used by pure data
        "port_com": "/dev/ttyACM0",
    },
    
    "hall_sensor_arduino": { ##arduino hall sensor communication
        "port_com": "",
        "baudrate": 9600
    },
    
    "bms_api": {
        "ip": "0.0.0.0",
        "port": 8888,
        "debut_print_osc" : True,
        "power_input_on_230V_watt" : 500,
    },
    
    "info_climat_api": {
        "authentification": default_meteo_auth,
        "key": default_meteo_key,
        "refresh_rate_sec" : 3600
    },
    "ephemeride_api": {
        "refresh_rate_sec" : 3600
    },
    
    "luminosite_scale": {
        "luminosity_on_230V" : 40,
        "power_to_luminosity" : [(0,0) , (200,50) , (300, 100)],
        "current_cloud_reducer" : [(0,0) , (50,10) , (100, 20)], ## percent of reduction, from 0 to 100
        "battery_remaining_reducer" : [(0,0) , (100, 20)], ## percent of reduction, from 0 to 100
        "next_day_sunlight_hour_reducer" : [(0,90) , (4,60) , (8,15) , (12,0), (24, 0)] ## percent of reduction, from 0 to 100
    },    
    
    "duty_cycle_duration_s": {
        "power_to_duration_s" : [(0,4.0) , (200, 2.0) , (300, 0.5)],
        "current_cloud_reducer" : [(0,0) , (50,10) , (100, 20)], ## percent of reduction, from 0 to 100
        "battery_remaining_reducer" : [(0,0) , (50,10) , (100, 20)], ## percent of reduction, from 0 to 100
        "next_day_sunlight_hour_reducer" : [(0,90) , (4,60) , (8,15) , (12,0), (24, 0)] ## percent of reduction, from 0 to 100
    },    
    
    "duty_cycle_fill_percent": {
        "power_to_fill_percent" : [(0,0) , (200,30) , (300, 60)],
        "current_cloud_reducer" : [(0,0) , (50,10) , (100, 20)], ## percent of reduction, from 0 to 100
        "battery_remaining_reducer" : [(0,0) , (50,10) , (100, 20)], ## percent of reduction, from 0 to 100
        "next_day_sunlight_hour_reducer" : [(0,90) , (4,60) , (8,15) , (12,0), (24, 0)] ## percent of reduction, from 0 to 100
    },
    

    "day_slice": {
        "day" : [0 , 40 , 60 , 94, 100],
        "night" :  [0, 100],
        "force_envoie_day" :  -1,
    },
    
    "playback": {
        "activate": False,
        "use_plugged_battery_data": False,
        "starting_date_iso_format" : "2026-07-27T08:00",
        "playback_speed": 1.0
    }
}

def test() :
    data = {
        "points": [[1, 2], [3, 4], [5, 6]],
        "values": [10, 20, 30],
        "name": "my shape",
    }
 
    encoded = json.dumps(DEFAULT_CONFIG, cls=json_encoder.CoordEncoder, indent=2)
    print("Encoded:")
    print(encoded)
 
    decoded = json.loads(encoded, cls=json_encoder.CoordDecoder)
    print("\nDecoded:")
    print(decoded)
    return


def merge_defaults(config, defaults):
    """
    Recursively add missing keys from defaults.
    """
    for key, value in defaults.items():
        if key not in config:
            config[key] = value
        elif isinstance(value, dict) and isinstance(config[key], dict):
            merge_defaults(config[key], value)


def load_config(filepath="config.json"):
    # Create file if it doesn't exist
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, cls=json_encoder.CoordEncoder, indent=2)
        return DEFAULT_CONFIG.copy()

    # Load existing config
    print(f"loading config file from : {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        config = json.load(f , cls=json_encoder.CoordDecoder)

    # Add missing keys
    merge_defaults(config, DEFAULT_CONFIG)

    # Rewrite file if defaults were added
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(config, f, cls=json_encoder.CoordEncoder, indent=2)
    return config
