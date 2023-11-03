#coding=gbk
import os
import sys
import inspect
from PresetTemplate import *
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-6]))
sys.path.append(ZKM_RootDirectory+'\\Maya\\MayaBS')
from BsAddIntermediateFramesAccordingSpecifications import *

BaseModel = cmds.textFieldButtonGrp('LoadName', q=1,text=1)
BS = cmds.textFieldButtonGrp('LoadBS', q=1,text=1)
bs = BS.split(',')
bs = bs[0].split('.')
Standard = cmds.textFieldGrp('BsIntermediateFrameIntervalSymbol',q=1,text=1)
Standard = Standard[4:-3]
ZKM_BsIntermediateFrame().ZKM_AsSpecificationsAddBSIntermediateFrame(bs[0], BaseModel, Standard)
