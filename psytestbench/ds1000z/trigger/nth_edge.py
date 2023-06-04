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
#from psytestbench.ds1000z.channel import Channel
class NthEdge(PropertyWrapper):
    
    def __init__(self, rawProperty:scpi.scpi_instrument.Property):
        super().__init__(rawProperty)
        
        
    def slope(self, slope:str=None):
        return self.getSetString(self.prop.slope, slope)
    
    def slopePositive(self):
        return self.slope('POSitive')
    def slopeNegative(self):
        return self.slope('NEGative')
    
    def idle(self, setToSecs:float=None):
        return self.getSetFloat(self.prop.idle, setToSecs)
    
    def edgeNumber(self, setToEdgeNum:int=None):
        '''
            u16_t value
        '''
        return self.getSetInt(self.prop.edge, setToEdgeNum)
    
    