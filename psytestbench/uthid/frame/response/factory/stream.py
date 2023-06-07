'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
import time
from psytestbench.uthid.comm.channel import Channel
from psytestbench.uthid.frame.frame import Frame
from psytestbench.uthid.frame.response.factory.factory import Factory
from psytestbench.uthid.event import Notifier

import logging 
log = logging.getLogger(__name__)

from enum import Enum 
class StreamState(Enum):
    Idle = 0
    WaitingForSize = 1
    WaitingForPayload = 2
    
class StreamFactory(Notifier):
    def __init__(self, channel:Channel):
        super().__init__()
        self.channel = channel
        self.buf = bytearray()
        self.rawframe = Frame()
        self.state = StreamState.Idle
        self.startsig = self.rawframe.startSignature
        self.startsiglen = len(self.startsig)
        self.packetSize = 0
    
    def reset(self):
        self.buf = bytearray()
        self.state = StreamState.Idle
        return 
    
    def poll(self):
        time.sleep(0.001)
        inbytes = self.channel.read_all()
        while inbytes and len(inbytes):
            self.buf += inbytes 
            inbytes = self.channel.read_all()
            
        if not len(self.buf):
            return 
        
        if self.state == StreamState.Idle:
            if self.buf.find(self.startsig[0]) < 0:
                log.debug("No %s found, chuck" % hex(self.startsig[0]))
                # this is trash, chuck it
                self.reset()
                return
            if len(self.buf) >= self.startsiglen:
                log.debug("Finding start sig")
                startPos = self.buf.find(self.startsig)
                if startPos < 0:
                    # trash 
                    log.debug("No %s found, chuck" % str(self.startsig))
                    self.reset()
                    return
                
                # have start pos
                if startPos >= 0:
                    log.debug("Found %s @ %i" % (str(self.startsig), startPos))
                    self.buf = self.buf[startPos:]
                    #log.debug("BUF NOW %s" % str(self.buf))
                    self.state = StreamState.WaitingForSize
        
        if self.state == StreamState.WaitingForSize:
            if len(self.buf) < Frame.minbufferlen_for_size():
                return
            s = Frame.payloadsize_from_rawbuffer(self.buf)
            if not s:
                # got a 0 size... trash
                self.reset()
                return 
            
            if s > Frame.maxpacket_size():
                # something is wrong 
                log.debug("Frame too large (%i) -- ignoring" % s)
                self.buf = self.buf[Frame.signature_numbytes():]
                #log.debug("Buf reset to %s" % self.buf)
                self.state = StreamState.Idle
                return 
            self.packetSize = s
            log.debug("Expecting full packet size %i" % s)
            self.state = StreamState.WaitingForPayload
            
        if self.state == StreamState.WaitingForPayload:
            fullPacketSize = self.packetSize + Frame.minbufferlen_for_size()
            if len(self.buf) < fullPacketSize:
                #log.debug("Buf still < %i" % fullPacketSize)
                return 
            
            self.state = StreamState.Idle
            # have enough 
            frameBuf = self.buf[:fullPacketSize+1]
            # log.debug("Using framebuf %s" %str(frameBuf))
            self.state = StreamState.Idle
            v = Factory.construct(frameBuf)
            if v is not None:
                self.buf = self.buf[fullPacketSize:]
                self.notify(v)
                return v
            # this failed... try a bit further down
            self.buf = self.buf[Frame.signature_numbytes():]
                
            
    
    