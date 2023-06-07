'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''

from enum import Enum 
from psytestbench.uthid.bitfield.bitfield import BitfieldStructure, BitfieldUnion, c_uint8


Signature = 0xcdab 
SignatureNumBytes = 2

byteorder='little'

PacketsizeNumBytes = 2
MaxPacketSize = 512


class PacketType(Enum):
    ReplyCode   = 0x01 
    Measurement = 0x02 
    Save        = 0x03 
    RecordInfo  = 0x04 
    RecordData  = 0x05
    ReplyData   = 0x72


class ReplyCode(Enum):
    OK = 0x4b4f 
    Error = 0x5245

class MiscByte1Bits(BitfieldStructure):
    _pack_ = 1
    _fields_ = [
            ("_res", c_uint8, 1),
            ("aux1", c_uint8, 1),
            ("aux2", c_uint8, 1),
            ("bargraph", c_uint8, 1),
            ("format", c_uint8, 3),
            ("hold", c_uint8, 1)
    ]
            

class MiscByte1(BitfieldUnion):
    _fields_ = [(BitfieldUnion.bitsName, MiscByte1Bits),
                (BitfieldUnion.bytesName, c_uint8)]
    

class MiscByte2Bits(BitfieldStructure):
    _pack_ = 1
    _fields_ = [
            ("autoRange", c_uint8, 1),
            ("highVoltage", c_uint8, 1),
            ("_res", c_uint8, 1),
            ("leadError", c_uint8, 1),
            ("compMode", c_uint8, 1),
            ("recordMode", c_uint8, 1)
    ]
    
class MiscByte2(BitfieldUnion):
    _fields_ = [(BitfieldUnion.bitsName, MiscByte2Bits),
                (BitfieldUnion.bytesName, c_uint8)]

class Range(Enum):
    Auto = 0x00 # Auto range |
    Min = 0x01 # 60 mV/6 V/600 uA/60 mA/600 Ohm/60 Hz/6 nF 
    Low = 0x02 # 600 mV/60 V/6000 uA/600 mA/6 KOhm/600 Hz/60 nF
    Med = 0x03 # 600V/60 KOhm/6 KHz/600 nF
    High = 0x04 # 1000 V/600 KOhm/60 KHz/6 uF
    MegA = 0x05 # 6 MOhm/600 KHz/60 uF 
    MegB = 0x06 # 60 MOhm/6 MHz/600 uF 
    MegC = 0x07 # 60 MHz/6 mF 
    MilliFarad = 0x08 # 60 mF
    


class PrecisionBits(BitfieldStructure):
    _pack_ = 1
    _fields_ = [
            ("overloadPositive", c_uint8, 1),
            ("overloadNegative", c_uint8, 1),
            ("_res", c_uint8, 2),
            ("digits", c_uint8, 4)
    ]
    
class Precision(BitfieldUnion):
    _fields_ = [(BitfieldUnion.bitsName, PrecisionBits),
                (BitfieldUnion.bytesName, c_uint8)]



class Command(Enum):
    SetMode = 0x01
    SetRange = 0x02
    SetReference = 0x03
    MinMaxControl = 0x04
    Monitor = 0x05 
    SaveMeasurement = 0x06 
    GetSaved = 0x07
    GetSaveCount = 0x08 
    DeleteSaved = 0x09
    RecordBegin = 0x0A
    RecordEnd = 0x0B 
    RecordInfo = 0x0C
    RecordGetSample = 0x0D
    RecordCount = 0x0E
    ToggleHold = 0x5A12

