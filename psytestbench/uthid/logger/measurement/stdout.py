'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
import datetime 

from psytestbench.uthid.frame.response.types import Measurement
from psytestbench.uthid.logger.measurement.measurement import MeasurementLogger

class StdOut(MeasurementLogger):
    
    def __init__(self, minInterval:datetime.timedelta=None, asCSV=False):
        super().__init__(minInterval)
        self.asCSV = asCSV
        
        
    
    def begin(self):
        super().begin()
        if self.asCSV:
            print(','.join(self.columnHeaders()))
        else:
            print(str(self.columnHeaders()))

    def measurement(self, m:Measurement):
        if self.asCSV:
            print(','.join(map(lambda x: str(x), self.toColumns(m))))
        else:
            print(str(m))