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
'''
from psytestbench.psytb.property import PropertyWrapper, scpi
from psytestbench.ds1000z.channel import Channel

class Measure(PropertyWrapper):
    
    def __init__(self, rawProperty:scpi.scpi_instrument.Property):
        super().__init__(rawProperty)
        

    def clear(self, item:str):
        self.prop.clear(item)

    def clearAll(self):
        return self.clear('ALL')
    
    def clearItem(self, idx:int):
        return self.clear(f'ITEM{idx}')
            
    def off(self):
        return self.source('OFF')
    
    def displayAll(self, setToOn:bool=True):
        self.activateBoolean(self.prop.adisplay, setToOn)
        
        
    def source(self, setToSource:str=None):
        '''
        D0|D1|D2|D3|D4|D5|D6|D7|D8|
        D9|D10|D11|D12|D13|D14|D15|
        CHANnel1|CHANnel2|CH
        '''
        return self.getSetString(self.prop.source, setToSource)
    
    def sourceChannel(self, channel:Channel):
        return self.source(f'CHANNEL{channel.id}')
    
    def sourceDigital(self, idx:int):
        return self.source(f'D{idx}')
    
    
    def item(self, itmName:str, forChannel:Channel, src2Channel:Channel = None):
        '''
        These are valid.  Many implemented as utility methods, but 
        others haven't used, so left for later.
        
            {VMAX|VMIN|VPP|VTOP|VBASe|VAMP|VAVG|
        VRMS|OVERshoot|PREShoot|MARea|MPARea|
        PERiod|FREQuency|RTIMe|FTIMe|PWIDth|
        NWIDth|PDUTy|NDUTy|RDELay|FDELay|
        RPHase|FPHase|TVMAX|TVMIN|PSLEWrate|
        NSLEWrate|VUPper|VMID|VLOWer|VARIance|
        PVRMS|PPULses|NPULses|PEDGes|NEDGes}
            '''
        if src2Channel is None:
            self.prop.item(f'{itmName}, CHANNEL{forChannel.id}')
        else:
            self.prop.item(f'{itmName}, CHANNEL{forChannel.id}, CHANNEL{src2Channel.id}')
            
    
    def vMax(self, forChannel:Channel):
        self.item('VMAX', forChannel)

    def vMin(self, forChannel:Channel):
        self.item('VMIN', forChannel)
    def vPP(self, forChannel:Channel):
        self.item('VPP', forChannel)
    def vTop(self, forChannel:Channel):
        self.item('VTOP', forChannel)
    def vBase(self, forChannel:Channel):
        self.item('VBASE', forChannel)
    def vAmp(self, forChannel:Channel):
        self.item('VAMP', forChannel)
    def vAvg(self, forChannel:Channel):
        self.item('Vavg', forChannel)
    def vRMS(self, forChannel:Channel):
        self.item('VRMS', forChannel)
    def overshoot(self, forChannel:Channel):
        self.item('OVERSHOOT', forChannel)
    def period(self, forChannel:Channel):
        self.item('PER', forChannel)
    def frequency(self, forChannel:Channel):
        self.item('FREQ', forChannel)
    def dutyP(self, forChannel:Channel):
        self.item('PDuty', forChannel)
    def dutyN(self, forChannel:Channel):
        self.item('NDuty', forChannel)
        
    def vMaxTime(self, forChannel:Channel):
        self.item('TVMax', forChannel)
        
    def vMinTime(self, forChannel:Channel):
        self.item('TVMin', forChannel)
        
        
        
    def riseDelay(self, forChannel:Channel, chanB:Channel):
        self.item('RDELAY', forChannel, chanB)
    def fallDelay(self, forChannel:Channel, chanB:Channel):
        self.item('FDELAY', forChannel, chanB)
    def risePhase(self, forChannel:Channel, chanB:Channel):
        self.item('RPHASE', forChannel, chanB)
    def fallPhase(self, forChannel:Channel, chanB:Channel):
        self.item('FPHASE', forChannel, chanB)

    
    
    