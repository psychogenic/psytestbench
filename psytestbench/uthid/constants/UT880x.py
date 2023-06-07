'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
from psytestbench.uthid.constants.UTHID import *

class Mode(Enum):
    NA = 0x01
    VACnormal           = 0x1110
    VACHz               = 0x1120
    VACpeak             = 0x1130
    VAClow              = 0x1140
    VACdBV              = 0x1150
    VACdBm              = 0x1160
    mVACnormal          = 0x2110
    mVACHz              = 0x2120
    mVACACDC            = 0x2140
    VDCnormal           = 0x3110
    VDCpeak             = 0x3120
    VDCACDC             = 0x3130
    mVDCnormal          = 0x4110
    mVDCpeak            = 0x4120
    Resistance          = 0x5110
    BeeperShort         = 0x5210
    Admittance          = 0x5310
    DiodeNormal         = 0x6110
    Capacitance         = 0x6210
    Frequency           = 0x7110
    Duty                = 0x7210
    PulseWidth          = 0x7310
    TempCT1T2           = 0x8110
    TempCT2T1           = 0x8120
    TempFT1T2           = 0x8210
    TempFT2T1           = 0x8220
    uADCnormal          = 0x9110
    uADCpeak            = 0x9120
    uAACnormal          = 0x9210
    uAACpeak            = 0x9230
    mADCnormal          = 0xa110
    mADCpeak            = 0xa120
    mAACnormal          = 0xa210
    mAACpeak            = 0xa230
    ADCnormal           = 0xb110
    ADCpeak             = 0xb120
    ADCACDC             = 0xb130
    AACnormal           = 0xb210
    AACHz               = 0xb220
    AACpeak             = 0xb230
    
    
    

