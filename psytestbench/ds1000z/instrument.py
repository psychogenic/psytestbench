'''
Created on Jun 2, 2023

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
'''
Created on May 26, 2023

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


from psytestbench.psytb.instrument_types import Oscilloscope
from psytestbench.ds1000z.channel import Channel
from psytestbench.ds1000z.acquire import Acquire
from psytestbench.ds1000z.measure import Measure
from psytestbench.ds1000z.measurement import Measurement
from psytestbench.ds1000z.timebase import Timebase

from psytestbench.ds1000z.trigger.trigger import Trigger

class Instrument(Oscilloscope):
    
    def __init__(self, port=None, port_match=True, backend='', handshake=False, arg_separator=',', **resource_params):
        '''
        
         @param port: The name of the port to connect to. [Default: None]
         @param backend: The pyvisa backend to use for communication. [Default: '']
         @param handshake: Handshake mode. [Default: False]
         @param arg_separator: Separator to use between arguments. [Default: ',']
         @param resource_params: Arguments sent to the resource upon connection.
                https://pyvisa.readthedocs.io/en/latest/api/resources.html
         @returns: An Instrument communicator.

        
        '''
        super().__init__(port, port_match, backend, handshake, arg_separator, **resource_params)
        # el swappy
        self.channel1 = Channel(1, self.channel1)
        self.channel2 = Channel(2, self.channel2)
        self.channel3 = Channel(3, self.channel3)
        self.channel4 = Channel(4, self.channel4)
        self.channels = [self.channel1, self.channel2, self.channel3, self.channel4]
        
        self.acquire = Acquire(self.acquire)
        self.measure = Measure(self.measure)
        self.measurement = Measurement(self)
        self.timebase = Timebase(self.timebase)
        self.trigger = Trigger(self.trigger)
        
        
    def clear(self):
        self.write(':STOP')
        
    def stop(self):
        self.write(':STOP')
    def run(self):
        self.write(':RUN')
    def single(self):
        self.write(':SINGLE')
        
    def triggerForce(self):
        self.write(':TForce')
        