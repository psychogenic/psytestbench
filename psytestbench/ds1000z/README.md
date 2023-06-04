# Instrument: Rigol MSO1000Z/DS1000Z series digital oscilloscopes

This has been tested on the DS1054Z DSO.

### sample usage

```
# some address, can get from 
#  ds1000z.instrument.Instrument.listResources()
# while connected
devAddress = 'USB0::TODO::INSTR' 

# instantiate
dso =  ds1000z.instrument.Instrument(devAddress)

```

### License

This file is part of the Psychogenic Testbench (psytestbench).

Psytestbench is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Psytestbench. If not, see <https://www.gnu.org/licenses/>.


