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
from psytestbench.psytb.property import IndexedProperty, scpi

class Channel(IndexedProperty):
    '''
        A DSO channel.  Using this attribute you can turn on and off 
        and set
        * scale
        * offset
        * bandwidth limit
        * coupling (e.g. AC, DC...)
        etc
    
    '''
    
    def __init__(self, chanid:int, channelProp:scpi.scpi_instrument.Property):
        super().__init__(chanid, channelProp)
        
    
    
        
    @property 
    def name(self):
        return f'CHAN{self.id}'
    
        
        
    
    def bandwidthLimit(self, setTo:str=None):
        return self.getSetString(self.prop.bwlimit, setTo)
    
    def bandwidthLimitOff(self):
        return self.bandwidthLimit('OFF')
    
    def bandwidthLimit20MHz(self):
        return self.bandwidthLimit('20M')
    

    def coupling(self, setTo:str=None):
        return self.getSetString(self.prop.coupling, setTo)
        
    def couplingDC(self):
        return self.coupling('DC')
    
    def couplingAC(self):
        return self.coupling('AC')
    
    def couplingGND(self):
        return self.coupling('GND')
    
    
    
    def isOn(self):
        return self.on(None)
    
    def on(self, turnOn:bool=True):
        return self.activateBoolean(self.prop.display, turnOn)
    
    def off(self):
        return self.on(False)
    
    def display(self, turnOn:bool=True):
        return self.on(turnOn)

        
    def invert(self, activate:bool=True):
        return self.activateBoolean(self.prop.invert, activate)
        
    def isInvert(self):
        return self.invert(None)
    
    def offset(self, setInUnits:float=None ):
        '''
            setter/getter
            
            @param setTo: optional value to set [amplitude units?]
            @return: with no setTo, returns current setting
        '''
        return self.getSetFloat(self.prop.offset, setInUnits)
    
    
    
    
    
    def delayCalibrationTime(self, setToSecs:float=None ):
        '''
            range is -100 ns to 100 ns, passed in as secs.
            0.00000002 is 20 ns
        '''
        return self.getSetFloat(self.tcal, setToSecs)
    
    
    def probe(self, setToAttenuation:float):
        '''
            @setToAttenuation: valid values
                0.01|0.02|0.05|0.1|0.2|0.5|1|2|5|10|20|50|100|200|500|1000
            10 == 10x
        '''
        
        return self.getSetFloat(self.prop.probe, setToAttenuation)
    
    
    
    
    def scale(self, setInUnits:float=None ):
        '''
            related to probe
            When the probe ratio is 1X: 1mV to 10V
            When the probe ratio is 10X (default): 10mV to
            100V
        '''
        return self.getSetFloat(self.prop.scale, setInUnits)
    
    def range(self, setInUnits:float=None ):
        '''
            Related to probe.
            When the probe ratio is 1X: 8mV to 80V
            When the probe ratio is 10X: 80mV to 800V
        
        '''
        return self.getSetFloat(self.prop.range, setInUnits)
    

    
    def units(self, setTo:str=None):
        return self.getSetString(self.prop.units, setTo)
    
    def unitsVolt(self):
        return self.units('VOLT')
    
    def unitsWatt(self):
        return self.units('WATT')
    
    def unitsAmp(self):
        return self.units('AMP')
    
    def unitsUnknown(self):
        return self.units('UNKNOWN')
    
    
    