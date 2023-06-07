'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

#
from psytestbench.uthid.frame.response.response import Response
import psytestbench.uthid.seldevice
class ReplyCode(Response):
    def __init__(self, byteslist:bytearray):
        super().__init__(byteslist)
        
    @property
    def status(self):
        c = psytestbench.uthid.seldevice.constants
        try:
            return c.ReplyCode(self.payloadInt(1,2))
        except:
            return c.ReplyCode.Error
        
        
    def __str__(self):
        c = psytestbench.uthid.seldevice.constants
        if self.status == c.ReplyCode.OK:
            return 'ReplyCode: OK'
        return 'ReplyCode: ERROR'
        