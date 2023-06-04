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

from psytestbench.psytb.property import PropertyWrapper, scpi
#from ds1000z.channel import Channel

from psytestbench.ds1000z.trigger.edge import Edge
from psytestbench.ds1000z.trigger.nth_edge import NthEdge


class Trigger(PropertyWrapper):
    
    def __init__(self, rawProperty:scpi.scpi_instrument.Property):
        super().__init__(rawProperty)
        self.edge = Edge(self.prop.edge)
        self.nthEdge = NthEdge(self.prop.nedge)
        
        
    def mode(self, setToMode:str=None):
        return self.getSetString(self.prop.mode, setToMode)
    
    def modeEdge(self):
        return self.mode('EDGE')
    def modeNthEdge(self):
        return self.mode('NEDG')
    def modePulse(self):
        return self.mode('PULSe')
    def modeRunt(self):
        return self.mode('RUNT')
    def modeWindow(self):
        return self.mode('WIND')
    def modeSlope(self):
        return self.mode('SLOPe')
    def modeVideo(self):
        return self.mode('VIDeo')
    def modePattern(self):
        return self.mode('PATTern')
    def modeDuration(self):
        return self.mode('DURation')
    def modeDelay(self):
        return self.mode('DELay')
    def modeRS232(self):
        return self.mode('RS232')
    def modeI2C(self):
        return self.mode('IIC')
    def modeSPI(self):
        return self.mode('SPI')
    
    
    
    def coupling(self, setToCpling:str=None):
        return self.getSetString(self.prop.coupling, setToCpling)
    
    def couplingAC(self):
        return self.coupling('AC')
    def couplingDC(self):
        return self.coupling('DC')
    def couplingHighpass(self):
        '''
            reject < 75kHz
        '''
        return self.coupling('LFReject')
    def couplingLowpass(self):
        '''
            reject > 75kHz
        '''
        return self.coupling('HFReject')
    
    
    def status(self):
        return self.prop.status()
    
    def statusIs(self, val):
        return self.status().lower().find(val.lower()) >= 0
    
    def statusIsAuto(self):
        return self.statusIs('auto')
    def statusIsWait(self):
        return self.statusIs('wait')
    def statusIsRun(self):
        return self.statusIs('run')
    def statusIsStop(self):
        return self.statusIs('stop')
    def statusIsTD(self):
        return self.statusIs('td')
    
    
    def sweep(self, setToMode:str=None):
        return self.getSetString(self.prop.sweep, setToMode)
    
    def sweepAuto(self):
        return self.sweep('AUTO')
    def sweepNormal(self):
        return self.sweep('NORMAL')
    def sweepSingle(self):
        return self.sweep('SINGLE')
    
    def auto(self):
        '''
            I always forget it's sweepAuto, 
            utility function trigger.auto()
            (and normal()/single())
        '''
        return self.sweepAuto()
    def normal(self):
        return self.sweepNormal()
    def single(self):
        return self.sweepSingle()
    
    def holdOff(self, setToSecs:float=None):
        '''
            stably trigger the complex waveforms (such as pulse
            series). Holdoff time is the time that the oscilloscope waits before re-arming the
            trigger circuitry.
            @setToSecs: optional     16ns to 10s (in seconds)
            @note: NOT available for video, timeout, setup/hold, Nth edge, RS232, I2C, or SPI triggers
        '''
        return self.getSetFloat(self.prop.holdoff, setToSecs)
    
    
    def noiseRejection(self, activate:bool=None):
        return self.activateBoolean(self.nreject, activate) 
    
    def position(self) -> int:
        '''
            -2 not triggered
            -1 triggered, out of mem
            >= 0 position in the
                internal memory that corresponds to the trigger position.
        '''
        return int(self.prop.position())

    
    
    
    