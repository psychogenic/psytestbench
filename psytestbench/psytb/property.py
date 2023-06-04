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

import easy_scpi as scpi 

class PropertyWrapper:
    
    def __init__(self, rawProperty:scpi.scpi_instrument.Property):
        self._property = rawProperty
    
    @property 
    def currentValue(self):
        return self.prop()
    
    @property 
    def prop(self):
        return self._property

    
    def getSetFloat(self, targetProperty:scpi.scpi_instrument.Property, val:float=None):
        if val is None:
            return float(targetProperty())
        return targetProperty(val)

    def getSetInt(self, targetProperty:scpi.scpi_instrument.Property, val:int=None):
        if val is None:
            return int(targetProperty())
        return targetProperty(val)
    
    def getSetString(self, targetProperty:scpi.scpi_instrument.Property, val:str=None):
        if val is None:
            return targetProperty()
        
        return targetProperty(val)
    def activateBoolean(self, targetProperty:scpi.scpi_instrument.Property, activate:bool=None):
        
        if activate is None:
            if int(targetProperty()):
                return True 
            else:
                return False
        
        v = 0
        if activate:
            v = 1
        return targetProperty(v)
    

class IndexedProperty(PropertyWrapper):
    
    def __init__(self, propid:int, rawProperty:scpi.scpi_instrument.Property):
        super().__init__(rawProperty)
        self.id = propid
    
    
    
    
    