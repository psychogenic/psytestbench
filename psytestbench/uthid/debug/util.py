'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
import readline
import code
import rlcompleter
import logging 


log = logging.getLogger(__name__)


class DebugUtils:
    DEBUG_SCRIPTS_REPL_ENABLE = True
    @classmethod 
    def dumpByteArray(cls, barray):
        print(cls.bytesToString(barray))
        
    @classmethod 
    def bytesToString(cls, barray):
        outStrs = []
        for b in barray:
            outStrs.append(hex(b))
        
        return ','.join(outStrs)
    
    @classmethod 
    def repl(cls, glob):
        readline.parse_and_bind("tab: complete")
        readline.set_completer(rlcompleter.Completer(glob).complete)
        code.InteractiveConsole(locals=glob).interact()
        
        
    @classmethod 
    def REPLLaunchIfEnabled(cls, glob, helpstr:str=None):
        if not cls.DEBUG_SCRIPTS_REPL_ENABLE:
            log.debug("NOT launching REPL")
            print()
            return

        log.debug("launching REPL")
        
        print("\n\n")
        stars = ' ' + '*'*60
        print(stars)
        print(' '*20 + 'Launching REPL shell')

        if helpstr is not None and len(helpstr):
            print()
            print('  ' + helpstr)
            print()
        
        print(stars)
        cls.repl(glob)
        
        