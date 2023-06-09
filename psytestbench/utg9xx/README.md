# Instrument: Unitrend UTG9xx Signal Generator

This has been tested on the UTG962 signal generator but should support others of the family.

This signal generator instrument has two output channels.

Other than connect/disconnect and locking, all the functionality happens 
through the two channels themselves.

Basic channel properties are accessed through channelN, e.g.

siggen.channel1.frequency(1000)
siggen.channel1.on()

but much of the functionality is accessed through channel attributes, namely:

    * mode (e.g. continuous, linear sweep, etc)
    * wave (e.g. sine, square etc)
    * sweep, which controls linear and log sweep settings


### sample usage

```
# get access
siggen = psytestbench.utg9xx.instrument.Instrument('USB0::26191::2100::3573542343::0::INSTR')
siggen.connect()
siggen.lock()

# set a 2khz square wave on 1
siggen.channel1.frequency(2000)
siggen.channel1.wave.square()

# set a 1-10kHz sine sweep on 2
siggen.channel2.wave.sine()
siggen.channel2.mode.sweepLinear()
siggen.channel2.sweep.frequencyStart(1000)
siggen.channel2.sweep.frequencyStop(10000)
siggen.channel2.sweep.time(5) # 5 seconds to sweep

# turn 'em on

siggen.channel1.on()
siggen.channel2.on()

# disconnect
siggen.disconnect() # auto unlocks

```

### License

This file is part of the Psychogenic Testbench (psytestbench).

Psytestbench is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Psytestbench. If not, see <https://www.gnu.org/licenses/>.


