'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
from psytestbench.uthid.comm.channel import Channel

#import cp2110
import hid 
import serial



class CP2110(Channel):
    def __init__(self, vendor:int=0x10c4, product:int=0xea80):
        super().__init__('CP2110')
        self._dev = None 
        self._path = None 
        for aDev in hid.enumerate():
            if aDev['vendor_id'] == vendor and aDev['product_id'] == product:
                self._path = aDev['path'].decode('ascii')
                break
        
        if self._path is None:
            raise ValueError(f'Could not find HID device {vendor}:{product} on bus')
        
    @property
    def device(self) : # -> cp2110.CP2110Device:
        if self._dev is not None: 
            return self._dev 
        self._dev = serial.serial_for_url(f'cp2110://{self._path}')
        return self._dev 
    
    def open(self, params=None):
        if self.device.isOpen():
            return 
        self.device.open()
    
    def openOLD(self, params=None):
        rVal =  self.device.enable_uart()
        c = self.device.get_uart_config()
        c.baud = 9600
        self.device.set_uart_config(c)
        return rVal
            
        
    def read(self, size:int=2, timeout:int=0) -> bytearray:
        return self.device.read(size)
    
    def write(self, byteslist:bytearray):
        return self.device.write(byteslist)
    
    def close(self):
        if self._dev is not None and self._dev.isOpen():
            return self._dev.close()
        
        return False
    def closeOLD(self):
        if self._dev is not None:
            return self.device.disable_uart()
        
        return False
    
    
    def flush(self):
        if self._dev is None:
            return 
        b = self.read()
        while len(b):
            b = self.read()

class CP2110OLD(Channel):
    def __init__(self, vid=None, pid=None, serial=None, path=None):
        super().__init__('CP2110')
        self._dev = None 
        self.vid = vid 
        self.pid = pid 
        self.serial = serial 
        self.path = path
        
        
    @property
    def device(self) : # -> cp2110.CP2110Device:
        if self._dev is not None: 
            return self._dev 
        self._dev = cp2110.CP2110Device(self.vid, self.pid, self.serial, self.path)

        return self._dev 
    
    def open(self, params=None):
        rVal =  self.device.enable_uart()
        c = self.device.get_uart_config()
        c.baud = 9600
        self.device.set_uart_config(c)
        return rVal
            
        
    def read(self, size:int=2, timeout:int=0) -> bytearray:
        return self.device.read(size)
    
    def write(self, byteslist:bytearray):
        return self.device.write(byteslist)
    
    def close(self):
        if self._dev is not None:
            return self.device.disable_uart()
        
        return False
    
    
    def flush(self):
        if self._dev is None:
            return 
        b = self.read()
        while len(b):
            b = self.read()
            
    
        