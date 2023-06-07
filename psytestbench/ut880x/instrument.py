'''
Created on Jun 6, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''

import struct


from psytestbench.psytb.instrument.uthid import UTHIDInstrument

import psytestbench.psytb.instrument_roles as role


# these imports are just to make things more intuitive from user side
# see dmm_monitor example.
from psytestbench.uthid.event import Listener
from psytestbench.uthid.frame.response.types import Response, ReplyCode
from psytestbench.uthid.frame.response.measurement import ValueWithPrecision, \
    Measurement, MeasurementMinMax, MeasurementNormal, MeasurementPeak, MeasurementRelative


import psytestbench.uthid.seldevice

import logging 

log = logging.getLogger(__name__)

class ReadingValueXXX:
    def __init__(self, val, units):
        self.value = val 
        self.units = units
        
    def __repr__(self):
        return f'{self.value}{self.units}'
        

class Instrument(UTHIDInstrument):
    Role = role.MultiMeter
    ugh = b'\xab\xcd\x04\x00\x05\x01\n\x00'
    StartMarker = b'\xab\xcd!'
    def __init__(self, path:str=None):
        
        psytestbench.uthid.seldevice.setDeviceUT800x()
        
        import psytestbench.uthid.frame.command as commands
        super().__init__(path, commands)
    
    def flush(self):
        self.read_all()
        