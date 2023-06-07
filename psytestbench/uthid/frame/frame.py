'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

from enum import Enum
import struct
import psytestbench.uthid.seldevice

import logging 
log = logging.getLogger(__name__)



class Frame:
    
    @classmethod 
    def maxpacket_size(cls):
        return psytestbench.uthid.seldevice.constants.MaxPacketSize
    
    @classmethod
    def signature_numbytes(cls):
        return psytestbench.uthid.seldevice.constants.SignatureNumBytes
    @classmethod 
    def minbufferlen_for_size(cls):
        constants = psytestbench.uthid.seldevice.constants
        return constants.SignatureNumBytes + constants.PacketsizeNumBytes
    @classmethod 
    def payloadsize_from_rawbuffer(cls, buf:bytearray):
        constants = psytestbench.uthid.seldevice.constants
        minlen = cls.minbufferlen_for_size()
        if len(buf) < minlen:
            return 0 
        
        sizebytes = buf[constants.SignatureNumBytes:minlen]
        fstr = '%sH' % cls.endianness_formatstr(constants.byteorder)
        return struct.unpack(fstr, sizebytes)[0]
    
    @classmethod 
    def int_to_bytes(cls, v, byteorder): 
        numFull = v.bit_length() // 8 
        rem = v.bit_length() % 8 
        if rem:
            numFull += 1 
            
        if numFull == 0:
            numFull = 1
        log.debug("Converting %s to bytes (%i bytes)" % (hex(v), numFull))
        asbytes =  v.to_bytes(numFull, byteorder)
        log.debug("Returning %s" % str(asbytes))
        return asbytes
        
    @classmethod 
    def endianness_formatstr(cls, byteorder):
        s = '<'
        if byteorder == 'big':
            s = '>'
        return s
    @classmethod
    def float_formatstr(cls, byteorder): 
        fstr = '%sf' % cls.endianness_formatstr(byteorder)
        return fstr
    
    @classmethod
    def float_to_bytes(cls, v:float, byteorder): 
        fstr = cls.float_formatstr(byteorder)
        return struct.pack(fstr, v)
    
    def __init__(self, payloadAppend:list=None):
        constants = psytestbench.uthid.seldevice.constants
        self._magicsig = self.int_to_bytes(constants.Signature, constants.byteorder)
        self.payload = [] 
        self._checksum = 0
        if payloadAppend is not None:
            self.append(payloadAppend)


    @property 
    def startSignature(self):
        return self._magicsig
    @property 
    def bytes(self):
        
        constants = psytestbench.uthid.seldevice.constants
        
        b = bytearray()
        for i in map(lambda x: self.int_to_bytes(x, constants.byteorder), self.payload):
            b += i
        
        plen = len(b) + 2 
        tochecksum = plen.to_bytes(2, constants.byteorder) + b 
        
        all_bytes = self._magicsig + tochecksum \
                        +  self.checksum(tochecksum).to_bytes(2, 
                                                              constants.byteorder)
        return all_bytes
    
    
    def payloadInt(self, index:int, endIdx:int=None):
        constants = psytestbench.uthid.seldevice.constants
        if endIdx is None:
            endIdx = index
        v = self.payload[index:endIdx+1]
        return int.from_bytes(v, byteorder=constants.byteorder)
    
    def payloadFloat(self, index:int):
        constants = psytestbench.uthid.seldevice.constants
        struct.unpack
        fstr = self.float_formatstr(constants.byteorder)
        return struct.unpack(fstr, bytearray(self.payload[index: index+4]))[0]
    
    def payloadString(self, index:int, maxlen:int=0):
        maxPoss = len(self.payload) - index
        if maxlen > maxPoss or maxlen < 1:
            maxlen = maxPoss
        retstr = ''
        for i in range(index, index+maxlen):
            if self.payload[i]:
                retstr += chr(self.payload[i])
                
        return retstr
    
    def append(self, appVal):
        constants = psytestbench.uthid.seldevice.constants
        #log.debug("Append %s" % str(appVal))
        if isinstance(appVal, Enum):
            #log.debug("append enum")
            self.payload.append(appVal.value)
        elif isinstance(appVal, int):
            #log.debug("append int")
            self.payload.append(appVal)
        elif isinstance(appVal, float):
            #log.debug("append float")
            for i in self.float_to_bytes(appVal, constants.byteorder):
                self.payload.append(i)
        else:
            for i in appVal:
                #log.debug("append from list")
                self.append(i)
                
    
    
    def checksum(self, b):
        log.debug("CALC CHECKSUM ON %s" % str(b))
        return sum(b)
    
        
           
### debug/test
if __name__ == "__main__":
    from psytestbench.uthid.debug.util import DebugUtils
    
    f = Frame()
    f.append([psytestbench.uthid.seldevice.constants.Command.Monitor, 0x1])
    DebugUtils.REPLLaunchIfEnabled(globals(), "Frame class available, instance 'f'")
        
     
        