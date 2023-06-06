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
from psytestbench.psytb.instrument.scpi import SCPIInstrument
import psytestbench.psytb.instrument_roles as role
from psytestbench.spd3303x.channel import Channel

from psytestbench.spd3303x.measurement import Measurement

class Instrument(SCPIInstrument):
    Role = role.PowerSupply
    
    def __init__(self, port=None, port_match=True, 
                 backend='', handshake=False, arg_separator=',', **resource_params):
        '''
        
         @param port: The name of the port to connect to. [Default: None]
         @param backend: The pyvisa backend to use for communication. [Default: '']
         @param handshake: Handshake mode. [Default: False]
         @param arg_separator: Separator to use between arguments. [Default: ',']
         @param resource_params: Arguments sent to the resource upon connection.
                https://pyvisa.readthedocs.io/en/latest/api/resources.html
         @returns: An Instrument communicator.

        
        '''
        super().__init__(port, port_match, backend, handshake, arg_separator, 
                         query_delay=0.025,
                         **resource_params)
        self.min_write_delay_s = 0.050
        
        self.channel1 = Channel(1, self, self.ch1)
        self.channel2 = Channel(2, self, self.ch2)
        self.channel3 = Channel(3, self, self.ch2)
        
        self.measurement = Measurement(self)
        
        self.outputs = [
                self.channel1,
                self.channel2,
                self.channel3
            
            ]
        

    def recall(self, idx:int):
        if idx < 1 or idx > 5:
            raise ValueError('Must use 1-5 for save/recall position ')
        self.write(f'*RCL {idx}')
        
    def save(self, idx:int):
        if idx < 1 or idx > 5:
            raise ValueError('Must use 1-5 for save/recall position ')
        self.write(f'*SAV {idx}')
        
    def trackingMode(self, setTo:int):
        return self.output.track(setTo)
    def trackingModeIndependent(self):
        return self.trackingMode(0)
    def trackingModeSeries(self):
        return self.trackingMode(1)
    def trackingModeParallel(self):
        return self.trackingMode(2)
    
    def select(self, channel:Channel):
        self.inst(channel.name)
        
    def selected(self) -> Channel:
        v = self.inst().rstrip()
        for ch in self.outputs:
            if v == ch.name:
                return ch 
            
        return None
        