'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

import ctypes 

c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16
c_uint64 = ctypes.c_uint64

import logging 
log = logging.getLogger(__name__)


class BitfieldStructure(ctypes.LittleEndianStructure):
    @property 
    def fields(self):
        return list(map(lambda x: x[0], self._fields_))
    
    def byName(self, name:str):
        return getattr(self, name)

class BitfieldUnion(ctypes.Union):
    '''
        Bitfield union: allows a bitfield to be accessed by:
          -- bit/bitset name
          -- actual byte(s) value for entire set
        
        To use
        1) define the bitfield as a BitfieldStructure derivative
        2) define the union as a BitfieldUnion
        
        The structure is where most of the work occurs.  
        
        From there, defining _fields_ in the union may be all the work required, e.g.
        
            class ASICStat(BitfieldUnion):   
                _fields_ = [(BitfieldUnion.bitsName, ASICStat_bits),
                            (BitfieldUnion.bytesName, c_uint8)]
                            
        From this point, all the bitsets defined in the ASICStat_bits are available
        on the object:
            a = Whatever(0xaa)
            a.somefield = 42
            print(a.another)
            # etc
        and the entire object may be interpreted as an int:
            print(hex(a))
        for the entire bitfield, or explicitly
            print(hex(a.bytes))
        

    '''
    bitsName = "b"
    bytesName = "asReg"
    def __init__(self, iniVal:int=None):
        #log.debug("BitfieldUnion c'tor")
        super().__init__()
        if iniVal is not None:
            self.asReg = iniVal
            
        self.publicFields = None
        
    def __dir__(self):
        if self.publicFields is not None:
            return self.publicFields
        return self.b.fields

    def valueUpdated(self):
        pass
        
    @property 
    def bytes(self):
        return self.asReg
    
    @bytes.setter
    def bytes(self, setTo:int):
        if setTo != self.asReg:
            self.asReg = setTo
            self.valueUpdated()
    
    
    def __str__(self):
        '''
            Generates a 
             name=value
            set of strings, for debug.
            
            @return: the actual output string
        '''
        retStrs = []
        if self.publicFields is not None:
            fieldset = self.publicFields
        else:
            fieldset = self.b.fields
        for f in fieldset:
            v = self.b.byName(f)
            try:
                retStrs.append(" %s=%s" % (f, hex(v)))
            except:
                retStrs.append(" %s=%s" % (f, str(v)))
                
        
        return "\n".join(retStrs)
        
    def __int__(self):
        return self.bytes
    def __index__(self):
        return self.bytes
    
    def __getattr__(self, name):
        try:
            if hasattr(self.b, name):
                v = getattr(self.b, name) 
                return v 
        except:
            pass
        raise AttributeError
        
    def __setattr__(self, name:str, val):
        try:
            if hasattr(self, 'b') and hasattr(self.b, name):
                origVal = self.asReg
                setattr(self.b, name, val)  
                if self.asReg != origVal:
                    self.valueUpdated()
                   
            else:
                super().__setattr__(name, val)
            return
        except Exception as e:
            log.error('Error: %s' % str(e))
        
        
    