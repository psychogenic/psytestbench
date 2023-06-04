# psytestbench
Electronics Testbench Automation Library

(C) 2023 Pat Deegan, [psychogenic.com](https://psychogenic.com)

This library is a set of utilities and wrappers built-atop the awesome easy_scpi
to allow for simplified control of lab instruments.

It is a repository of interfaces for the electronics lab instruments used here, and by much of the maker community and other companies.

It's goal is to offer a sensibly uniform means of controlling power supplies, 
oscilloscopes, multimeters, signal generators and other tools that support SCPI.

## Current instruments supported
 * Siglent SPD3303x power supplies
 * Rigol DS1000Z/MSO1000Z series oscilloscopes (like the classic DS1054z)
 * Unitrend Uni-T UTG9xx signal generators (tested on the UTG962)

with more devices coming shortly, including DMM.

##examples

The examples directory has a few samples of the interfaces in use.  Most interesting may be the filterscan.py which uses the signal generator and oscope to characterize a low frequency, low pass filter.

### filterscan example

The signal gen sweeps frequencies using the siggen and measures input/output levels using the scope.

It has on-line --help


```
$ python psytestbench/examples/filterscan.py --help
usage: filterscan.py [-h] [--list] [--device DEVICE]
                     [--loglevel {debug,info,warn,error}] [--csv CSV]
                     [--freqmin FREQMIN] [--freqmax FREQMAX] [--step STEP]
                     [--numsamps NUMSAMPS] [--wave {sine,square,arb}]
                     [--amplitude AMPLITUDE] [--psu_program PSU_PROGRAM]
                     [--supply_voltage SUPPLY_VOLTAGE]

xfer function sweep (testbench v 1.0.0)

options:
  -h, --help            show this help message and exit
  --list                List all currently connected devices
  --loglevel {debug,info,warn,error}
                        Set log level (verbosity)
  --csv CSV             CSV file to output [/tmp/sweep.csv]
  --freqmin FREQMIN     start frequency 50
  --freqmax FREQMAX     start frequency 1200
  --step STEP           start frequency 10
  --numsamps NUMSAMPS   Num samples to average [2]
  --wave {sine,square,arb}
                        Select wave type [sine]
  --amplitude AMPLITUDE
                        Select wave amplitude (Volts) [0.4]
  --psu_program PSU_PROGRAM
                        PSU program to recall [1]
  --supply_voltage SUPPLY_VOLTAGE
                        PSU supply voltage (Volts) [3.3]


```


### interactive console

The console allows manual control of instruments defined in the lab.

Here's a small session controlling the power supply


```
$ python psytestbench/examples/console.py                                                                 
                                                                              
*********     Psychogenic Testbench Console     *********                       
Control instruments manually                                                    
                                                                                
* Lab instruments available *                                                   
        Power:          lab.powerSupply or lab.psu                              
        Sig gen:        lab.signalGenerator                                     
        o-scope:        lab.oscilloscope or lab.dso                             
  3/4 instrument types enabled.                                
     
>>> lab.psu.recall(1)
>>> lab.psu.channel1.voltage()
3.3
>>> lab.psu.channel1.voltage(3.14)
>>> lab.psu.channel1.voltage()
3.14
>>> lab.psu.channel1.on()
>>> lab.psu.measurement.voltage(lab.psu.channel1)
3.14


```
## todo

Make a nice package for python installation.
Bring in DMM support.
More tools.

## license 

The Psychogenic Technologies testbench (psytestbench) is released under the terms
of the GPL.

   psytestbench is free software: you can redistribute it and/or modify it under 
   the terms of the GNU General Public License as published by the Free Software 
   Foundation, either version 3 of the License, or (at your option) any later version.

   psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY 
   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
   PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with psytestbench. 
If not, see <https://www.gnu.org/licenses/>.
