'''
Created on Jun 7, 2023

@author: Pat Deegan
@copyright: Copyright (C) 2023 Pat Deegan, https://psychogenic.com
'''

import datetime 
import time
import psytestbench.examples.mylab
from psytestbench.uthid.logger.logger import Logger
from psytestbench.uthid.logger.measurement.csv import CSV as CSVLogger
from psytestbench.uthid.logger.measurement.stdout import StdOut as StdOutLogger


import logging 
log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

SampleMinIntervalMs = 250
CSVFileDefault = '/tmp/dmm.csv'


def getLogger(csvFile:str=None) -> Logger:
    minInterval = datetime.timedelta(milliseconds=SampleMinIntervalMs)
    if csvFile:
        return CSVLogger(csvFile, minInterval)
    print("No --csv specified, logging to stdout")
    return StdOutLogger(minInterval, asCSV=True)



def main(csvFile:str=None):

    lab = psytestbench.examples.mylab.Lab
    
    dmm = lab.dmm
    
    myLogger = getLogger(csvFile)
    myLogger.begin()
    
    dmm.listenerAdd(myLogger) 
    
    dmm.startAsyncMonitoring()
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    
    dmm.stopAsyncMonitoring()
    dmm.disconnect()


main(CSVFileDefault)