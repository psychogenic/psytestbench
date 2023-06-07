'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''


import psytestbench.uthid.seldevice 
from psytestbench.uthid.frame.response.response import Response

import logging 
log = logging.getLogger(__name__)


class ValueWithPrecision:
    def __init__(self, val:float=0.0, precInit:int=0, units:str='N/A'):
        self.value = val 
        self.precision = psytestbench.uthid.seldevice.constants.Precision(precInit)
        self.units = units
        self.seconds = 0
        
        
    @property 
    def value_string(self):
        if self.precision and self.precision.digits:
            formatted = f'{{:.{self.precision.digits}f}}'
            
            return formatted.format(self.value)
        
        return '%.5f' % self.value
        
    def __str__(self):
        return f'{self.value_string} {self.units}'

class Measurement(Response):
    def __init__(self, byteslist:bytearray):
        super().__init__(byteslist)
        constants = psytestbench.uthid.seldevice.constants
        self.misc1 = constants.MiscByte1(self.payload[1])
        self.misc2 = constants.MiscByte2(self.payload[2])
        modeVal = self.payloadInt(3, 4)
        try:
            self.mode = constants.Mode(modeVal)
        except ValueError:
            log.error("UNKNOWN MODE: %s (is this the right device?)" % hex(modeVal))
            self.mode = None
            
        self.range = constants.Range(self.payload[5])
        self.startIdx = 6
        
        self.valuesByNameMap = dict()
        
    @property 
    def rangeAuto(self):
        return self.misc2.autoRange
    
    
    @property 
    def rangeManual(self):
        if self.rangeAuto:
            return False 
        return True
    
    
    @property 
    def highVoltage(self):
        return self.misc2.highVoltage
    
    @property 
    def leadError(self):
        return self.misc2.leadError
    
    @property 
    def compMode(self):
        return self.misc2.compMode
        
    @property 
    def recordMode(self):
        return self.misc2.recordMode


    @property 
    def aux1_present(self):
        return self.misc1.aux1
    
    @property 
    def aux2_present(self):
        return self.misc1.aux2
    @property 
    def bargraph_present(self):
        return self.misc1.bargraph

    @property 
    def format(self):
        return self.misc1.format
    @property 
    def hold(self):
        return self.misc1.hold
    
        
    def extractValueWithPrecision(self,startIdx:int, saveAsAttrib:str, 
                                  includeUnits=True):
        curIdx = startIdx
        log.debug("extractValueWithPrecision starting @ %i" % curIdx)
        if curIdx + 5 >= len(self.payload):
            log.error("Not enough space left for value-with-precision!")
             
            setattr(self, saveAsAttrib, ValueWithPrecision())
            return 0 
        
        val = self.payloadFloat(curIdx)
        curIdx += 4
        precInit = self.payload[curIdx]
        curIdx += 1
        unitstr = ''
        if includeUnits:
            unitstr = self.payloadString(curIdx, 8)
            curIdx += 8 # 0-term
        log.debug("Got %.3f %s" % (val, unitstr))
        v = ValueWithPrecision(val, precInit, unitstr)
        setattr(self, saveAsAttrib, v)
        self.valuesByNameMap[saveAsAttrib] = v
        return curIdx - startIdx
    
    @property 
    def valueNames(self):
        return sorted(list(self.valuesByNameMap.keys()))
    
    def valueByName(self, vname:str) -> ValueWithPrecision:
        return self.valuesByNameMap[vname]
    
    def statusString(self):
        modeStr = 'AUTO' if self.rangeAuto else 'MAN'
        
        retStrings = [modeStr]
        if self.highVoltage:
            retStrings.append('HighV') 
        if self.leadError:
            retStrings.append('LeadERR')
        if self.compMode:
            retStrings.append('CompMode')
        if self.recordMode:
            retStrings.append('REC')
            
        if self.hold:
            retStrings.append('HOLD')
            
        return '|'.join(retStrings)
            
        

