from dataclasses import is_dataclass
import json
import datetime
import random
from struct import pack
import requests
import time
from SharedPacket import SharedPacket

def get_linear_regression_from_array(array, current_value_percent) : 
    '''
    Do a linear regression with an array of point [(x_0,y_0),...,(x_i,y_i)]
    '''
    ## if not enought point is given, we return the current value directly and False to indicate the linear reduction didn't work
    if (len(array) <= 1) :
        return False, current_value_percent

    for i in range (1, len(array)) :
        ## first find the 2 couples points around the value
        if array[i-1][0] < current_value_percent < array[i][0]: 
            ## then get the dx / dy of the value
            pt_1 = array[i-1]
            pt_2 = array[i]
            dx = pt_2[0] - pt_1[0]
            dy = pt_2[1] - pt_1[1]
            ## y = a x + b 
            ## where a = dy / dx,  b = pt_1[1]
            return True, (dy / dx) * (current_value_percent - pt_1[0]) + pt_1[1]

    ## if nothing is found mean we are at a maximun
    if current_value_percent <= array[0][0] : 
        return True, array[0][1]
    else : 
        return True, array[-1][1]
    
    
def get_luminosity_from_packet(config_json, packet_to_share : SharedPacket) -> float :
    '''
    Will take the power input and rescale it to a luminosity
    Formula : 
    reducer = cloud_to_luminosity_reducer_converter(cloud_next_3h) * sunlight_duration_tomorrow_reducer_converter(cloud_next_3h)
    power_to_luminosity_converter(current_irradiance) * reduction_ratio
    '''
    power_on_230 = config_json["bms_api"]["power_input_on_230V_watt"]
    if packet_to_share.power_input_watt > power_on_230 :
        ## what do we do here? no idea to fill, for the moment same thing than the other
        to_return = config_json["luminosite_scale"]["luminosity_on_230V"]
    else : 
        lum_array = config_json["luminosite_scale"]["power_to_luminosity"]    
        success_l, luminosity_percent = get_linear_regression_from_array(lum_array, packet_to_share.power_input_watt)
        ## mean issue with the array, we set to 60% by default
        if success_l == False : 
            luminosity_percent = 60.0
        reducer_ratio = get_reducer_from_dict(config_json["luminosite_scale"] , packet_to_share)
        to_return = (luminosity_percent / 100.0) * reducer_ratio
    if to_return < 0.0 :
        to_return = 0.0
    elif to_return >= 1.0 :
        to_return = 1.0
    return round(to_return,2)    

def get_duty_cycle_duration_from_packet(config_json, packet_to_share : SharedPacket) -> float :
    '''
    Will take the power input and rescale it to a duty cycle duration
    Formula : 
    reducer = cloud_to_luminosity_reducer_converter(cloud_next_3h) * sunlight_duration_tomorrow_reducer_converter(cloud_next_3h) * battery_remaning_reducer(remaining_battery)
    power_to_duration(current_irradiance) * (2.0 - reduction_ratio)
    '''
    duty_cycle_array = config_json["duty_cycle_duration_s"]["power_to_duration_s"]    
    success_l, duty_cycle_s = get_linear_regression_from_array(duty_cycle_array, packet_to_share.power_input_watt)
    ## mean issue with the array, we set to 60% by default
    if success_l == False : 
        duty_cycle_s = 4.0
    reduction_ratio = get_reducer_from_dict(config_json["duty_cycle_duration_s"] , packet_to_share)
    to_return = duty_cycle_s * ( 2.0 - reduction_ratio) ## must be scaled from 1.0 to 2.0, we increase the duration here
    if to_return < 0.3 :
        to_return = 0.3
    return round(to_return,2)  

def get_duty_cycle_fill_rate_from_packet(config_json, packet_to_share : SharedPacket) -> float :
    '''
    Will take the power input and rescale it to a duty cycle duration
    Formula : 
    reducer = cloud_to_luminosity_reducer_converter(cloud_next_3h) * sunlight_duration_tomorrow_reducer_converter(cloud_next_3h)
    power_to_duration(current_irradiance) * (1.0 + reduction_ratio)
    '''
    duty_cycle_array = config_json["duty_cycle_fill_percent"]["power_to_fill_percent"]    
    success_l, duty_cycle_fill = get_linear_regression_from_array(duty_cycle_array, packet_to_share.power_input_watt)
    ## mean issue with the array, we set to 60% by default
    if success_l == False : 
        duty_cycle_s = 4.0
    reduction_ratio = get_reducer_from_dict(config_json["duty_cycle_fill_percent"] , packet_to_share)
    to_return = (duty_cycle_fill / 100.0) * reduction_ratio
    if to_return < 0.0 :
        to_return = 0.0
    elif to_return >= 1.0 :
        to_return = 1.0
    return round(to_return,2)  


