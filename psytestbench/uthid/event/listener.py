'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
from psytestbench.psytb.event.listener import Listener as BaseListener
from psytestbench.uthid.frame.response.types import Response, ReplyCode, Measurement

import logging 
log = logging.getLogger(__name__)

class Listener(BaseListener):
    ListIdCount = 0
    def __init__(self, lid:int=None):
        super().__init__(lid)
        
    
    def listenerNotify(self, resp:Response):
        if isinstance(resp, Measurement):
            return self.measurement(resp)
        
        if isinstance(resp, ReplyCode):
            return self.replyCode(resp)
            
        
    
    def replyCode(self, reply:ReplyCode):
        # override me
        log.info("Got reply:\n%s" % str(reply))
    
    def measurement(self, m:Measurement):
        # override me
        log.info("Got measurement:\n%s" % str(m))

