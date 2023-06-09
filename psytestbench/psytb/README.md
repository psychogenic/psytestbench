# Psytestbench base classes

This is the repository of base and utility classes used by the testbench and only of interest if you are extending the library.

The most important sections are:

	* psytestbench.psytb.instrument base classes for various instrument types
	* psytestbench.psytb.instrument_roles which define the function types for instruments
	
This split allows for a hierarchy that isn't a giant inheritance mess and some instruments may be based of off something other
than some universal base class (e.g. the SCPI instruments are all built directly atop the easy-scpi Instrument class).

For use with the lab instrument collection, and as a way to share functionality that is logically common to instruments, the 
roles are set through composition.  E.g. the SPD3303x PSU

	* IS A scpi.Instrument
	* HAS A PowerSupply role which implements a ramp() method to go from voltage X to Y 
	
but any PSU, say based on some serial interface instead, can share the role and hence the ramp() functionality.

### License

This file is part of the Psychogenic Testbench (psytestbench).

Psytestbench is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Psytestbench. If not, see <https://www.gnu.org/licenses/>.


