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




This is a demo based on a program I have used to characterize low frequency, low pass filters.

It will sweep the signal generator through the frequencies "manually" and make measurements on
both channel 1 and 2 of the oscilloscope to produce a CSV of the resulting 
frequency, Vpp in, Vpp out.

It makes many assumptions about the devices, their capabilities and their connections--its main
purpose here is to serve as a real world example use case.


usage: filterscan.py [-h] [--list] [--device DEVICE] [--loglevel {debug,info,warn,error}]
                     [--csv CSV] [--freqmin FREQMIN] [--freqmax FREQMAX] [--step STEP]
                     [--numsamps NUMSAMPS] [--wave {sine,square,arb}]
                     [--amplitude AMPLITUDE] [--psu_program PSU_PROGRAM]
                     [--supply_voltage SUPPLY_VOLTAGE]

xfer function sweep (testbench v 1.0.0)

options:
  -h, --help            show this help message and exit
  --list                List all currently connected devices
  --device DEVICE       Address of device
  --loglevel {debug,info,warn,error}
                        Set log level (verbosity)
  --csv CSV             CSV file to output [/tmp/sweep.csv]
  --freqmin FREQMIN     start frequency 50
  --freqmax FREQMAX     start frequency 1200
  --step STEP           start frequency 10
  --numsamps NUMSAMPS   Num samples to average [2]
  --wave {sine,square,arb}
                        Select wave type [sine]
  --amplitude AMPLITUDE
                        Select wave amplitude (Volts) [0.4]
  --psu_program PSU_PROGRAM
                        PSU program to recall [1]
  --supply_voltage SUPPLY_VOLTAGE
                        PSU supply voltage (Volts) [3.3]