class MeasurementNormal(Measurement):
    def __init__(self, byteslist:bytearray):
        super().__init__(byteslist)
        
        self.main = ValueWithPrecision()
        self.aux1 = ValueWithPrecision()
        self.aux2 = ValueWithPrecision()
        self.bargraph = ValueWithPrecision()
        
        curIdx = self.startIdx
        curIdx += self.extractValueWithPrecision(curIdx, 'main')
        
        if self.aux1_present:
            log.debug("HAVE AUX1")
            curIdx += self.extractValueWithPrecision(curIdx, 'aux1')
        if self.aux2_present:
            log.debug("HAVE AUX1")
            curIdx += self.extractValueWithPrecision(curIdx, 'aux2')
        if self.bargraph_present:
            log.debug("HAVE BG")
            curIdx += self.extractValueWithPrecision(curIdx, 'bargraph')
                    
    def __str__(self):
        strVals = [
            'Normal Measurement',
            self.statusString(),
            ' main: %s' % str(self.main)
            
        ]
        if self.aux1_present:
            strVals.append(' AUX1: %s' % str(self.aux1))
        if self.aux2_present:
            strVals.append(' AUX2: %s' % str(self.aux2))
        if self.bargraph_present:
            strVals.append(' BG: %s' % str(self.bargraph))
            
        return "\n".join(strVals)

class MeasurementRelative(Measurement):
    def __init__(self, byteslist:bytearray):
        super().__init__(byteslist)
        curIdx = self.startIdx
        curIdx += self.extractValueWithPrecision(curIdx, 'relative')
        curIdx += self.extractValueWithPrecision(curIdx, 'reference')
        curIdx += self.extractValueWithPrecision(curIdx, 'absolute')
        
    def __str__(self):
        strVals = [
            
            'Relative Measurement',
            self.statusString(),
            ' Rel: %s' % str(self.relative),
            ' Ref: %s' % str(self.reference),
            ' Abs: %s' % str(self.absolute),
        ]

        return "\n".join(strVals)
        
class MeasurementMinMax(Measurement):
    def __init__(self, byteslist:bytearray):
        super().__init__(byteslist)
        curIdx = self.startIdx
        curIdx += self.extractValueWithPrecision(curIdx, 'current', False)
        curIdx += self.extractValWithPrecisionAndSeconds(curIdx, 'max')
        curIdx += self.extractValWithPrecisionAndSeconds(curIdx, 'average')
        curIdx += self.extractValWithPrecisionAndSeconds(curIdx, 'min')
        unitstr = self.payloadString(curIdx, 8)
        for v in [self.current, self.max, self.average, self.min]:
            setattr(v, 'units', unitstr)
        
        
    def extractValWithPrecisionAndSeconds(self, startIdx, saveAsAttrib:str):
        curIdx = startIdx 
        curIdx += self.extractValueWithPrecision(curIdx, saveAsAttrib, False)
        vSaved = getattr(self, saveAsAttrib)
        setattr(vSaved, 'seconds', self.payloadInt(curIdx, curIdx+4))
        curIdx += 4
        return curIdx - startIdx
        
    def __str__(self):
        strVals = [
            
            'MinMax Measurement',
            self.statusString(),
            ' Cur: %s' % str(self.current),
            ' Max: %s' % str(self.max),
            ' Min: %s' % str(self.min),
            ' Avg: %s' % str(self.average),
        ]

        return "\n".join(strVals)
class MeasurementPeak(Measurement):
    def __init__(self, byteslist:bytearray):
        super().__init__(byteslist)
        curIdx = self.startIdx
        curIdx += self.extractValueWithPrecision(curIdx, 'max')
        curIdx += self.extractValueWithPrecision(curIdx, 'min')
    
    def __str__(self):
        strVals = [
            'Peak Measurement',
            self.statusString(),
            ' Max: %s' % str(self.max),
            ' Min: %s' % str(self.min)
        ]
        
        return "\n".join(strVals)

class Factory:
    
    @classmethod 
    def construct(cls, byteslist:bytearray):
        m = Measurement(byteslist)
        fmt = m.misc1.format
        formatToClassMap = {
            0: MeasurementNormal,
            1: MeasurementRelative,
            2: MeasurementMinMax,
            4: MeasurementPeak
            }
        
        if fmt in formatToClassMap:
            return formatToClassMap[fmt](byteslist)
        
        return None
