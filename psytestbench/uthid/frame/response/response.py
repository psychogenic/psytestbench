'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

from psytestbench.uthid.frame.frame import Frame 
import psytestbench.uthid.seldevice

import logging 
log = logging.getLogger(__name__)

class RawResponse(Frame):
    def __init__(self, byteslist:bytearray):
        super().__init__()
        constants = psytestbench.uthid.seldevice.constants
        self.b = byteslist
        log.debug("Creating resp from %s" % str(byteslist))
        
        signatureFoundAt = byteslist.find(self.startSignature)
        if signatureFoundAt < 0:
            return 
        
        plen = self.payloadsize_from_rawbuffer(byteslist)
        startIdx = signatureFoundAt + self.minbufferlen_for_size()
        endIdx = startIdx + (plen - 2)
        log.debug('CHECK BYTES %s' % str(byteslist[endIdx:endIdx+2]))
        log.debug("Got sig, len: %i (full len %i), [%i,%i]" % (plen, len(byteslist), startIdx, endIdx))
                
        rcvdChecksum = int.from_bytes(byteslist[endIdx:endIdx+2], constants.byteorder)
        pload = byteslist[startIdx:endIdx]
        log.debug('pload %s' % str(pload))
        calcChecksum = self.checksum(plen.to_bytes(2, constants.byteorder) + pload )
        if rcvdChecksum == calcChecksum:
            log.debug("CHECKSUMS match: %i" % rcvdChecksum) 
            self.append(pload)
        else:
            log.info("CHECKSUMS mismatch: %s != %s" % (hex(rcvdChecksum), hex(calcChecksum)))
                    
                
                
                
                
                
                

class Response(Frame):
    def __init__(self, byteslist:bytearray):
        super().__init__(byteslist)
                

                