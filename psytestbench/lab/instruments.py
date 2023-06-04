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

import psytestbench.psytb.instrument_types as insttypes
from psytestbench.psytb.instrument import InstrumentType

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
        
        
    def hasInstrumentType(self, ofType) -> InstrumentType:
        for instType in self._instDetails:
            if instType.isSubclass(ofType):
                return instType
            
        return None
        
    def generateInstrument(self, ofType):
        instType = self.hasInstrumentType(ofType)
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
        return self.hasInstrumentType(insttypes.Oscilloscope)
    def hasSignalGenerator(self):
        return self.hasInstrumentType(insttypes.SignalGenerator)
    def hasPowerSupply(self):
        return self.hasInstrumentType(insttypes.PowerSupply)
    
    def hasMultimeter(self):
        return self.hasInstrumentType(insttypes.MultiMeter)
    
    @property 
    def dso(self) -> insttypes.Oscilloscope:
        return self.oscilloscope
    
    @property 
    def oscilloscope(self) -> insttypes.Oscilloscope:
        if self._dso is None:
            self._dso = self.generateInstrument(insttypes.Oscilloscope)
        return self._dso 
    
    @property 
    def signalGenerator(self) -> insttypes.SignalGenerator:
        
        if self._siggen is None:
            self._siggen = self.generateInstrument(insttypes.SignalGenerator)
            
        return self._siggen
    
    
    @property 
    def psu(self) -> insttypes.PowerSupply:
        return self.powerSupply
    @property 
    def powerSupply(self) -> insttypes.PowerSupply:
        if self._benchsupply is None:
            self._benchsupply = self.generateInstrument(insttypes.PowerSupply)
        return self._benchsupply
    
    @property 
    def dmm(self) -> insttypes.MultiMeter:
        return self.multimeter
    
    @property 
    def multimeter(self) -> insttypes.MultiMeter:
        if self._dmm is None:
            self._dmm = self.generateInstrument(insttypes.MultiMeter)
        return self._dmm
    
    