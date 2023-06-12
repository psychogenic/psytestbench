'''
Created on Jun 12, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
   This file is part of the Psychogenic Technologies testbench (psytestbench).

   psytestbench is free software: you can redistribute it and/or modify it under 
   the terms of the GNU General Public License as published by the Free Software 
   Foundation, either version 3 of the License, or (at your option) any later version.

   psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY 
   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
   PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with psytestbench. 
If not, see <https://www.gnu.org/licenses/>.


  A simplified UT880X DMM interface.  The Unitrend UT8804 and friends just spews out a
  ton of measurement messages when you are monitoring.
  
  This puts the onus on you to begin some form of asynchronous processing or to poll() it
  continuously.  A bit annoying.
  
  This is an example of how to use a simple wrapper that basically just gives you access to the 
  latest measurement at any time.
  
  

'''


import threading
import time
import psytestbench.examples.mylab 
from psytestbench.examples.mylab import DMMListener, DMMMeasurement, DMMValueWithPrecision

import logging 
log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

class Measurement:
    
    def __init__(self, mId:int, measObj:DMMMeasurement):
        self.id = mId
        self._source = measObj 
        
    @property
    def source(self) -> DMMMeasurement:
        return self._source
    
    @property 
    def mode(self):
        return self._source.mode
    
    def value(self, name:str='main') -> DMMValueWithPrecision:
        return self.source.valueByName(name)
    
    def value_string(self, name:str='main') -> str:
        v = self.value(name)
        if v is not None:
            return f'{v.value_string} {v.units}'
        return None
        

        
class MeasurementTracker(DMMListener):
    def __init__(self, listenerId:int=None):
        super().__init__(listenerId)
        self._rcvCount = 0
        self._lock = threading.Lock()
        self._last_measurement = None
        
    @property 
    def latest(self) -> Measurement:
        with self._lock:
            v = self._last_measurement
        
        return v
    
        
    def measurement(self, m:Measurement):
        self._rcvCount += 1
        with self._lock:
            self._last_measurement = Measurement(self._rcvCount, m)
    


def main():
    lab = psytestbench.examples.mylab.Lab
    if lab.dmm is None:
        raise RuntimeError('Could not connect to DMM')
    
    lab.dmm.connect()
    
    
    timeBetweenOutputsSecs = 1
    print(f"Will output current reading every {timeBetweenOutputsSecs}.  Hit CTRL-C to abort and shutdown.")
    
    measTracker = MeasurementTracker()
    lab.dmm.listenerAdd(measTracker)
    lab.dmm.startAsyncMonitoring()
    
    try:
        while True:
            # do other stuff, simulated by simple sleep
            time.sleep(1)
            
            # at any time, get the latest measurement from the tracker
            measurementNow = measTracker.latest
            
            
            # this is an instance of the Measurement class defined above
            # for which we've added various helpers
            # most "normal" readings have a 'main' reading, may also have
            # bargraph, aux1 and 2, etc... depends on how the DMM is 
            # currently configured
            valStr = measurementNow.value_string('main')
            if valStr is not None:
                print(f"Main reading ({measurementNow.id}): {valStr} ({measurementNow.mode})")
            else:
                # no main, just dump raw measurement
                print(str(measurementNow.source))
            
    except KeyboardInterrupt:
        pass 
    
    # you could dmm.stopAsyncMonitoring() but this is handled
    # in disconnect() anyway
    lab.disconnect()


main()
        