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

from psytestbench.psytb.instrument_roles.role import InstrumentRole
import psytestbench.psytb.instrument_roles as roles
from psytestbench.psytb.instrument.type import InstrumentType
from psytestbench.psytb.instrument.instrument import Instrument as InstrumentBase

import logging 
log = logging.getLogger(__name__)
class LabInstruments:
    
    def __init__(self, typeIdTuplesList:list, autoconnect=True):
        self._instDetails = []
        for ttup in typeIdTuplesList:
            self._instDetails.append(InstrumentType(ttup[0], ttup[1]))
            
        self.autoconnect = autoconnect
        self._dso = None 
        self._siggen = None 
        self._benchsupply = None 
        self._dmm = None 
        
        
    def hasInstrumentRole(self, roleType:InstrumentRole) -> InstrumentType:
        for instType in self._instDetails:
            if instType.hasRole(roleType):
                return instType
            
        return None
        
    def generateInstrument(self, ofType):
        instType = self.hasInstrumentRole(ofType)
        if instType is None:
            log.warn(f'No info found to generate {ofType} instrument')
            return None
        
        try:
            newInst =  instType.construct()
        except RuntimeError as e:
            log.error(f'Failed to construct device!\n{e}')
            return None
        if self.autoconnect:
            log.info(f'Connection (auto) to newly constructed {newInst}')
            try:
                newInst.connect()
            except:
                log.error(f'Failed to connect to device!')
        return newInst
            
        
        
    
    def disconnect(self):
        instruments = [
                self._dso,
                self._siggen,
                self._benchsupply,
                self._dmm,
            ]
        
        for inst in instruments:
            if inst is not None and inst.is_connected:
                log.info(f'Disconnecting {inst}')
                inst.disconnect()
                
                
    def hasOscilloscope(self):
        return self.hasInstrumentRole(roles.Oscilloscope)
    def hasSignalGenerator(self):
        return self.hasInstrumentRole(roles.SignalGenerator)
    def hasPowerSupply(self):
        return self.hasInstrumentRole(roles.PowerSupply)
    
    def hasMultimeter(self):
        return self.hasInstrumentRole(roles.MultiMeter)
    
    @property 
    def dso(self) -> InstrumentBase:
        return self.oscilloscope
    
    @property 
    def oscilloscope(self) -> InstrumentBase:
        if self._dso is None:
            self._dso = self.generateInstrument(roles.Oscilloscope)
        return self._dso 
    
    @property 
    def signalGenerator(self) -> InstrumentBase:
        
        if self._siggen is None:
            self._siggen = self.generateInstrument(roles.SignalGenerator)
            
        return self._siggen
    
    
    @property 
    def psu(self) -> InstrumentBase:
        return self.powerSupply
    @property 
    def powerSupply(self)  -> InstrumentBase:
        if self._benchsupply is None:
            self._benchsupply = self.generateInstrument(roles.PowerSupply)
        return self._benchsupply
    
    @property 
    def dmm(self)  -> InstrumentBase:
        return self.multimeter
    
    @property 
    def multimeter(self)  -> InstrumentBase:
        if self._dmm is None:
            self._dmm = self.generateInstrument(roles.MultiMeter)
        return self._dmm
    
    