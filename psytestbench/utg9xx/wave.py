'''
Created on Jun 3, 2023

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
from psytestbench.ds1000z.channel import Channel

class Wave(PropertyWrapper):
    
    def __init__(self, rawProperty:scpi.scpi_instrument.Property):
        super().__init__(rawProperty)
        
    def sine(self):
        '''
            set output to sine wave
        '''
        return self.prop('SINE')
    
    def square(self):
        '''
            set output to sine wave
        '''
        return self.prop('SQUARE')
    def pulse(self):
        '''
            set output to pulse
        '''
        return self.prop('PULSE')
    def ramp(self):
        '''
            set output to ramp
        '''
        return self.prop('RAMP')
    def arbitrary(self):
        '''
            set output to arbitrary
        '''
        return self.prop('ARB')
    def noise(self):
        '''
            set output to noise
        '''
        return self.prop('NOISE')
    def DC(self):
        '''
            set output to DC
        '''
        return self.prop('DC')