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


from psytestbench.psytb.instrument import Instrument

class MultiMeter(Instrument):
    InstrumentTypeName = 'multimeter'
    
    def __init__(self, port=None, 
                 port_match=True, 
                 backend='', 
                 handshake=False, 
                 arg_separator=',', **resource_params):
        super().__init__(port, port_match, backend, handshake, arg_separator, 
                         **resource_params)
        