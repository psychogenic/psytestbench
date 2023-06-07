'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
from psytestbench.uthid.comm.channel import Channel

import serial

class Serial(Channel):
    def __init__(self, port:str='', baud=115200, timeout=1, device=None):
        super().__init__(port)
        self._dev = device 
        self.baud = baud 
        self.timeout = timeout 
        
        
    @property
    def device(self) -> serial.Serial:
        if self._dev is not None: 
            return self._dev 
        
        self._dev = serial.Serial(self.name, baudrate=self.baud, timeout=self.timeout)
        return self._dev 
    
    def open(self):
        self.close()    
        return self.device.open()
            
        
    def read(self, size:int=0, timeout:int=0) -> bytearray:
        return self.device.read(size)
        
    
    def write(self, byteslist:bytearray):
        return self.device.write(byteslist)
    
    def close(self):
        if self._dev is not None:
            self.device.close()
            self._dev = None 
            
            
        