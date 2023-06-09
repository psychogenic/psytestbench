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
import serial
import time
import logging 
log = logging.getLogger(__name__)


from psytestbench.psytb.instrument.instrument import Instrument

class SerialInstrument(Instrument):
    
    def __init__(self, devicePathorPort:str, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None):
        super().__init__()
        self._serdev = None
        try:
            if devicePathorPort.lower().find('://') >= 0:
                self._serdev = serial.serial_for_url(devicePathorPort, baudrate=baudrate)
            else:
                self._serdev = serial.Serial(devicePathorPort, baudrate, bytesize, parity, stopbits)
        
        except FileNotFoundError as ex:
            log.error(f"Could not find device {devicePathorPort}: {ex}")
            self._serdev = None
            
        except serial.SerialException as ex:
            log.error(f"Problem with serial {devicePathorPort}: {ex}")
            self._serdev = None
            
        if self._serdev is None:
            raise RuntimeError(f"Could not construct serial instrument {devicePathorPort}")
            
    
        
    def poll(self):
        raise NotImplemented
    
    def dump(self):
        b = self.read(10)
        while len(b):
            print(b)
            time.sleep(0.001)
            b = self.read(10)
            
    @property 
    def serialConn(self):
        return self._serdev
    def connect(self):
        if not self.serialConn.isOpen():
            self.serialConn.open()
            
    @property 
    def is_connected(self):
        if self._serdev is None or not self._serdev:
            return False 
        return self.serialConn.isOpen()
            

    def disconnect(self):
        if not self._serdev and self.serialConn.isOpen():
            return 
        self.serialConn.close()
        
    def write(self, v):
        return self.serialConn.write(v)
    
    def read(self, v:int=1):
        return self.serialConn.read(v)
    
    def read_all(self):
        return self.serialConn.read_all()
    
    def flush(self):
        return self.serialConn.flush()
    
    
    
        