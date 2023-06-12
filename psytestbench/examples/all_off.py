'''
Created on Jun 12, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''

import psytestbench.examples.mylab 



def main():
    lab = psytestbench.examples.mylab
    
    # assumes auto-connect is true
    dso = lab.dso
    if dso and dso.is_connected:
        for ch in dso.channels:
            ch.off()
        
        dso.stop()
        
    psu = lab.psu 
    if psu and psu.is_connected:
        for ch in psu.channels:
            ch.off()
            
    
    
    siggen = lab.signalGenerator 
    if siggen and siggen.is_connected:
        for ch in siggen.channels:
            ch.off()
    
    
    dmm = lab.dmm 
    if dmm and dmm.is_connected:
        dmm.stopAsyncMonitoring()
    
    
    lab.disconnect()

main()
    
        
        