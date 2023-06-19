#coding=gbk
'''import sys
import os
import inspect
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
file_path = os.path.join(cur_dir)  # 获取文件路径
sys.path.append(file_path)'''
from Attribute import *
'''
链接属性：
ZKM_AttributeClass().ZKM_LinkAttributes(Soure,Target,NodeType,Multiplier,SoureMappingMin,SoureMappingMax,TargetMappingMin,TargetMappingMax)
Soure是原属性，Target是目标属性，NodeType属性有multiplyDivide和setRange，multiplyDivide是乘节点，Multiplier是乘以的数值，如果NodeType不是multiplyDivide，
则Multiplier可以随便填个数字，setRange是范围映射节点，SoureMappingMin和SoureMappingMax代表控制源的数值范围，TargetMappingMin和
TargetMappingMax代表控制目标的数值范围，如果NodeType不是setRange，则SoureMappingMin,SoureMappingMax,TargetMappingMin,TargetMappingMax
可以随便填数字。
下面是案例：
ZKM_AttributeClass().ZKM_HideUselessAttributes('nurbsCircle1.translateX','blendShape1.pSphere2','setRange',1,0,1,0,10)

隐藏并锁定无用属性：
ZKM_AttributeClass().ZKM_HideUselessAttributes(Sel)
sel是控制器名称。
下面是案例：
ZKM_AttributeClass().ZKM_HideUselessAttributes('nurbsCircle1')
'''
ZKM_AttributeClass().ZKM_LinkAttributes('JawLine_Curve_M.translateY','blendShape1.jawOpen_Mesh','setRange',0,0,1,0,1)
ZKM_AttributeClass().ZKM_HideUselessAttributes('JawLine_Curve_M')
ZKM_AttributeClass().ZKM_LinkAttributes('OrbicularisOculiMuscle1_Curve_L.translateY','blendShape1.browDownLeft_Mesh','setRange',0,0,1,0,1)
ZKM_AttributeClass().ZKM_HideUselessAttributes('OrbicularisOculiMuscle1_Curve_L')
ZKM_AttributeClass().ZKM_LinkAttributes('OrbicularisOculiMuscle1_Curve_R.translateY','blendShape1.browDownRight_Mesh','setRange',0,0,1,0,1)
ZKM_AttributeClass().ZKM_HideUselessAttributes('OrbicularisOculiMuscle1_Curve_R')
ZKM_AttributeClass().ZKM_LinkAttributes('LaughingMuscle_Curve_L.translateY','blendShape1.mouthPressLeft_Mesh','setRange',0,0,1,0,1)
ZKM_AttributeClass().ZKM_HideUselessAttributes('LaughingMuscle_Curve_L')

