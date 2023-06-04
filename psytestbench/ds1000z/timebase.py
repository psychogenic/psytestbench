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

import time
import math

from psytestbench.psytb.property import PropertyWrapper, scpi
import psytestbench.ds1000z.settings as settings 

import logging 
log = logging.getLogger(__name__)

class Timebase(PropertyWrapper):
    '''
        An output channel from the signal generator.
        
        This is a collection of utility methods to provide a handy interface
        and mask the SCPI specific stuff (e.g. when it's :CHANNEL<n>:BLAh 
        vs when it's :CHANnel<n>:BASE:BLAh).
    
    '''
    
    def __init__(self, prop:scpi.scpi_instrument.Property):
        super().__init__(prop)
        self.last_scale = None
        
    
    def mode(self, setTo:str=None):
        return self.getSetString(self.prop.mode, setTo)
    
    def modeYT(self):
        return self.mode('MAIN')
    
    def modeXY(self):
        return self.mode('XY')
    
    def modeRoll(self):
        return self.mode('ROLL')
    
    def offset(self, setToSecs:float=None):
        '''― YT mode
                RUN: (-0.5 x MemDepth/SampleRate) to 1s (when the horizontal
                timebase is less than 200ms/div)
                (-0.5 x MemDepth/SampleRate) to (10 x MainScale) (when the
                horizontal timebase is greater than or equal to 200ms/div, namely
                the "Slow Sweep" mode)
                STOP: (-MemDepth/SampleRate) to (1s + 0.5 x MemDepth/SampleRate)
            ― Roll mode
                RUN: This command is invalid.
                STOP: (-12 x MainScale) to 0
        
        '''
        return self.getSetFloat(self.prop.offset, setToSecs)
    
    def scale(self, setToSecs:float=None):
        '''
            YT mode: 5ns/div to 50s/div in 1-2-5 step
            Roll mode: 200ms/div to 50s/div in 1-2-5 step1μs/div
        '''
        retval = None
        if setToSecs is None:
            return self.getSetFloat(self.prop.scale)
        else:
            if setToSecs != self.last_scale:
                self.last_scale = setToSecs 
                log.info(f'Changing timescale to {setToSecs}')
                retval =  self.getSetFloat(self.prop.scale, setToSecs)
                time.sleep(settings.ScaleChangeDelaySecs)
                
        return retval
                
    
    def scaleToFrequency(self, frequencyHz:int):
        period = 1/frequencyHz 
        # we want around 5-10 cycles per screen
        divisionsPerScreen = settings.ScreenTimeDivisions
        minScale = (period * settings.TimebaseMinPeriodsPerScreen)/divisionsPerScreen 
        maxScale = (period * settings.TimebaseMaxPeriodsPerScreen)/divisionsPerScreen
        
        expMax = round(math.log10(1/minScale))
        expMin = round(math.log10(1/minScale))
        
        for exp in [expMin, expMax]:
            for i in [1,2,5]: # only allows for 1-2-5
                v = i/(10**exp)
                if v >= minScale and v<= maxScale:
                    log.debug(f'Setting scale to {v} secs')
                    self.scale(v)
                    return 
        
        log.warn(f'No valid timescale found for freq {frequencyHz}Hz?')
        
        
        
        
    
    