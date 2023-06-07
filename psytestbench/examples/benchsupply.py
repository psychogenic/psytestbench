'''
Created on Jun 2, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
   This file is part of the Psychogenic Technologies testbench (psytestbench).

   psytestbench is free software: you can redistribute it and/or modify it under 
   the terms of the GNU General Public License as published by the Free Software 
   Foundation, either version 3 of the License, or (at your option) any later version.

   psytestbench is distributed in the hope that it will be useful, but WITHOUT ANY 
   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
   PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with psytestbench. 
If not, see <https://www.gnu.org/licenses/>.



This is a demo program that allows you to control a Siglent SPD3303 power supply.

It may be run from the command line to do things like set voltage/current limits, turn
outputs on/off, e.g.

List SPCI devices
$ python path/to/benchsupply.py --list


Set voltage and turn on channel 2
$ python path/to/benchsupply.py --device $DEVID --voltage_2 3.3 --on_2

Recall program 4 and turn on channel 1
$ python path/to/benchsupply.py --device $DEVID --recall 4 --on_1 --off_2

$DEVID is the SPCI identifier for your device.

The full --help is:


usage: benchsupply.py [-h] [--list] [--device DEVICE] [--loglevel {debug,info,warn,error}]
                      [--recall RECALL] [--voltage_1 VOLTAGE_1] [--voltage_2 VOLTAGE_2]
                      [--current_1 CURRENT_1] [--current_2 CURRENT_2] [--off_all]
                      [--off_1] [--on_1] [--off_2] [--on_2] [--off_3] [--on_3] [--measure]
                      [--settings]

Bench Supply CLI (testbench v 1.0.0)

options:
  -h, --help            show this help message and exit
  --list                List all currently connected devices
  --device DEVICE       Address of device
  --loglevel {debug,info,warn,error}
                        Set log level (verbosity)
  --recall RECALL       stored settings to recall [1-5]
  --voltage_1 VOLTAGE_1
                        Vout for channel 1
  --voltage_2 VOLTAGE_2
                        Vout for channel 2
  --current_1 CURRENT_1
                        Current limit for channel 1
  --current_2 CURRENT_2
                        Current limit channel 2
  --off_all             Outputs ALL OFF
  --off_1               Output 1 OFF
  --on_1                Output 1 ON
  --off_2               Output 2 OFF
  --on_2                Output 2 ON
  --off_3               Output 3 OFF
  --on_3                Output 3 ON
  --measure             Take measurements on 2 config channels
  --settings            Dump settings for 2 configurable channels

'''
from psytestbench.spd3303x.instrument import Channel, Instrument as BenchSupply
from psytestbench.psytb.cli import CLI 


import psytestbench.examples.mylab 

import logging 
log = logging.getLogger(__name__)

def prepareArgParser():
    parser = CLI.getArgsParser('Bench Supply CLI')
    parser.add_argument('--recall', required=False, 
                            default=0, 
                            type=int, 
                            help="stored settings to recall [1-5]")
    parser.add_argument('--voltage_1',
                        required=False, 
                        default=0, 
                        type=float, 
                        help="Vout for channel 1")
    parser.add_argument('--voltage_2',
                        required=False, 
                        default=0, 
                        type=float, 
                        help="Vout for channel 2")
    parser.add_argument('--current_1',
                        required=False, 
                        default=0, 
                        type=float, 
                        help="Current limit for channel 1")
    parser.add_argument('--current_2',
                        required=False, 
                        default=0, 
                        type=float, 
                        help="Current limit channel 2")
    
    
        
    parser.add_argument('--off_all', default=False, action='store_true',
                            dest='offALL' ,
                            help="Outputs ALL OFF")
        
    parser.add_argument('--off_1', default=False, action='store_true',
                            dest='offch1' ,
                            help="Output 1 OFF")
    
    parser.add_argument('--on_1', default=False, action='store_true',
                            dest='ch1' ,
                            help="Output 1 ON")
        
    parser.add_argument('--off_2', default=False, action='store_true',
                            dest='offch2' ,
                            help="Output 2 OFF")
        
    parser.add_argument('--on_2', default=False, action='store_true',
                            dest='ch2' ,
                            help="Output 2 ON")
    
    parser.add_argument('--off_3', default=False, action='store_true',
                            dest='offch3' ,
                            help="Output 3 OFF")
    
    parser.add_argument('--on_3', default=False, action='store_true',
                            dest='ch3' ,
                            help="Output 3 ON")
    
    
    parser.add_argument('--measure', default=False, action='store_true',
                            dest='takemeasurements' ,
                            help="Take measurements on 2 config channels")
    parser.add_argument('--settings', default=False, action='store_true',
                            dest='dumpsettings' ,
                            help="Dump settings for 2 configurable channels")
    
    return parser 


