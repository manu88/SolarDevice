
import time
from abc import ABC, abstractmethod

class ManagerModule(ABC) :
    '''
    Base class which will do the on_update function each Refresh rate sec
    '''
    def __init__(self, refresh_rate_s) :
        self.__lastTick_s = 0
        self.refresh_rate_s = refresh_rate_s

        self.force_update_on_next = False
        ## used to print every update if set to true in the child class
        self.print_update = True

        ## if set to false, will not update the class
        self.enable = True
        return
    
    def start(self) :
        if self.enable == False:
            return
        self.on_start()
        return

    def update(self, packet_to_share):
        if self.enable == False:
            return

        t_s = time.time()
        if (self.force_update_on_next  == True or t_s - self.__lastTick_s > self.refresh_rate_s) : 
            self.__lastTick_s = t_s
            self.force_update_on_next = False
            self.on_update(packet_to_share)
        return
    
    
    @abstractmethod
    def on_start(self, packet_to_share) :
        return
    
    
    @abstractmethod
    def on_update(self, packet_to_share) :
        return