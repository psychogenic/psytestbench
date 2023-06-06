'''
Created on Jun 6, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''

try:
    import hid 
    HIDLibraryIsPresent = True
except:
    HIDLibraryIsPresent = False 

import struct
from psytestbench.psytb.instrument.serial import SerialInstrument

import psytestbench.psytb.instrument_roles as role

import logging 

log = logging.getLogger(__name__)

class ReadingValue:
    def __init__(self, val, units):
        self.value = val 
        self.units = units
        
    def __repr__(self):
        return f'{self.value}{self.units}'
        

class Instrument(SerialInstrument):
    Role = role.MultiMeter
    
    StartMarker = b'\xab\xcd!'
    def __init__(self, path:str=None):
        if path is None:
            if not HIDLibraryIsPresent:
                raise RuntimeError('No path passed and hid library not found to enumerate')
            
            numFound = 0
            for devs in hid.enumerate():
                if devs['product_string'].find('CP21') >= 0:
                    path = self._hidpathToURL(devs['path'])
                    log.info(f"CP21xx device found: {devs['path']} ({devs['product_string']})")
                    numFound += 1
            
            if not numFound:
                raise RuntimeError('No CP2110 devices enumerated--cannot find DMM')
            if numFound > 1:
                log.warn("Multiple CP21xx devices found??? using last (pass path)")
                
        if path.lower().find('usb:') >= 0:
            vals = path.split(':')
            vendor_id = int(vals[1], 16)
            product_id = int(vals[2], 16)
            if not HIDLibraryIsPresent:
                raise RuntimeError('Passed a USB:VID:PID path but no hid library to enum!')
            
            for devs in hid.enumerate():
                if devs['vendor_id'] == vendor_id and devs['product_id'] == product_id:
                    path = self._hidpathToURL(devs['path'])
        
        if path is None or not len(path):
            raise RuntimeError('Must pass some sort of path to UT880x instrument')
        
        super().__init__(path)
            
    def _hidpathToURL(self, path:bytearray):
        decPath = path.decode('ascii')
        return f'cp2110://{decPath}'
    
    def flush(self):
        self.read_all()
        self.serialConn.read_until(Instrument.StartMarker)
        
        
    def _bufToReading(self, buf):
        startIdx = 7
        if len(buf) < 15:
            return None
        val = struct.unpack("f", buf[startIdx:startIdx+4])[0]
        
        unitsFieldStart = startIdx + 5
        unitsChars = buf[unitsFieldStart:].find(b'\x00')
        units = buf[unitsFieldStart:unitsFieldStart+unitsChars].decode('utf-8')
        
        return ReadingValue(val, units)
        
        
        
    def readingNext(self):
        return self._bufToReading(self.serialConn.read_until(Instrument.StartMarker))
    
    def readingLatest(self):
        self.flush()
        return self.readingNext()
        