'''



import psytestbench.examples.mylab 
import time
import csv 
from enum import Enum

import logging
log = logging.getLogger(__name__)


class WaveType(Enum):
    sine = 'sine'
    square = 'square'
    arbitrary = 'arb'

    def __str__(self):
        return self.value
    
    

# just sanity checks
AbsMaxFreq = 1e6
AbsMaxVpp = 10
AbsMaxSiggenAmplitude = 5

# basic settings/defaults
MaxFrequencyOfGreatestInterest = 360
FreqMinDefault = 50
FreqMaxDefault = 1200
FreqStepBase = 10

# global lab object
lab = psytestbench.examples.mylab.Lab


def basicSetup(args):
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
    
    dso.run()
    
    dso.timebase.scaleToFrequency(50)
    dso.triggerForce()
    
    
    psu = lab.powerSupply
    psu.connect()
    if args.psu_program:
        psu.recall(args.psu_program)
        
    if args.supply_voltage < AbsMaxSiggenAmplitude:
        psu.channel1.voltage(args.supply_voltage)
    
    psu.channel1.on()
    
    
    siggen = lab.signalGenerator
    siggen.connect()
    if args.wave == WaveType.square:
        siggen.channel1.wave.square()
    elif args.wave == WaveType.arbitrary:
        siggen.channel1.wave.arbitrary()
    else:
        siggen.channel1.wave.sine()
    siggen.channel1.dutyCycle(50)
    siggen.channel1.frequency(200)
    amp = args.amplitude
    if amp > AbsMaxSiggenAmplitude:
        amp = AbsMaxSiggenAmplitude
    siggen.channel1.amplitude(amp)
    siggen.channel1.on()
    
    
    
    
    dso.measure.frequency(dso.channel1)
    dso.measure.vPP(dso.channel1)
    dso.measure.vPP(dso.channel2)

def collectSamples(dso, num=5, intsampdelay=0.25, freq=None):
    tfreq = 0
    tvpp = 0
    fvpp = 0
    count = 0
    for _i in range(num):
        time.sleep(intsampdelay)
        if freq is None:
            freq = dso.measurement.frequency(dso.channel1)
        vpp = dso.measurement.vPP(dso.channel1)
        postvpp = dso.measurement.vPP(dso.channel2)
        if freq < AbsMaxFreq and vpp < AbsMaxVpp and postvpp < AbsMaxVpp:
            tfreq += freq
            tvpp += vpp
            fvpp += postvpp
            count += 1
    if not count:
        log.error(f"Could not collect any valid samples!")
        return 
    valsTuple = (tfreq/count, tvpp/count, fvpp/count)
    log.debug(f"Collected sample {valsTuple}")
    return valsTuple


LastFreq = None
def sweepRange(args, start, end, step, intoSamps):
    global LastFreq

    for i in range(start, end, step):
        log.debug(f"Freq {i}")
        lab.signalGenerator.channel1.frequency(i)
        if LastFreq is None or abs(i-LastFreq) > 50:
            log.info(f"scaling timebase to freq {i}")
            lab.dso.timebase.scaleToFrequency(i)
            if LastFreq is None:
                time.sleep(0.5)
            else:
                time.sleep(0.25)
            LastFreq = i
        time.sleep(0.2)
        intoSamps.append(collectSamples(lab.dso, num=args.numsamps, freq=i))



def doSweep(args):
    allSamps = []
    f = args.freqmin
    fmax = args.freqmax 
    chunks = []
    if fmax <= MaxFrequencyOfGreatestInterest:
        chunks = [(f, fmax, args.step)]
    else:
        baseStep = args.step
        # there's a problem here if f starts > 350?
        chunks = [(f, MaxFrequencyOfGreatestInterest, baseStep)]
        curMax = MaxFrequencyOfGreatestInterest*2
        while curMax < fmax:
            baseStep *= 2
            newChunk = (chunks[-1][1], curMax, baseStep)
            chunks.append(newChunk)
            curMax += MaxFrequencyOfGreatestInterest
            
        if chunks[-1][1] < fmax:
            baseStep *= 2
            newChunk = (chunks[-1][1], curMax, baseStep)
            chunks.append(newChunk)
            
    for c in chunks:
        sweepRange(args, c[0], c[1], c[2], allSamps)
        
    outfile=args.csv
    
    with open(outfile, 'w', newline='') as csvfile:
        sampswriter = csv.writer(csvfile, delimiter=',',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
        sampswriter.writerow(['# freq', 'src vpp', 'filtered vpp'])
        for s in allSamps:
            sampswriter.writerow(s)
            print(f'{s[0]}, {s[1]}, {s[2]}')
    
def getArgs():
    parser = psytestbench.CLI.getArgsParser(applicationName='xfer function sweep')
    
    # add some args of our own
    parser.add_argument('--csv', required=False, 
                            default='/tmp/sweep.csv', 
                            type=str, 
                            help="CSV file to output [/tmp/sweep.csv]")
    
    parser.add_argument('--freqmin', required=False, 
                            default=FreqMinDefault, 
                            type=int, 
                            help=f"start frequency {FreqMinDefault}")
    parser.add_argument('--freqmax', required=False, 
                            default=FreqMaxDefault, 
                            type=int, 
                            help=f"start frequency {FreqMaxDefault}")
    parser.add_argument('--step', required=False, 
                            default=FreqStepBase, 
                            type=int, 
                            help=f"start frequency {FreqStepBase}")
    
    parser.add_argument('--numsamps', required=False, 
                            default=2, 
                            type=int, 
                            help=f"Num samples to average [2]")
    
    parser.add_argument('--wave', required=False, 
                            default=WaveType.sine, 
                            type=WaveType,
                            choices=list(WaveType),
                            help="Select wave type [sine]")
    
    
    parser.add_argument('--amplitude', required=False, 
                            default=0.4, 
                            type=float,
                            help="Select wave amplitude (Volts) [0.4]")
    
    
    parser.add_argument('--psu_program', required=False,
                        default=1,
                        type=int,
                        help='PSU program to recall [1]')
    parser.add_argument('--supply_voltage', required=False,
                        default=3.3,
                        type=float,
                        help='PSU supply voltage (Volts) [3.3]')
    
    return psytestbench.CLI.getArguments(parser)


    
def disconnect():
    lab.dso.stop()
    lab.signalGenerator.channel1.off()
    lab.powerSupply.channel1.off()
    
    lab.disconnect()

def main():
    args = getArgs()
    basicSetup(args)
    doSweep(args)
    disconnect()


if __name__ == '__main__':
    main()
