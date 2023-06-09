# Instrument: Unitrend UT880x digital multimeter

This has been tested on the UT8804N DMM.  Unlike most devices here, it is *not* 
an SCPI-controlled device and uses both a weird serial protocol and a CP2110 USB-Serial connection.

The main caveats with this instrument are that

	* only measurements available from the current physical selector position are available (i.e. turn the knob)
	* it is normally used asynchronously, with event listeners rather than polled
	



This is actually a distinct project, merged into the psytestbench, and is frankly still rather messy.



### instantiation

You basically only need the usb bus path for the device, or anything pyserial's serial.serial_for_url will accept.  
However, this bus location depends on where/when you plug the device in--annoying.  

So the library implements a bit of a hack to allow you to specify a path as

usb:VENDOR_ID:PRODUCT_ID

and it will then determine the correct path for you.

Instatiation can then be manual

```
   from psytestbench.ut880x.instrument import Instrument as Multimeter
   dmm = Multimeter('usb:10c4:ea80')
```

Or set it up as part of a LabInstruments object, which will handle lazy initialization
and only connect to instruments as they are used for the first time.  
You can see `examples/mylab.py` and the `examples/console.py` which 
uses the lab instrument collection, but is basically

```

# get the classes for the specific devices I actually have
from psytestbench.ds1000z.instrument import Instrument as OScope
from psytestbench.spd3303x.instrument import Instrument as BenchSupply
from psytestbench.utg9xx.instrument import Instrument as SigGen
from psytestbench.ut880x.instrument import Instrument as Multimeter

# init the lab instrument collection with a list of tuples
# (DEVICE_CLASS, ID)

Lab = LabInstruments([
        (OScope,        'USB0::6833::1230::DS1ZA181104442::0::INSTR'),
        (BenchSupply,   'USB0::1155::30016::SPD3EGFQ6R2092::0::INSTR' ),
        (SigGen,        'USB0::26198::2100::3568543393::0::INSTR'),
        (Multimeter,    'usb:10c4:ea80')
        ],
        autoconnect=True)
```

From there you can use the various instruments configured, e.g.

```
Lab.dmm.monitoring = True
# etc
```


### sample usage

In the most manual case, you setup a listener for measurement events and poll() the DMM periodically to process incoming data.

A better example is in `examples/dmm_logger.py` which demonstrates asynchronous event generation, so you don't have to poll manually.


```

from psytestbench.ut880x.instrument import Listener, ReplyCode, Measurement, ValueWithPrecision
import psytestbench.examples.mylab 

import logging 
log = logging.getLogger(__name__)

# this is a class derived from the DMM listener to output measurements received
class DMMEventListener(Listener):
    def dumpReading(self, name, val:ValueWithPrecision):
        print(f'{name}: {val.value_string} {val.units}')
        
    def measurement(self, m:Measurement):
        print(f'Measurement')
        for vname in m.valueNames:
            self.dumpReading(vname, m.valueByName(vname))
        log.warn("Raw: %s" % str(m))
        
def main():
    lab = psytestbench.examples.mylab.Lab
    # add the listener to the DMM
    listener = DMMEventListener()
    lab.dmm.listenerAdd(listener)
    
    # enable monitoring of the DMM
    lab.dmm.monitoring = True 
    try:
        for _i in range(400):
            lab.dmm.poll() # poll it manually (multiple measurements may be sent to listener)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    
    lab.dmm.monitoring = False
    lab.dmm.disconnect()
```

### License

This file is part of the Psychogenic Testbench (psytestbench).

Psytestbench is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Psytestbench. If not, see <https://www.gnu.org/licenses/>.