def get_reducer_from_dict(dict, packet_to_share) : 
    '''
    Return (1.0 - ratio_cloud) * (1.0 - ratio_sun) * (1.0 - ratio_battery)
    '''
    cloud_red_array = dict["current_cloud_reducer"]
    success_c , cloud_reducing_percent = get_linear_regression_from_array(cloud_red_array, packet_to_share.nebulosite_actuelle)
    ## mean issue with the array
    if success_c == False : 
        cloud_reducing_percent = 0
        
    tomorrow_sunlight_red_array = dict["next_day_sunlight_hour_reducer"]
    tomorrow_sun_hour = packet_to_share.get_tomorrow_sunlight_duration_hour()
    success_s , tomorrow_sun_reducing_percent = get_linear_regression_from_array(tomorrow_sunlight_red_array, tomorrow_sun_hour)
    ## mean issue with the array
    if success_s == False : 
        tomorrow_sun_reducing_percent = 0

    battery_red_array = dict["battery_remaining_reducer"]
    success_b , battery_reducing_percent = get_linear_regression_from_array(battery_red_array, packet_to_share.charge_batterie_pourcent)
    ## mean issue with the array
    if success_s == False : 
        tomorrow_sun_reducing_percent = 0
    return (1.0 - cloud_reducing_percent / 100.0) *  (1.0 - tomorrow_sun_reducing_percent / 100.0) *  (1.0 - battery_reducing_percent / 100.0)



def get_day_index_from_packet(config_json, packet_to_share : SharedPacket) -> int :
    '''
    Return the slide of the day, the day start from the previous sunset to the next sunset
    Approximation => next day sunrise / sunset == current day sunset / sunrise
    '''
    array_day = config_json["day_slice"]["day"]
    array_night = config_json["day_slice"]["night"]
    force_day = config_json["day_slice"]["force_envoie_day"]
    if force_day >= 1 :
        return force_day

    index = 0
    ratio_done = 0
    ## we take only hour and minute because it s easier for the next calcul
    ## approximation all in minute
    pckt_min = packet_to_share.date.hour * 60 + packet_to_share.date.minute
    cs_min = packet_to_share.coucher_soleil.hour * 60 + packet_to_share.coucher_soleil.minute
    ls_min = packet_to_share.lever_soleil.hour * 60 + packet_to_share.lever_soleil.minute
    duration_sunlight_min = cs_min -  ls_min

    if packet_to_share.is_day_packet() == True : 
        ## day packet min into sunset
        current_min = pckt_min - ls_min
        ratio_done = 1.0 - (duration_sunlight_min - current_min) / duration_sunlight_min
        index_to_add = 0
        array_to_look_index = array_day
    else : 
        duration_night_min = 24 * 60 - duration_sunlight_min
        if pckt_min >= cs_min : 
            ## we are in the sun set before 00:00
            current_min = pckt_min - cs_min
        else :
            ## we are in the morning, between 00:00 and sunrise
            sunset_to_midnight_min =  24 * 60 - cs_min  ## approx at min, don't need the second
            current_min = pckt_min + sunset_to_midnight_min
        ratio_done = 1.0 - (duration_night_min - current_min) / duration_night_min
        index_to_add = len(array_day) - 1 ## -1 because len 4 and sharing one length with the other day_array
        array_to_look_index = array_night
        
    index_in_array = 0
    percent_done = 100.0 * ratio_done
    for value in array_to_look_index : 
        if value > percent_done :
            break
        index_in_array += 1
    return index_in_array + index_to_add



def print_all_day_index_from_packet(config_json) :
    current_index = -1
    sharedpacket = SharedPacket()
    today = datetime.datetime.now().date()

    sharedpacket.lever_soleil = datetime.datetime.combine(today, datetime.datetime.min.time()) + datetime.timedelta(hours=6)
    sharedpacket.coucher_soleil = datetime.datetime.combine(today, datetime.datetime.min.time()) + datetime.timedelta(hours=22)

    for h in range (0,24) :
        for m in range (0,59):
            sharedpacket.date = datetime.datetime.combine(today, datetime.datetime.min.time()) + datetime.timedelta(hours=h, minutes=m)
            idx = get_day_index_from_packet(config_json, sharedpacket)
            if idx != current_index :
                current_index = idx
                time.sleep(0.1)
                print(f"{current_index }: {sharedpacket.date}") 
    return