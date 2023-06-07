'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

import datetime 
from psytestbench.uthid.logger.logger import Logger

from psytestbench.uthid.frame.response.types import Measurement, MeasurementNormal, \
        MeasurementRelative, MeasurementMinMax, MeasurementPeak

class MeasurementLogger(Logger):
    def __init__(self, minInterval:datetime.timedelta=None):
        super().__init__(minInterval)
        
        
    def valWithPrecToColumns(self, name, v):
        vDig = v.precision.digits
        fstr = '%%.%if' % vDig 
        val = fstr % v.value
        return [ 
                 name,
                 val,
                 v.precision.digits,
                 v.units,
                 v.seconds
        ]
        
    def columnHeaders(self):
        valWPrecCols = [
                'vname',
                'value',
                'prec',
                'units',
                'secs'
            ]
        return [
                '# date-time',
                'auto',
                'hold',
                'highV',
                'ldERR',
                'cmpMode',
                'recMode',
                'format',
                'meastype',
                'mode',
                *(valWPrecCols*4)            
            
            ]
        
    def toColumns(self, m:Measurement):
        cols = [
            self.timestamp(),
            m.rangeAuto,
            m.hold, 
            m.highVoltage,
            m.leadError,
            m.compMode,
            m.recordMode,
            m.format,
            str(type(m).__name__),
            m.mode.name,
        ]
        
        #MeasurementRelative
        if isinstance(m, MeasurementNormal):
            cols += self.valWithPrecToColumns('main', m.main)
            cols += self.valWithPrecToColumns('aux1', m.aux1)
            cols += self.valWithPrecToColumns('aux2', m.aux2)
            cols += self.valWithPrecToColumns('bg', m.bargraph)
        elif isinstance(m, MeasurementRelative):
            cols += self.valWithPrecToColumns('relative', m.relative)
            cols += self.valWithPrecToColumns('reference', m.reference)
            cols += self.valWithPrecToColumns('absolute', m.absolute)
            cols += ['']*5
        elif isinstance(m, MeasurementMinMax):
            cols += self.valWithPrecToColumns('min', m.min)
            cols += self.valWithPrecToColumns('max', m.max)
            cols += self.valWithPrecToColumns('average', m.average)
            cols += self.valWithPrecToColumns('current', m.current)
        elif isinstance(m, MeasurementPeak):
            cols += self.valWithPrecToColumns('min', m.min)
            cols += self.valWithPrecToColumns('max', m.max)

        return cols
        
