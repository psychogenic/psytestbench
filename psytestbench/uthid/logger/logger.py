'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

import datetime 

from psytestbench.uthid.event.listener import Listener
from psytestbench.uthid.frame.response.types import Response

class Logger(Listener):
    def __init__(self, minInterval:datetime.timedelta=None, showHeader:bool=True):
        super().__init__()
        self._mininterval = minInterval
        self._lastNotif = None
        self._started = False 
        self.showHeader = showHeader
        
    @property 
    def started(self):
        return self._started
    
    def outputHeader(self):
        return 
    
    def begin(self):
        self._started = True
        if self.showHeader:
            self.outputHeader()
        
    def end(self):
        self._started = False
        
        
    def timestamp(self, dt:datetime.datetime=None):
        if dt is None:
            dt = datetime.datetime.now() 
            
        return dt.isoformat()
    
    def listenerNotify(self, resp:Response):
        if not self.started:
            return 
        
        if self._mininterval is None:
            return super().listenerNotify(resp)
        
        dtnow = datetime.datetime.now()
        if self._lastNotif is None or dtnow > self._lastNotif + self._mininterval:
            self._lastNotif = dtnow 
            return super().listenerNotify(resp)
        