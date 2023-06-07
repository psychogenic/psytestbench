'''
Created on Apr 27, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
import csv 
import datetime

from psytestbench.uthid.frame.response.types import Measurement
from psytestbench.uthid.logger.measurement.measurement import MeasurementLogger

import logging 
log = logging.getLogger(__name__)

class CSV(MeasurementLogger):
    
    def __init__(self, csvFilePath:str, minInterval:datetime.timedelta=None,
                        delimiter=',',
                         quoting=csv.QUOTE_MINIMAL,
                        ):
        super().__init__(minInterval)
        self.csvfilepath = csvFilePath
        self.delimiter = delimiter
        self.quoting = quoting
        self._mcount = 0
        self.csvwriter = None
        
    
    def outputHeader(self):
        cHeaders = self.columnHeaders()
        if len(cHeaders):
            self.csvwriter.writerow(cHeaders)
    
    def begin(self):
        log.info("Starting CSV logging to %s" % self.csvfilepath)
        self.csvfile = open(self.csvfilepath, 'w', newline='')
        self.csvwriter = csv.writer(self.csvfile, 
                                    delimiter=self.delimiter,
                                    quoting=self.quoting)
        
        #self.csvwriter.writerow(self.columnHeaders())
        super().begin() # call after so writer is started up

        
        
    def end(self):
        if not self.started:
            return 
        self.csvfile.close()
        super().end()
    
    def measurement(self, m:Measurement):
        log.info("\n%s" % m)
        self.csvwriter.writerow(self.toColumns(m))
        self._mcount += 1
        if self._mcount > 5:
            self.csvfile.flush()
            
            
        