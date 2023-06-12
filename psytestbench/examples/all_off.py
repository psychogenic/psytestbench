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
    
    # assumes auto-connect is true
    dso = lab.dso
    if dso and dso.is_connected:
        print("Turning everything off for DSO")
        for ch in dso.channels:
            ch.off()
        
        dso.stop()
    else:
        print("No DSO present")
        
    psu = lab.psu 
    if psu and psu.is_connected:
        print("Turning everything off for PSU")
        for ch in psu.channels:
            ch.off()
    else:
        print("No PSU present")
        
            
    
    
    siggen = lab.signalGenerator 
    if siggen and siggen.is_connected:
        print("Turning everything off for SigGen")
        for ch in siggen.channels:
            ch.off()
    else:
        print("No SigGen present")
    
    
    dmm = lab.dmm 
    if dmm and dmm.is_connected:
        print("Turning everything off for DMM")
        for ch in dmm.channels:
            ch.off()
    else:
        print("No DMM present")
    
    
    lab.disconnect()

main()
    
        
        