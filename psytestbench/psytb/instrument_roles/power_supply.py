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

import time

from psytestbench.psytb.instrument_roles.role import InstrumentRole

class PowerSupply(InstrumentRole):
    InstrumentRoleName = 'power supply'
    

    @classmethod
    def name(cls):
        return PowerSupply.InstrumentRoleName
    
    
    @classmethod 
    def ramp(cls, voltageSetter,
             startValue:float, 
             endValue:float, step:float, 
             delaySeconds:float=0.03):
        
        goingUp = True 
        if startValue <= endValue:
            if step <= 0:
                raise ValueError(f'Ramp ({startValue},{endValue},{step} will never end')
            goingUp = True 
        elif startValue > endValue:
            if step >= 0:
                raise ValueError(f'Ramp ({startValue},{endValue},{step} will never end')
            goingUp = False
            
        
        v = startValue 
        
        isDone = False
        while not isDone:
            voltageSetter(v) 
            
            v += step 
            if goingUp:
                if v >= endValue:
                    isDone = True 
            else:
                if v <= endValue:
                    isDone = True 
            
            time.sleep(delaySeconds)
            
        voltageSetter(endValue)
                    
                
                
                
        
        
