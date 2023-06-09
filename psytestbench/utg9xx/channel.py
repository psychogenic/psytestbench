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
from psytestbench.psytb.property import IndexedProperty, scpi
from psytestbench.utg9xx.sweep import Sweep
from psytestbench.utg9xx.mode import Mode
from psytestbench.utg9xx.wave import Wave 
class Channel(IndexedProperty):
    '''
        An output channel from the signal generator.
        
        Use the channel to turn it on()/off() and set frequency, amplitude, offset...
        
        To keep things organized, many of the functions are available through 
        channel attributes, namely
        
            * mode (e.g. continuous, linear sweep, etc)
            * wave (e.g. sine, square etc)
            * sweep, which controls linear and log sweep settings
            
        See those for details.
    '''
    
    def __init__(self, chanid:int, channelProp:scpi.scpi_instrument.Property):
        super().__init__(chanid, channelProp)
        self.sweep = Sweep(self.prop.sweep)
        self.mode = Mode(self.prop.mode)
        self.wave = Wave(self.prop.base.wave)
        
    @property 
    def baseProp(self):
        return self.prop.base 
    
    def isOn(self):
        return self.on(None)
    
    def on(self, turnOn:bool=True):
        return self.activateBoolean(self.prop.output, turnOn)
    
    def off(self):
        return self.on(False)
    
    def invert(self, activate:bool=True):
        return self.activateBoolean(self.prop.inversion, activate)
        
    def isInvert(self):
        return self.invert(None)
    
    def sync(self, activate:bool=True):
        return self.activateBoolean(self.prop.output.sync, activate)
    
    def isSync(self):
        return self.sync(None)
    
    def limit(self, activate:bool=True):
        return self.activateBoolean(self.prop.limit.enable, activate)
    
    def isLimit(self):
        return self.limit(None)
    
    
    def amplitudeUnit(self, setTo:str=None):
        return self.getSetString(self.prop.amplitude, setTo)

    def amplitudeUnitVPP(self):
        '''
            set amplitude units to Vp-p
        '''
        return self.amplitudeUnit('VPP')
    def amplitudeUnitVRMS(self):
        '''
            set amplitude units to Vrms
        '''
        return self.amplitudeUnit('VRMS')
    def amplitudeUnitDBM(self):
        '''
            set amplitude units to dBm
        '''
        return self.amplitudeUnit('DBM')
    
    def limitLower(self, voltage:float=None):
        return self.getSetFloat(self.prop.limit.lower, voltage)

    def limitUpper(self, voltage:float=None):
        return self.getSetFloat(self.prop.limit.upper, voltage)
    
    def frequency(self, setHz:int=None):
        '''
            setter/getter
            
            @param setTo: optional value to set [Hz]
            @return: with no setTo, returns current setting
        '''
        return self.getSetInt(self.baseProp.frequency, setHz)

    
    def period(self, setSeconds:int=None):
        '''
            setter/getter
            
            @param setTo: optional value to set [secs]
            @return: with no setTo, returns current setting
        '''
        return self.getSetInt(self.baseProp.period, setSeconds)
    
    def phase(self, setDegrees:int=None):
        '''
            setter/getter
            
            @param setTo: optional value to set [degrees]
            @return: with no setTo, returns current setting
        '''
        return self.getSetInt(self.baseProp.phase, setDegrees)
    
    def amplitude(self, setInUnits:int=None):
        '''
            setter/getter
            
            @param setTo: optional value to set [amplitude units]
            @return: with no setTo, returns current setting
        '''
        return self.getSetInt(self.baseProp.amplitude, setInUnits)
    
    def offset(self, setInUnits:int=None ):
        '''
            setter/getter
            
            @param setTo: optional value to set [amplitude units?]
            @return: with no setTo, returns current setting
        '''
        return self.getSetInt(self.baseProp.offset, setInUnits)
    
    
    def dutyCycle(self, setToPercent:int=None):
        return self.getSetInt(self.baseProp.duty, setToPercent)
    
    
    