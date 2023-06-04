'''
Created on Jun 4, 2023

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

import readline
import code
import rlcompleter
import logging 

import psytestbench.examples.mylab 

from psytestbench.lab.instruments import LabInstruments

log = logging.getLogger(__name__)

def launchREPL(glob):
    readline.parse_and_bind("tab: complete")
    readline.set_completer(rlcompleter.Completer(glob).complete)
    code.InteractiveConsole(locals=glob).interact()

def dumpCapabilities(l:LabInstruments):
    print("* Lab instruments available *")
    capCount = 0
    if l.hasPowerSupply():
        print('\tPower:\t\tlab.powerSupply or lab.psu')
        capCount += 1
    if l.hasSignalGenerator():
        print('\tSig gen:\tlab.signalGenerator')
        capCount += 1
    if l.hasOscilloscope():
        print('\to-scope:\tlab.oscilloscope or lab.dso')
        capCount += 1
    if l.hasMultimeter():
        print('\tDMM:\tlab.multimeter or lab.dmm')
        capCount += 1
    print(f'  {capCount}/4 instrument types enabled.')
    print()
if __name__ == '__main__':
    lab = psytestbench.examples.mylab.Lab
    print('\n\n')
    print("*********     Psychogenic Testbench Console     *********")
    print("Control instruments manually\n")
    dumpCapabilities(lab)
    autoconn = 'OFF'
    if lab.autoconnect:
        autoconn = 'ON'
    print(f"Autoconnect is {autoconn}")
    print('\n\n')
    
    launchREPL(globals())
    
    