def getArgs():
    p = prepareArgParser()
    return CLI.getArguments(p)
    
def recall(dev:BenchSupply, idx):
    log.info(f'Recall {idx}')
    v = dev.recall(idx)
    log.debug(v)

def setVoltage(ch:Channel, setTo:float):
    log.info(f'set voltage {setTo}')
    v = ch.voltage(setTo)  
    log.debug(v)  
    
def setCurrent(ch:Channel, setTo:float):
    log.info(f'set current {setTo}')
    v = ch.current(setTo)
    log.debug(v)
    
def errorMsg(msg):
    log.warn(f'Issue: {msg}')
    print(f'\n\nERROR: {msg}\n\n')
    return -1

def dumpChannelMeasurements(dev:BenchSupply, ch:Channel):
    print(f'Measurement Channel {ch.id}')
    print(f'\tI: {dev.measurement.current(ch)}A\t  V: {dev.measurement.voltage(ch)}V')
    print( '---------------------------------')
    

def dumpCurrentMeasurements(dev:BenchSupply):
    for ch in [dev.channel1, dev.channel2]:
        dumpChannelMeasurements(dev, ch)
        
        
def dumpChannelSettings(dev:BenchSupply, ch:Channel):
    print(f'Settings Channel {ch.id}')
    print(f'\tIlim: {ch.current()}A\t  V: {ch.voltage()}V')
    print( '---------------------------------')
    

def dumpCurrentSettings(dev:BenchSupply):
    for ch in [dev.channel1, dev.channel2]:
        dumpChannelSettings(dev, ch)
    
        
def getBenchSupply(devAddress:str) -> BenchSupply:
    
    dev = BenchSupply(devAddress)
    dev.connect()
    if not dev.is_connected:
        errorMsg(f'Could not connect to {devAddress}')
        return None 
    return dev
    
def main():
    args = getArgs()
    
    if not args.device:
        if args.listdevices:
            return 
        
        dev = psytestbench.examples.mylab.Lab.psu 
        
        if dev is None:
            return errorMsg('You must pass a --device ADDRESS')
    
    else:
        dev = getBenchSupply(args.device)
    
    if args.recall:
        recall(dev, args.recall)
        
    if args.voltage_1:
        setVoltage(dev.channel1, args.voltage_1)
    
    if args.voltage_2:
        setVoltage(dev.channel2, args.voltage_2)
        
    if args.current_1:
        setCurrent(dev.channel1, args.current_1)
        
    if args.current_2:
        setCurrent(dev.channel2, args.current_2)
    
    if args.offALL:
        log.info("All outputs OFF")
        for ch in dev.outputs:
            ch.off()
             
    else:
        if args.offch1:
            log.info('CHANNEL 1 OFF')
            dev.channel1.off()
        elif args.ch1:
            log.info('CHANNEL 1 ON')
            dev.channel1.on()
        
        if args.offch2:
            log.info('CHANNEL 2 OFF')
            dev.channel2.off()
        elif args.ch2:
            log.info('CHANNEL 2 ON')
            dev.channel2.on()
        
        if args.offch3:
            log.info('CHANNEL 3 OFF')
            dev.channel3.off()
        elif args.ch3:
            log.info('CHANNEL 3 ON')
            dev.channel3.on()
        
    if args.dumpsettings:
        dumpCurrentSettings(dev)
    if args.takemeasurements:
        dumpCurrentMeasurements(dev)
    
    
main()
    