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

from psytestbench.psytb.instrument_roles.role import InstrumentRole

from psytestbench.psytb.event.listener import Listener
from psytestbench.psytb.event.notifier import Notifier
class Instrument:
    
    @classmethod 
    def instrumentRole(cls) -> InstrumentRole:
        return cls.Role
    
    @classmethod 
    def instrumentRoleName(cls) -> InstrumentRole:
        return cls.Role.name()
    
    def __init__(self):
        self.event_notifier = Notifier()
    
    def connect(self):
        return False
    
    def disconnect(self):
        return False

    def write(self, v):
        return False
    
    
    # event notifier interfaces
    def listenerAdd(self, listener:Listener):
        self.event_notifier.add(listener)
        
    def listenerRemove(self, listener:Listener):
        self.event_notifier.remove(listener)
        
    def notify(self, response):
        self.event_notifier.notify(response)
    

class InstrumentAPIPackage:
    
    def __init__(self, parentInstrument:Instrument):
        self._instrument = parentInstrument
        
        
    @property 
    def instrument(self) -> Instrument:
        return self._instrument