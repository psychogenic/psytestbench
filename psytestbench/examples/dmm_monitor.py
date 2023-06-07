'''
Created on Jun 7, 2023

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
'''


#from psytestbench.spd3303x.instrument import Channel, Instrument as BenchSupply
from psytestbench.psytb.cli import CLI 
import time
from psytestbench.ut880x.instrument import Listener, ReplyCode, Measurement, ValueWithPrecision
import psytestbench.examples.mylab 

import logging 
log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)
            
class DMMEventListener(Listener):
    def replyCode(self, reply:ReplyCode):
        # override me
        log.warn("Got reply:\n%s" % str(reply))
    
    def dumpReading(self, name, val:ValueWithPrecision):
        print(f'{name}: {val.value_string} {val.units}')
        
    def measurement(self, m:Measurement):
        print(f'Measurement')
        for vname in m.valueNames:
            self.dumpReading(vname, m.valueByName(vname))
        log.warn("Raw: %s" % str(m))
        
def main():
    lab = psytestbench.examples.mylab.Lab
    listener = DMMEventListener()
    lab.dmm.listenerAdd(listener)
    lab.dmm.monitoring = True 
    try:
        for _i in range(400):
            lab.dmm.poll()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    
    lab.dmm.monitoring = False
    lab.dmm.disconnect()
    
main()
    