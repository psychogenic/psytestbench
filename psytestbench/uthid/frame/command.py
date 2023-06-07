'''
Created on Apr 26, 2022

@author: Pat Deegan
@copyright: Copyright (C) 2022 Pat Deegan, https://psychogenic.com
'''
from psytestbench.uthid.frame.frame import Frame 
from psytestbench.uthid.seldevice import constants

class Command(Frame):
    def __init__(self, cmd:constants.Command):
        super().__init__(cmd)
    def __str__(self):
        try: 
            cmd = constants.Command(self.payload[0])
        except:
            cmd = self.payload[0]
            
        v = []
        for i in self.payload[1:]:
            v.append(hex(i))
        if len(v):
            return "Command: %s\nPayload: %s" % (str(cmd), ','.join(v))
        else:
            return "Command: %s" % str(cmd)

class SetMode(Command):
    def __init__(self, mode:constants.Mode):
        super().__init__([constants.Command.SetMode, mode])

class SetRange(Command):    
    def __init__(self, rangeVal:constants.Range):
        super().__init__([constants.Command.SetRange, rangeVal])



class SetReferenceValue(Command):    
    def __init__(self, refVal:float):
        super().__init__([constants.Command.SetReference, refVal])
        

class SetMinMax(Command):
    def __init__(self, enable=True):
        super().__init__(constants.Command.MinMaxControl)
        if enable:
            self.append([1, 0, 0, 0])
        else:
            self.append([0, 0, 0, 0])
            
class Monitor(Command):
    def __init__(self, enable=True):
        setTo = 1 if enable else 0
        super().__init__([constants.Command.Monitor, setTo])
    
        
class MeasurementSave(Command):
    def __init__(self):
        super().__init__(constants.Command.SaveMeasurement) 

    
    
class CommandWithIndex(Command):
    def __init__(self, cmd:constants.Command, index:int):
        super().__init__(cmd) 
        self.append(index.to_bytes(2, constants.byteorder))

class MeasurementGet(CommandWithIndex):
    def __init__(self, index:int):
        super().__init__(constants.Command.GetSaved, index)

class MeasurementCount(Command):
    def __init__(self):
        super().__init__(constants.Command.GetSaveCount) 
        
class MeasurementDelete(CommandWithIndex):
    def __init__(self, index:int):
        super().__init__(constants.Command.DeleteSaved, index)


class RecordBegin(Command):
    def __init__(self, name:str, interval:int, duration:int):
        super().__init__(constants.Command.RecordBegin)
        if len(name) >= 10:
            name = name[:9]
        self.append(name)
        self.append(interval.to_bytes(2, constants.byteorder))
        self.append(duration.to_bytes(4, constants.byteorder))
        
class RecordStop(Command):
    def __init__(self):
        super().__init__(constants.Command.RecordEnd)
        
class RecordInfo(CommandWithIndex):
    def __init__(self, index:int):
        super().__init__(constants.Command.RecordInfo, index)
        
        
class RecordGetSample(CommandWithIndex):
    def __init__(self, index:int, sampoffset:int):
        super().__init__(constants.Command.RecordGetSample, index)
        self.append(sampoffset.to_bytes(4, constants.byteorder))
        

class RecordCount(Command):
    def __init__(self):
        super().__init__(constants.Command.RecordCount)
        
class ToggleHold(Command):
    def __init__(self):
        super().__init__(constants.Command.ToggleHold)
        
### debug/test
if __name__ == "__main__":
    from psytestbench.uthid.debug.util import DebugUtils
    
    
    DebugUtils.REPLLaunchIfEnabled(globals(), "All command classes available")
        
     
        