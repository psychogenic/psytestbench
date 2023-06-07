'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

import logging 
log = logging.getLogger(__name__)

class Listener:
    ListIdCount = 0
    def __init__(self, lid:int=None):
        if lid is None:
            lid = Listener.ListIdCount
            Listener.ListIdCount += 1
            
        self._listid = id
        
        
    @property 
    def id(self):
        return self._listid
    
    def listenerNotify(self, resp):
        raise NotImplemented('listener notify: implement in subclass')
            

