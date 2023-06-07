'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

class Channel:
    def __init__(self, someName:str):
        self._name = someName 
        
    @property 
    def name(self):
        return self._name
    
    def begin(self):
        pass 
    
    def open(self, params=None):
        raise NotImplemented
    
    def read(self, size:int=0, timeout:int=0) -> bytearray:
        raise NotImplemented
    
    def write(self, byteslist:bytearray):
        raise NotImplemented
    
    def close(self):
        raise NotImplemented
    
    def flush(self):
        raise NotImplemented