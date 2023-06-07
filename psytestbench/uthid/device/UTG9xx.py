'''
Created on May 26, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''

import time
from psytestbench.uthid.comm.channel import Channel 
#from psytestbench.uthid.frame.frame import Frame 
from psytestbench.uthid.device.device import Device
#from psytestbench.uthid.event.listener import Listener

#from psytestbench.uthid.frame.response.factory.stream import StreamFactory


import logging 
log = logging.getLogger(__name__)



class UTG9xx(Device):
    def __init__(self, channel:Channel):
        self.channel = channel
        