'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

from psytestbench.uthid.frame.response.response import RawResponse
import psytestbench.uthid.frame.response.types as resptypes
import psytestbench.uthid.seldevice

import logging 
log = logging.getLogger(__name__)


class Factory:
    @classmethod 
    def construct(cls, byteslist:bytearray):
        r = RawResponse(byteslist)
        if len(r.payload):
            return cls.specify(r)
        return None 
    
    @classmethod 
    def specify(cls, r:RawResponse):
        constants = psytestbench.uthid.seldevice.constants
        try:
            t = constants.PacketType(r.payload[0])
        except:
            return None 
        
        typeToClassMap = {
            constants.PacketType.ReplyCode: resptypes.ReplyCode,
            # constants.PacketType.Measurement: resptypes.MeasurementRelative
            
            }
        if t in typeToClassMap:
            return typeToClassMap[t](r.payload)
        
        if t == constants.PacketType.Measurement:
            return resptypes.MeasurementFactory.construct(r.payload)
        
        