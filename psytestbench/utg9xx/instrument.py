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

from psytestbench.psytb.instrument_types import SignalGenerator
from psytestbench.utg9xx.channel import Channel

class Instrument(SignalGenerator):
    
    def __init__(self, port=None, port_match=True, backend='', handshake=False, arg_separator=',', **resource_params):
        '''
        
         @param port: The name of the port to connect to. [Default: None]
         @param backend: The pyvisa backend to use for communication. [Defualt: '']
         @param handshake: Handshake mode. [Default: False]
         @param arg_separator: Separator to use between arguments. [Default: ',']
         @param resource_params: Arguments sent to the resource upon connection.
                https://pyvisa.readthedocs.io/en/latest/api/resources.html
         @returns: An Instrument communicator.

        
        '''
        super().__init__(port, port_match, backend, handshake, arg_separator, **resource_params)
        self.channel1 = Channel(1, self.channel1)
        self.channel2 = Channel(2, self.channel2)
        self.channels = [self.output1, self.output2]
        
        
    def lock(self, setLocked:bool=True):
        if setLocked is None:
            return bool(self.system.lock())
        
        v = 0
        if setLocked:
            v = 1
            
        return self.system.lock(v)
    
    def isLocked(self):
        return self.lock(None)
    
    
    def disconnect(self):
        '''
            Disconnect from device (auto unlocks if necessary)
        '''
        if self.isLocked():
            self.lock(False)
            
        super().disconnect()
    
            
            
        