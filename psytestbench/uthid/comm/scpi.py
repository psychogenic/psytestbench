'''
Created on May 26, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''
import pyvisa as visa 

from psytestbench.uthid.comm.channel import Channel



class SCPI(Channel):
    def __init__(self, devAddress=1):
        super().__init__(devAddress)
        self._dev = None 
        self.address = devAddress
        
        
    @property
    def device(self):
        if self._dev is not None: 
            return self._dev 
        
        rm = visa.ResourceManager('@py')
        
        self._dev = rm.open_resource(self.address)
        return self._dev 
    
    def open(self):
        self.close()    
        return self.device.open()
            
        
    def read(self, size:int=0, timeout:int=0) -> bytearray:
        return bytearray(self.device.read(size), 'ascii')
        
    
    def write(self, byteslist:bytearray):
        return self.device.write(byteslist.decode('ascii'))
    
    def close(self):
        if self._dev is not None:
            self.device.close()
            self._dev = None 
            
            
        