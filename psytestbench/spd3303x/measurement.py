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

from psytestbench.psytb.instrument.instrument import InstrumentAPIPackage
from psytestbench.psytb.instrument.scpi import SCPIInstrument

from psytestbench.spd3303x.channel import Channel

class Measurement(InstrumentAPIPackage):
    
    def __init__(self, parentInstrument:SCPIInstrument):
        super().__init__(parentInstrument)
        
        
    def getMeasurementOf(self, itemName:str, forChannel:Channel=None):
        
        q = f'MEASURE:{itemName}?'
        if forChannel is not None:
            q += f' {forChannel.name}'
        val = 0
        try:
            val = float(self.instrument.query(q))
        except:
            pass 
        
        return val
    
    def current(self, forChannel:Channel=None):
        return self.getMeasurementOf('CURRENT', forChannel)
    def voltage(self, forChannel:Channel=None):
        return self.getMeasurementOf('VOLTAGE', forChannel)
    def power(self, forChannel:Channel=None):
        return self.getMeasurementOf('POWER', forChannel)