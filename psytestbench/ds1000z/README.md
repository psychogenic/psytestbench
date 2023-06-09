# Instrument: Rigol MSO1000Z/DS1000Z series digital oscilloscopes

This has been tested on the DS1054Z DSO but should support



This instrument implements functions to control and query 
Rigol MSO1000Z/DS1000Z series digital oscilloscopes.
        
This object only has a few methods associated with it directly,
things like run(), stop() and single().
        
Most of the functionality is encapsulated in attributes which have
their own methods and/or sub-attributes, namely

    * channelN (channel1 to channel4) and channels (a list of all channels)
    * timebase
    * trigger
    * acquire
    * measure: control what is measured
    * measurement: get values for actual measurements
    
    
    
For instance, each channel allows you to turn it on()/off() or set 

    * scale
    * offset
    * bandwidth limit
    * coupling (e.g. AC, DC...)
and more.  

For specific details on each of these, help(dso.ATTRIBUTE) should do nicely.



### sample usage

```
# some address, can get from 
#  ds1000z.instrument.Instrument.listResources()
# while connected
devAddress = 'USB0::TODO::INSTR' 

# instantiate
dso =  ds1000z.instrument.Instrument(devAddress)

dso.connect()

# setup and turn on channels
dso.channel1.bandwidthLimit20MHz()
dso.channel1.couplingDC()
dso.channel1.on()

dso.channel2.bandwidthLimit20MHz()
dso.channel2.couplingAC()
dso.channel2.on()

# set the trigger mode, looking at low freqs here
dso.trigger.modeEdge()
dso.trigger.edge.source(dso.channel1)
dso.trigger.couplingLowpass()
dso.trigger.normal()


# I want these to be monitored/measured
# freq on 1 and V peak-to-peak on 1 and 2
dso.measure.frequency(dso.channel1)
dso.measure.vPP(dso.channel1)
dso.measure.vPP(dso.channel2)

# make certain we're acquiring
dso.run()


freq = dso.measurement.frequency(dso.channel1)
vpp = dso.measurement.vPP(dso.channel1)
postvpp = dso.measurement.vPP(dso.channel2)

# ... do things

```

### License

This file is part of the Psychogenic Testbench (psytestbench).

Psytestbench is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Psytestbench. If not, see <https://www.gnu.org/licenses/>.


