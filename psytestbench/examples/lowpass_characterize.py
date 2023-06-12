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


This is a program which characterizes a low pass filter using 4 instruments
     * power supply
     * multimeter - measuring current
     * signal generator - manually sweeping 
     * oscilloscope - measuring Vpp in and out, and frequency

Here, all the flexibility and clutter of the command line arguments from 
the filterscan example are cleared away by hard-coding parameters, instead 
focusing on the library functionality and augmenting that example with the 
asynchronous DMM readings.

It will just step through frequencies and log samples.  It assumes:

    * siggen channel1 is connected to dso channel1 and filter input
    * dso channel2 is monitoring output
    * PSU powers the active filter
    * DMM is in loop with PSU to monitor current (uA range)

'''


import time
import csv 
import threading


import psytestbench.examples.mylab 
from psytestbench.examples.mylab import DMMListener, DMMMeasurement

import logging
logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)




# path to output CSV file -- set to None or '' to skip
OutCSVFilePath = '/tmp/lpfilt.csv'

# basic settings/defaults
FreqMin = 40
FreqMax = 1400
FreqStep = 10
InputSignalAmplitudeVolts = 0.500
AbsMaxValidValue = 2


# PSU
PowerRampStartV = 0
PowerRampEndV = 3.300
PowerRampStepV = 0.25

# number of samples of to average
NumSamplesMinDMM = 6
NumSamplesMinDSO = 4

class Sample:
    '''
        Just a container for one datapoint
    '''
    @classmethod 
    def header(cls):
        return ['# freq (set) Hz', 'freq (measured) Hz', 
                'Vpp In', 'Vpp Out', 'Current (uA)']
    
    def __init__(self, setFrequency:int, measuredFrequency:float, 
                 vppIn:float,
                 vppOut:float,
                 current:float):
        self.frequency = setFrequency 
        self.frequency_measured = measuredFrequency
        self.vppIn = vppIn 
        self.vppOut = vppOut 
        self.current = current
        
    def toList(self):
        return [
            
            str(self.frequency), 
            str(self.frequency_measured),
            str(self.vppIn),
            str(self.vppOut),
            str(self.current)
            ]
        
    def __str__(self):
        return ','.join(self.toList())
    


class CollectAndAverage:
    '''
        Just a thread safe way of collecting 
        numerical values and getting average back.
    '''
    
    def __init__(self, precision:int=2, maxValidValue:float=None):
        self.values = []
        self.lock = threading.Lock()
        self.precision = precision
        self.maxValid = maxValidValue
    
    
    def append(self, value:float):
        if self.maxValid is not None:
            if abs(value) > self.maxValid:
                return 
            
        with self.lock:
            self.values.append(value)
    
    def __len__(self):
        with self.lock:
            num = len(self.values)
            
        return num

    @property 
    def mean(self):
        if not len(self.values):
            return 0 
        with self.lock:
            avg = sum(self.values) / len(self.values)
        
        return avg 
    
        
    @property 
    def mean_string(self):
        avg = self.mean 
        if self.precision:
            formatted = f'{{:.{self.precision}f}}'
            
            return formatted.format(avg)
        
        return str(avg)
    
        
    def reset(self):
        with self.lock:
            self.values = []
            
class DSOMeasurements:
    '''
        A place to centralize DSO measurement collection and averaging
    '''
    
    def __init__(self):
        self.freq = CollectAndAverage(1)
        self.vpp_in = CollectAndAverage(4, AbsMaxValidValue)
        self.vpp_out = CollectAndAverage(4, AbsMaxValidValue)
        
        self.all = [self.freq, self.vpp_in, self.vpp_out]
        
    def __len__(self):
        return len(self.vpp_out)
    
    def reset(self):
        for a in self.all:
            a.reset()
    
    

class DMMMeasurementListener(DMMListener):
    '''
        This listener will receive notifications on every measurement
        and add the main reading value to a growing list.
        
        
    
    '''
    def __init__(self, lid:int=None):
        super().__init__(lid)
        self.averager = CollectAndAverage(3)
        self.units = ''
        
    def __len__(self):
        return len(self.averager)
    
    @property 
    def mean(self):
        return self.averager.mean
    
        
    @property 
    def mean_string(self):
        return self.averager.mean_string
    
        
    def reset(self):
        self.averager.reset()
        
    def measurement(self, m:DMMMeasurement):
        measVal = m.main # only care about main reading here
        self.units = measVal.units 
        self.averager.precision = measVal.precision.digits
        self.averager.append(measVal.value)






#### GLOBALS


# global lab object
lab = psytestbench.examples.mylab.Lab
CurrentAverager = DMMMeasurementListener()
DSOAverages = DSOMeasurements()


def basicSetup():
    '''
        Connect to and configure 4 instruments, and power up
    
    '''
    
    ### multi-meter
    dmm = lab.dmm 
    dmm.connect()
    dmm.listenerAdd(CurrentAverager)
    dmm.startAsyncMonitoring() # enables monitoring automatically
    
    
    ### oscilloscope
    dso = lab.dso
    dso.connect()
    
    dso.channel1.bandwidthLimit20MHz()
    dso.channel1.couplingDC()
    dso.channel1.on()
    
    dso.channel2.bandwidthLimit20MHz()
    dso.channel2.couplingAC()
    dso.channel2.on()
    
    
    dso.trigger.modeEdge()
    dso.trigger.edge.source(dso.channel1)
    dso.trigger.couplingLowpass()
    dso.trigger.normal()
    
    # reduce noise a whole lot by setting to average traces
    dso.acquire.averageNum(3)
    dso.acquire.average()
    
    dso.timebase.scaleToFrequency(50)
    dso.run()
    
    
    ### DSO measurements
    dso.measure.frequency(dso.channel1)
    dso.measure.vPP(dso.channel1)
    dso.measure.vPP(dso.channel2)
    
    
    ### Power supply
    
    psu = lab.powerSupply
    psu.connect()
    psu.channel1.voltage(PowerRampStartV)
    psu.channel1.on()
    psu.channel1.ramp(PowerRampStartV, PowerRampEndV, PowerRampStepV, stepDelaySecs=0.2)
    
    
    ### signal generator
    
    siggen = lab.signalGenerator
    siggen.connect()
    siggen.channel1.wave.sine()
    siggen.channel1.dutyCycle(50)
    siggen.channel1.frequency(10)
    siggen.channel1.amplitude(InputSignalAmplitudeVolts)
    siggen.channel1.on()
    
    
    
    

def collectSample(addTo:list, setFreq:int, intersampledelay=0.15):
    
    # the frequency has changed, reset our stats
    DSOAverages.reset()
    CurrentAverager.reset()
    
    # less typing
    dso = lab.dso
    
    while (len(DSOAverages) < NumSamplesMinDSO) or (len(CurrentAverager) < NumSamplesMinDMM):
        
        # wait a bit
        time.sleep(intersampledelay)
        
        # append current values to DSO averages
        DSOAverages.freq.append(dso.measurement.frequency(dso.channel1))
        DSOAverages.vpp_in.append(dso.measurement.vPP(dso.channel1))
        DSOAverages.vpp_out.append(dso.measurement.vPP(dso.channel2))
        
        # The DMM will handle itself, async
        
        log.debug(f'Have {len(DSOAverages)} DSO samples, {len(CurrentAverager)} DMM samples')
                
    
    
    log.debug(f'Done collection: {len(DSOAverages)} DSO samples, {len(CurrentAverager)} DMM samples')
    # once we have enough of both sample sources, add a datapoint to the list
    # collecting averages as formatted strings
    samp = Sample(setFreq, 
                            DSOAverages.freq.mean_string, 
                            DSOAverages.vpp_in.mean_string,
                            DSOAverages.vpp_out.mean_string,
                            CurrentAverager.mean_string)
    log.info(str(samp))
    addTo.append(samp)
    
        




LastFreq = None
def sweepRange(start:int, end:int, step:int, outCSVFilename:str=''):
    global LastFreq, DSOAverages, CurrentAverager

    allSamples = []
    
    for inFreq in range(start, end, step):
        log.debug(f"Freq {inFreq}")
        lab.signalGenerator.channel1.frequency(inFreq)
        
        # reset timebase once in a while
        if LastFreq is None or abs(inFreq-LastFreq) > 50:
            log.info(f"scaling timebase to freq {inFreq}")
            lab.dso.timebase.scaleToFrequency(inFreq)
            # give it time to adjust
            if LastFreq is None:
                time.sleep(0.5)
            else:
                time.sleep(0.33)
            LastFreq = inFreq
        time.sleep(0.5) # we've changed freq, let things settle
        
        collectSample(allSamples, inFreq)



    if outCSVFilename:
        with open(outCSVFilename, 'w', newline='') as csvfile:
            sampswriter = csv.writer(csvfile, delimiter=',',
                                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            sampswriter.writerow(Sample.header())
            for aSamp in allSamples:
                sampswriter.writerow(aSamp.toList())


def disconnect():
    lab.dso.stop()
    lab.signalGenerator.channel1.off()
    lab.powerSupply.channel1.off()
    lab.dmm.stopAsyncMonitoring()
    lab.disconnect()

def main():
    try:
        basicSetup()
        sweepRange(FreqMin, FreqMax, FreqStep, OutCSVFilePath)
        print('Done!')
        if OutCSVFilePath:
            print(f"Output collected in: {OutCSVFilePath}")
    except KeyboardInterrupt:
        pass 
    disconnect()


if __name__ == '__main__':
    main()
