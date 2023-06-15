'''
Created on Jun 12, 2023

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

Quick utility to turn everything off (and demonstrate uniformity of _most_ interfaces)


'''

import psytestbench.examples.mylab 



def main():
    lab = psytestbench.examples.mylab.Lab
    
    # assumes auto-connect in LabInstruments collection is true
    instruments = {
       'DSO': lab.dso,
       'PSU': lab.psu,
       'SigGen': lab.signalGenerator,
       'DMM': lab.dmm   
       }
    
    
    for name, inst in instruments.items():
        if inst and inst.is_connected:
            print(f'Turning everything off for {name}')
            for ch in inst.channels:
                ch.off()
        else:
            print(f'No {name} present')
    
    
    lab.disconnect()

main()
    
        
        