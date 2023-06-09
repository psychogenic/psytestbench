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


from psytestbench.psytb.instrument.scpi import SCPIInstrument
import psytestbench.psytb.instrument_roles as role
from psytestbench.utg9xx.channel import Channel

class Instrument(SCPIInstrument):
    '''
        This signal generator instrument has two output channels.
        
        Other than connect/disconnect and locking, all the functionality happens 
        through the two channels themselves.
        
        Basic channel properties are accessed through channelN, e.g.
        
        siggen.channel1.frequency(1000)
        siggen.channel1.on()
        
        but much of the functionality is accessed through channel attributes, namely:
        
            * mode (e.g. continuous, linear sweep, etc)
            * wave (e.g. sine, square etc)
            * sweep, which controls linear and log sweep settings
        
        For instance
        
        # get access
        siggen = psytestbench.utg9xx.instrument.Instrument('USB0::26191::2100::3573542343::0::INSTR')
        siggen.connect()
        siggen.lock()
        
        # set a 2khz square wave on 1
        siggen.channel1.frequency(2000)
        siggen.channel1.wave.square()
        
        # set a 1-10kHz sine sweep on 2
        siggen.channel2.wave.sine()
        siggen.channel2.mode.sweepLinear()
        siggen.channel2.sweep.frequencyStart(1000)
        siggen.channel2.sweep.frequencyStop(10000)
        siggen.channel2.sweep.time(5) # 5 seconds to sweep
        
        # turn 'em on
        
        siggen.channel1.on()
        siggen.channel2.on()
        
        # disconnect
        siggen.disconnect() # auto unlocks

    '''
    Role = role.SignalGenerator
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
    
            
            
        