'''
Created on Jun 6, 2023

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
from psytestbench.psytb.instrument_roles.role import InstrumentRole
class InstrumentType:
    def __init__(self, instrumentClass:type, resourceId:str=''):
        self.classType = instrumentClass 
        self.resourceId = resourceId 
        
    @property 
    def instrumentTypeName(self):
        return self.classType.InstrumentTypeName 
    
    def hasRole(self, role:InstrumentRole):
        return self.classType.role() == role
    
    def construct(self):
        ctype = self.classType 
        return ctype(self.resourceId)
    