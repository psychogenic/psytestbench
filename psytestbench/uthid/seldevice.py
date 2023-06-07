'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''


# import psytestbench.uthid.constants.UT880x as as constants
import psytestbench.uthid.constants.UT880x as UT800x
import psytestbench.uthid.constants.UT181A as UT181A

constants = None

def setDeviceUT181A():
    global constants 
    constants = UT181A
    
def setDeviceUT800x():
    global constants 
    constants = UT800x
    
