'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
import time
from psytestbench.uthid.comm.channel import Channel 
from psytestbench.uthid.frame.frame import Frame 
from psytestbench.uthid.seldevice import constants
import psytestbench.uthid.frame.command as commands
import psytestbench.uthid.frame.response.types as resptypes
from psytestbench.uthid.event.listener import Listener

import logging 
log = logging.getLogger(__name__)



class Device:
    def __init__(self, channel:Channel):
        self.channel = channel 
        self._monitoring = False 
        self.listeners = []
        
        
    def begin(self):
        self.channel.begin()
        
    @property 
    def monitoring(self):
        return self._monitoring
    
    @monitoring.setter 
    def monitoring(self, enable):
        resp = self.send(commands.Monitor(enable))
        self._monitoring = enable
        return self._checkResponse(resp)
        
                
        
    def setMode(self, mode:constants.Mode):
        return self._checkResponse(self.send(commands.SetMode(mode)))

        
    def open(self, params=None):
        return self.channel.open(params)
    
    def close(self):
        return self.channel.close()
    
    def read(self, size:int=1, timeout:int=1):
        return self.channel.read(size, timeout)
                                 
    def write(self, bytelist:bytearray):
        return self.channel.write(bytelist)
    
    def flush(self):
        self.channel.flush()
    
    def send(self, frame:Frame):
        log.info("Sending frame \n%s" % str(frame))
        bts = frame.bytes
        log.debug("Bytes: %s" % bts)
        self.flush()
        self.write(bts)
        
        
    def poll(self):
        raise NotImplemented
    
    def dump(self):
        b = self.read(10)
        while len(b):
            print(b)
            time.sleep(0.001)
            b = self.read(10)
            
    
        
        
    def _checkResponse(self, resp:resptypes.ReplyCode):
        if not resp:
            return False 
        if not isinstance(resp, resptypes.ReplyCode):
            return True # whatevs
        if resp.status != constants.ReplyCode.OK:
            return False 
        return True 
    
   
    def addListener(self, listener:Listener):
        self.listeners.append(listener)
        
### debug/test
if __name__ == "__main__":
    from psytestbench.uthid.debug.util import DebugUtils
    from psytestbench.uthid.comm.cp2110 import CP2110
    import psytestbench.uthid.frame.command as command
    logging.basicConfig(level=logging.DEBUG)
    chan = CP2110()
    d = Device(chan)
    monOn = command.Monitor(True)
    monOff = command.Monitor(False) 
    togHold = command.ToggleHold()
    d.open()
    DebugUtils.REPLLaunchIfEnabled(globals(), "Device 'd' available")
        
     
         