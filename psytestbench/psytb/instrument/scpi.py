'''
Created on Jun 6, 2023

@author: Pat Deegan
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
import pyvisa 
import time


from psytestbench.psytb.instrument_roles.role import InstrumentRole

class SCPIInstrument(scpi.Instrument):
    ResourceManagerSingleton = None
    Role = None
    
    @classmethod 
    def role(cls) -> InstrumentRole:
        return cls.Role
    
    
    @classmethod 
    def listResources(cls):
        if SCPIInstrument.ResourceManagerSingleton is None:
            SCPIInstrument.ResourceManagerSingleton = pyvisa.ResourceManager()
        return SCPIInstrument.ResourceManagerSingleton.list_resources()
    
    def __init__(self, port=None, 
                 port_match=True, 
                 backend='', 
                 handshake=False, 
                 arg_separator=',', **resource_params):
        '''
        
         @param port: The name of the port to connect to. [Default: None]
         @param backend: The pyvisa backend to use for communication. [Defualt: '']
         @param handshake: Handshake mode. [Default: False]
         @param arg_separator: Separator to use between arguments. [Default: ',']
         @param resource_params: Arguments sent to the resource upon connection.
                https://pyvisa.readthedocs.io/en/latest/api/resources.html
         @returns: An Instrument communicator.

        
        '''
        super().__init__(port, port_match, backend, handshake, arg_separator, **resource_params)
        self.min_write_delay_s = 0
        
    def identity(self):
        val = self.query('*IDN?')
        if val is not None and len(val):
            return  val.rstrip().split(',')
        
    def connect(self):
        if self.is_connected:
            return 
        super().connect()

    def write(self, v):
        super().write(v)
        if self.min_write_delay_s:
            time.sleep(self.min_write_delay_s)
            
    
    