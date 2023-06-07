'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
import argparse
from enum import Enum 
from psytestbench.uthid.version import VERSION
import psytestbench.uthid.seldevice

import logging
log = logging.getLogger(__name__)

class LogLevel(Enum):
    debug = 'debug'
    info = 'info'
    warn = 'warn'
    error = 'error'

    def __str__(self):
        return self.value
    
class SelectedDevice(Enum):
    ut800x = 'ut800x'
    ut181a = 'ut181a'
    utg9xx = 'utg9xx'

    def __str__(self):
        return self.value

class CommandLine:
    ParsedArgs = None
    
    @classmethod 
    def getArgsParser(cls, scriptName:str):
        parser = argparse.ArgumentParser(description='%s (v%s)' % (scriptName, VERSION))
        cls.addBaseArguments(parser)
        return parser
    
    
    @classmethod 
    def addBaseArguments(cls, parser:argparse.ArgumentParser):

        parser.add_argument('--device', required=False, 
                            default=None, 
                            type=SelectedDevice, 
                            choices=list(SelectedDevice),
                            help="Select device")
        

        parser.add_argument('--csv', required=False, 
                            dest='csv', help="CSV file for logging (where applicable)")
        
        parser.add_argument('--repl', default=False, action='store_true', 
                            dest='repl', help="Enable REPL if available")
        
        parser.add_argument('--debug', action='append', nargs='+',
                            help="modules for which logging should "
                            "be forced to DEBUG "
                            "e.g. --debug pups.frame.response.measurement " 
                            "(may specify multiple)")
        
        
        parser.add_argument('--loglevel', required=False, 
                            default=LogLevel.warn, 
                            type=LogLevel, 
                            choices=list(LogLevel),
                            help="Set log level (verbosity)")
        

    @classmethod 
    def getArguments(cls, scriptName:str, parser:argparse.ArgumentParser=None):
        if parser is None:
            parser = cls.getArgsParser(scriptName)
        
        args = parser.parse_args()
        
        if args.device is not None:
            if args.device == SelectedDevice.ut800x:
                psytestbench.uthid.seldevice.setDeviceUT800x()
            elif args.device == SelectedDevice.ut181a:
                psytestbench.uthid.seldevice.setDeviceUT181A()
                
            elif args.device == SelectedDevice.utg9xx:
                psytestbench.uthid.seldevice.setDeviceUTG9xx()
            else:
                log.error("UNKNOWN SELECTED DEVICE??? %s" % args.device)
        
        
        # actually handle default args
        
        levs = {
            LogLevel.debug: logging.DEBUG,
            LogLevel.info: logging.INFO,
            LogLevel.warn: logging.WARN,
            LogLevel.error: logging.ERROR,
            
            
        }
        logging.basicConfig(level=levs[args.loglevel])
        
            
        if args.debug and len(args.debug):
            for alist in args.debug:
                for modname in alist:
                    aLogger = logging.getLogger(modname)
                    if aLogger:
                        log.info("Setting module %s to DEBUG" % modname)
                        aLogger.setLevel(logging.DEBUG)
            
        
        cls.ParsedArgs = args
        return args
    
    @classmethod
    def handleDefaultArguments(cls, scriptName:str=None, parser:argparse.ArgumentParser=None):
        args = cls.getArguments(scriptName, parser)
        return args
