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
'''


import argparse
from enum import Enum


import psytestbench.psytb.settings as settings
from psytestbench.psytb.instrument.instrument import Instrument
from psytestbench.psytb.instrument.scpi import SCPIInstrument

import logging 
log = logging.getLogger(__name__)

class LogLevel(Enum):
    debug = 'debug'
    info = 'info'
    warn = 'warn'
    error = 'error'

    def __str__(self):
        return self.value
    

class CLI:
    
    @classmethod 
    def listAvailableDevices(cls):
        return SCPIInstrument.listResources()
        
    
    @classmethod 
    def getArgsParser(cls, applicationName:str) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description=f'{applicationName} (testbench v {settings.VERSION})')
        cls.addStandardArguments(parser)
        return parser
    
    @classmethod 
    def addStandardArguments(cls, parser:argparse.ArgumentParser):
        
        parser.add_argument('--list', required=False, 
                            action='store_true',
                            dest='listdevices' ,
                            help="List all currently connected devices")
        
        parser.add_argument('--device', required=False, 
                            default='', 
                            type=str, 
                            help="Address of device")
        
        parser.add_argument('--loglevel', required=False, 
                            default=LogLevel.warn, 
                            type=LogLevel, 
                            choices=list(LogLevel),
                            help="Set log level (verbosity)")
        
        
    
    @classmethod 
    def handleStandardArguments(cls, args):
        
        levs = {
            LogLevel.debug: logging.DEBUG,
            LogLevel.info: logging.INFO,
            LogLevel.warn: logging.WARN,
            LogLevel.error: logging.ERROR,
        }
        logging.basicConfig(level=levs[args.loglevel])
        
        if args.listdevices:
            print('Available devices:')
            for d in cls.listAvailableDevices():
                print(d)
            print()
        
        
    
    @classmethod 
    def getArguments(cls, parser:argparse.ArgumentParser=None, applicationName:str='N/A'):
        if parser is None:
            parser = cls.getArgsParser(applicationName)
        
        args = parser.parse_args()
        
        cls.handleStandardArguments(args)
        
        return args

        
        
        
    