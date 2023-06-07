'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
from psytestbench.uthid.comm.channel import Channel 
from psytestbench.uthid.device.UTHID import UTHID

import logging 
log = logging.getLogger(__name__)



class UT181A(UTHID):
    def __init__(self, channel:Channel):
        super().__init__(channel)
    
### debug/test
if __name__ == "__main__":
    # magic for device selection
    import psytestbench.uthid.seldevice
    psytestbench.uthid.seldevice.setDeviceUT181A()
    
    #from psytestbench.uthid.logger.measurement.stdout import StdOut as StdOutLogger
    from psytestbench.uthid.logger.measurement.csv import CSV as CSVLogger
    from psytestbench.uthid.debug.util import DebugUtils
    from psytestbench.uthid.comm.cp2110 import CP2110
    import psytestbench.uthid.frame.command as command
    import datetime
    logging.basicConfig(level=logging.INFO)
    chan = CP2110()
    d = UT181A(chan)
    d.begin()
    monOn = command.Monitor(True)
    monOff = command.Monitor(False) 
    togHold = command.ToggleHold()
    d.open()
    #r = d.send(togHold)
    
    me = CSVLogger('/tmp/datacol.csv', datetime.timedelta(milliseconds=200))
    
    v = d.send(monOn)
    me.begin()
    d.addListener(me) 
    
    
    #r = d.send(monOn)
    DebugUtils.REPLLaunchIfEnabled(globals(), "Device 'd' available")