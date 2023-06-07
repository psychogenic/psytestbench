'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

from psytestbench.psytb.event.listener import Listener

class Notifier:
    def __init__(self):
        self._listmap = {}
        
    def add(self, listener:Listener):
        self._listmap[listener.id] = listener
        
    def remove(self, listener:Listener):
        if not listener.id in self._listmap:
            return 
        
        del self._listmap[listener.id]
        
    def notify(self, response):
        for aList in self._listmap.values():
            aList.listenerNotify(response)