'''
Created on Jun 6, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''

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

class Instrument(UTHIDInstrument):
    '''
    This class implements functionality for the Unitrend UT880x (tested on UT8804N) digital
    multimeters.
    
    Only measurements available from the current physical selector position are available (i.e. turn the knob).
    
    It is normally used asynchronously, with event listeners rather than polled.  This 
    simple example shows the full manual mode, while still leveraging the response parsing and encapsulation.
    
    @see: examples/dmm_logger.py which demonstrates asynchronous event generation, so you don't have to poll manually.

    
    In short:
        1) some event listener class is defined, to process incoming measurements
        2) the DMM instance is created and a listener added/monitor mode engaged
        3) the DMM is polled occasionally, which will send any received and processed measurements to the listener
    
    # this is a class derived from the DMM listener to output measurements received
    class DMMEventListener(Listener):
        def dumpReading(self, name, val:ValueWithPrecision):
            print(f'{name}: {val.value_string} {val.units}')
            
        def measurement(self, m:Measurement):
            print(f'Measurement')
            for vname in m.valueNames:
                self.dumpReading(vname, m.valueByName(vname))
            log.warn("Raw: %s" % str(m))
    
    dmm = psytestbench.ut880x.instrument.Instrument('usb:10c4:ea80')
    # add the listener to the DMM
    listener = DMMEventListener()
    dmm.listenerAdd(listener)
    
    # enable monitoring of the DMM
    dmm.monitoring = True 
    try:
        for _i in range(400):
            dmm.poll() # poll it manually (multiple measurements may be sent to listener)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    
    dmm.monitoring = False
    dmm.disconnect()
    
    '''
    Role = role.MultiMeter
    def __init__(self, path:str=None):
        
        psytestbench.uthid.seldevice.setDeviceUT800x()
        
        import psytestbench.uthid.frame.command as commands
        super().__init__(path, commands)
    
    def flush(self):
        self.read_all()
        