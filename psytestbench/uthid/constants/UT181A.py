'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
from psytestbench.uthid.constants.UTHID import *

class Mode(Enum):
    NA = 0x01
    VACnormal       = 0x1111
    VACnormalRel    = 0x1112
    VACHz           = 0x1121
    VACpeak         = 0x1131
    VAClow          = 0x1141
    VAClowRel       = 0x1142
    VACdBV          = 0x1151
    VACdBVRel       = 0x1152
    VACdBm          = 0x1161
    VACdBmRel       = 0x1162
    mVACnormal      = 0x2111
    mVACnormalRel   = 0x2112
    mVACHz          = 0x2121
    mVACpeak        = 0x2131
    mVACACDC        = 0x2141
    mVACACDCRel     = 0x2142
    VDCnormal       = 0x3111
    VDCnormalRel    = 0x3112
    VDCACDC         = 0x3121
    VDCACDCRel      = 0x3122
    VDCpeak         = 0x3131
    mVDCnormal      = 0x4111
    mVDCnormalRel   = 0x4112
    mVDCpeak        = 0x4121
    TempCT1T2       = 0x4211
    TempCT1T2Rel    = 0x4212
    TempCT2T1       = 0x4221
    TempCT2T1Rel    = 0x4222
    TempCT1mT2      = 0x4231
    TempCT2mT1Rel   = 0x4241
    TempFT1T2       = 0x4311
    TempFT1T2Rel    = 0x4312
    TempFT2T1       = 0x4321
    TempFT2T1Rel    = 0x4322
    TempFT1mT2      = 0x4331
    TempFT2mT1      = 0x4341
    Resistance      = 0x5111
    ResistanceRel   = 0x5112
    BeeperShort     = 0x5211
    BeeperOpen      = 0x5212
    Admittance      = 0x5311
    AdmittanceRel   = 0x5312
    DiodeNormal     = 0x6111
    DiodeAlarm      = 0x6112
    Capacitance     = 0x6211
    CapacitanceRel  = 0x6212
    Frequency       = 0x7111
    FrequencyRel    = 0x7112
    Duty            = 0x7211
    DutyRel         = 0x7212
    PulseWidth      = 0x7311
    PulseWidthRel   = 0x7312
    uADCnormal      = 0x8111
    uADCnormalRel   = 0x8112
    uADCACDC        = 0x8121
    uADCACDCRel     = 0x8122
    uADCpeak        = 0x8131
    uAACnormal      = 0x8211
    uAACnormalRel   = 0x8212
    uAACHz          = 0x8221
    uAACpeak        = 0x8231
    mADCnormal      = 0x9111
    mADCnormalRel   = 0x9112
    mADCACDC        = 0x9121
    mADCACDCRel     = 0x9122
    mADCpeak        = 0x9131
    mAACnormal      = 0x9211
    mAACnormalRel   = 0x9212
    mAACHz          = 0x9221
    mAACpeak        = 0x9231
    ADCnormal       = 0xA111
    ADCnormalRel    = 0xA112
    ADCACDC         = 0xA121
    ADCACDCRel      = 0xA122
    ADCpeak         = 0xA131
    AACnormal       = 0xA211
    AACnormalRel    = 0xA212
    AACHz           = 0xA221
    AACpeak         = 0xA231
    
