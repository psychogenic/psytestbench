# Instrument: Siglent SPD3303X Bench Power Supply

This has been tested on the SPD3303C, can see and control it through the examples/benchsupply.py script.

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
	pwrsupply.measurement.voltage(pwrsupply.channel1) )
print(
	pwrsupply.measurement.current(pwrsupply.channel2) )
	
pwrsupply.channel3.on()
pwrsupply.channel1.off()
```

### License

This file is part of the Psychogenic Testbench (psytestbench).

Psytestbench is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Psytestbench. If not, see <https://www.gnu.org/licenses/>.


