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

from psytestbench.psytb.instrument import Instrument, InstrumentAPIPackage

from psytestbench.ds1000z.channel import Channel

class Measurement(InstrumentAPIPackage):
    
    def __init__(self, parentInstrument:Instrument):
        super().__init__(parentInstrument)
        
    def getMeasurementOf(self, itemName:str, forChannel:Channel=None):
        
        q = f':MEASURE:{itemName}?'
        if forChannel is not None:
            q += f' CHAN{forChannel.id}'
        val = 0
        try:
            val = float(self.instrument.query(q))
        except:
            pass 
        
        return val
    
    def vMax(self, forChannel:Channel=None):
        return self.getMeasurementOf('VMAX', forChannel)
    
    def vMin(self, forChannel:Channel=None):
        return self.getMeasurementOf('VMIN', forChannel)
    def vPP(self, forChannel:Channel=None):
        return self.getMeasurementOf('VPP', forChannel)
    def vTop(self, forChannel:Channel=None):
        return self.getMeasurementOf('VTOP', forChannel)
    def vBase(self, forChannel:Channel=None):
        return self.getMeasurementOf('VBASE', forChannel)
    def vAmp(self, forChannel:Channel=None):
        return self.getMeasurementOf('VAMP', forChannel)
    def vAvg(self, forChannel:Channel=None):
        return self.getMeasurementOf('Vavg', forChannel)
    def vRMS(self, forChannel:Channel=None):
        return self.getMeasurementOf('VRMS', forChannel)
    def overshoot(self, forChannel:Channel=None):
        return self.getMeasurementOf('OVERSHOOT', forChannel)
    def period(self, forChannel:Channel=None):
        return self.getMeasurementOf('PER', forChannel)
    def frequency(self, forChannel:Channel=None):
        return self.getMeasurementOf('FREQ', forChannel)
    def dutyP(self, forChannel:Channel=None):
        return self.getMeasurementOf('PDuty', forChannel)
    def dutyN(self, forChannel:Channel=None):
        return self.getMeasurementOf('NDuty', forChannel)
        
    def vMaxTime(self, forChannel:Channel=None):
        return self.getMeasurementOf('TVMax', forChannel)
        
    def vMinTime(self, forChannel:Channel=None):
        return self.getMeasurementOf('TVMin', forChannel)
        
    