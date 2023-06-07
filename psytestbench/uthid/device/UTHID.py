'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
import time
from psytestbench.uthid.comm.channel import Channel 
from psytestbench.uthid.frame.frame import Frame 
from psytestbench.uthid.device.device import Device
from psytestbench.uthid.event.listener import Listener
# from psytestbench.uthid.frame.response.factory import Factory as ResponseFactory
from psytestbench.uthid.frame.response.factory.stream import StreamFactory


import logging 
log = logging.getLogger(__name__)



class UTHID(Device):
    def __init__(self, channel:Channel):
        self.channel = channel 
        self.factory = StreamFactory(channel)
    
    def send(self, frame:Frame):
        log.info("Sending frame \n%s" % str(frame))
        super().send(frame)
        
    def poll(self):
        attempt = 0
        while attempt < 20:
            v = self.factory.poll()
            if v is not None:
                return v 
            time.sleep(0.03)
            attempt += 1
            
            
    def keepPolling(self):
        try:
            while True:
                self.poll()
        except:
            return
        
    def addListener(self, listener:Listener):
        self.factory.add(listener)
        