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

# get the lab instruments utility class
from psytestbench.lab.instruments import LabInstruments

# get the classes for the specific devices I actually have
from psytestbench.ds1000z.instrument import Instrument as OScope
from psytestbench.spd3303x.instrument import Instrument as BenchSupply
from psytestbench.utg9xx.instrument import Instrument as SigGen
from psytestbench.ut880x.instrument import Instrument as Multimeter


# these imports are just to make things more intuitive from user side
# see lowpass_characterize example.
from psytestbench.ut880x.instrument import Listener as DMMListener
from psytestbench.ut880x.instrument import Measurement as DMMMeasurement
from psytestbench.ut880x.instrument import ValueWithPrecision as DMMValueWithPrecision






# init the lab instrument collection with a list of tuples
# (DEVICE_CLASS, ID)

Lab = LabInstruments([
        (OScope,        'USB0::6833::1230::DS1ZA181104442::0::INSTR'),
        # (OScope,        'TCPIP::192.168.0.24::INSTR'),
        
        (BenchSupply,   'USB0::1155::30016::SPD3EGFQ6R2092::0::INSTR' ),
        (SigGen,        'USB0::26198::2100::3568543393::0::INSTR'),
        (Multimeter,    'usb:10c4:ea80')
        ],
        autoconnect=True)

# now when I
# Lab.oscilloscope etc the device will be instantiated
# and connected to


