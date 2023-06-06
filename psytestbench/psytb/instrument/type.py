'''
Created on Jun 6, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''
from psytestbench.psytb.instrument_roles.role import InstrumentRole
class InstrumentType:
    def __init__(self, instrumentClass:type, resourceId:str=''):
        self.classType = instrumentClass 
        self.resourceId = resourceId 
        
    @property 
    def instrumentTypeName(self):
        return self.classType.InstrumentTypeName 
    
    def hasRole(self, role:InstrumentRole):
        return self.classType.role() == role
    
    def construct(self):
        ctype = self.classType 
        return ctype(self.resourceId)
    