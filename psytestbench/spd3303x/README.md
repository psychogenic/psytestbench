# Instrument: Siglent SPD3303X Bench Power Supply

This has been tested on the SPD3303C, can see and control it through the examples/benchsupply.py script.

The power supply has a few methods of its own, like the various
tracking method setters and a measurements attribute, but most of the 
functionality is through the channels themselves.
         
This PSU has 3 channels:

	* #1 and #2 are programmable
	* #3 is 2v5, 3v3 or 5v (set manually with a switch)

Each channel is accessible with the .channeln accessor and has 
relevant methods, e.g. 

```
    psu = psytestbench.spd3303x.instrument.Instrument('USB0::1155 ... ')

    psu.channel2.voltage(4.2)
    psu.channel2.on()
```

Only the on()/off() methods are relevant to channel 3.

Setting and querying present values is through the same methods, with 
no parameters

```
    v = psu.channel1.voltage()
    i = psu.channel1.current()
```

If you want the actual measured values, these are access through a 
'measurement' attribute:


```
    measuredV = psu.measurement.channel1.voltage
    measuredI = psu.measurement.channel1.current
````


### instantiation

You basically only need the SCPI identifier for the device.  This can be discovered through the `listResources` 
class method on any of the SCPI-based instrument classes, e.g.

```
   from psytestbench.spd3303x.instrument import Instrument as BenchSupply 
   
   print(BenchSupply.listResources())
```

This method returns a tuple of all the discovered SCPI devices.  The device of interest should be rather obvious.

From there, either instantiate directly

```
	myPSU = BenchSupply('USB0::1235::31563::SPD3XGEQ4R1841::0::INSTR')
```

using the appropriate identifier or set it up as part of a LabInstruments object, which will handle lazy initialization
and only connect to instruments as they are used for the first time.  You can see `examples/mylab.py` and the `examples/console.py` which 
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
Lab.psu.channel1.on()
```


### sample usage

```
# some address, can get from 
#  spd3303x.instrument.Instrument.listResources()
# while connected
devAddress = 'USB0::1235::31563::SPD3XGEQ4R1841::0::INSTR' 

# instantiate
pwrsupply =  spd3303x.instrument.Instrument(devAddress)

# recall previous program
pwrsupply.recall(3)

# change voltage on output channel 2
pwrsupply.channel2.voltage(3.25)

# change current limit on channel 1
pwrsupply.channel1.current(0.250)

# turn both on
pwrsupply.channel1.on()
pwrsupply.channel2.on()

# measure output voltage/current 
print(
	pwrsupply.measurement.channel1.voltage )
print(
	pwrsupply.measurement.channel2.current)
	
pwrsupply.channel3.on()
pwrsupply.channel1.off()
```

### License

This file is part of the Psychogenic Testbench (psytestbench).

Psytestbench is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Psytestbench. If not, see <https://www.gnu.org/licenses/>.


