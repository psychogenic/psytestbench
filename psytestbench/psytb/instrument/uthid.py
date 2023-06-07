'''
Created on Jun 6, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''

try:
    import hid 
    HIDLibraryIsPresent = True
except:
    HIDLibraryIsPresent = False 
    

import time
import threading

from psytestbench.psytb.instrument.serial import SerialInstrument

#from psytestbench.uthid.comm.channel import Channel 
from psytestbench.uthid.frame.frame import Frame 
from psytestbench.uthid.event.listener import Listener
# from psytestbench.uthid.frame.response.factory import Factory as ResponseFactory
from psytestbench.uthid.frame.response.factory.stream import StreamFactory


import logging 
log = logging.getLogger(__name__)



class UTHIDInstrument(SerialInstrument):
    
    @classmethod 
    def massagePathForSerial(cls, pathToHID):
        if pathToHID is None:
            if not HIDLibraryIsPresent:
                raise RuntimeError('No path passed and hid library not found to enumerate')
            
            numFound = 0
            for devs in hid.enumerate():
                if devs['product_string'].find('CP21') >= 0:
                    pathToHID = cls._hidpathToURL(devs['path'])
                    log.info(f"CP21xx device found: {devs['path']} ({devs['product_string']})")
                    numFound += 1
            
            if not numFound:
                raise RuntimeError('No CP2110 devices enumerated--cannot find DMM')
            if numFound > 1:
                log.warn("Multiple CP21xx devices found??? using last (pass path)")
                
        if pathToHID.lower().find('usb:') >= 0:
            vals = pathToHID.split(':')
            vendor_id = int(vals[1], 16)
            product_id = int(vals[2], 16)
            if not HIDLibraryIsPresent:
                raise RuntimeError('Passed a USB:VID:PID path but no hid library to enum!')
            
            for devs in hid.enumerate():
                if devs['vendor_id'] == vendor_id and devs['product_id'] == product_id:
                    pathToHID = cls._hidpathToURL(devs['path'])
        
        if pathToHID is None or not len(pathToHID):
            raise RuntimeError('Must pass some sort of path to UT HID instrument')
        
        return pathToHID
    
    @classmethod 
    def _hidpathToURL(cls, path:bytearray):
        decPath = path.decode('ascii')
        return f'cp2110://{decPath}'
    
    @classmethod 
    def monitor_thread(cls, hidObj):
        try:
            while hidObj.monitoring:
                hidObj.poll()
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass
    
    def __init__(self, pathToHID:str, commands):
        
        serPath = self.massagePathForSerial(pathToHID)
        super().__init__(serPath)
        
        
        self.factory = StreamFactory(self.serialConn)
        self.commands = commands
        self._monitor_thread = None
        self._monitoring = False
    
    @property 
    def channel(self):
        return self.serialConn
    
    @property 
    def monitoring(self):
        return self._monitoring
    
    @monitoring.setter 
    def monitoring(self, enable):
        resp = self.send(self.commands.Monitor(enable))
        self._monitoring = enable
        return self._checkResponse(resp)

    def disconnect(self):
        if not self.stopAsyncMonitoring():
            self.monitoring = False 
            
        super().disconnect()
        
        
    def send(self, frame:Frame):
        log.info("Sending frame \n%s" % str(frame))
        bts = frame.bytes
        log.debug("Bytes: %s" % bts)
        #self.flush()
        self.write(bts)
    
    def startAsyncMonitoring(self):
        if self._monitor_thread:
            return None
        
        self.monitoring = True
        self._monitor_thread = threading.Thread(target=self.monitor_thread(self), args=(self,), 
                                                daemon=True)
        self._monitor_thread.start()
        
        return self._monitor_thread
        
    def stopAsyncMonitoring(self):
        if not self._monitor_thread:
            return False 
        
        self.monitoring = False 
        self._monitor_thread.join()
        self._monitor_thread = None
        
        return True
        
    
    def poll(self):
        attempt = 0
        while attempt < 20:
            v = self.factory.poll()
            if v is not None:
                return v 
            time.sleep(0.005)
            attempt += 1
    
    
    
    # event notifier interface overrides 
    def listenerAdd(self, listener:Listener):
        self.factory.add(listener)
        
    def listenerRemove(self, listener:Listener):
        self.factory.remove(listener)
        
    def notify(self, response):
        self.factory.notify(response)
        
    def _checkResponse(self, resp):
        log.debug(f'RESPONSE {resp}')
    
        