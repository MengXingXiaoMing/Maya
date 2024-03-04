#coding=gbk
'''import sys
import os
import inspect
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
file_path = os.path.join(cur_dir)  # 获取文件路径
sys.path.append(file_path)'''
from Attribute import *
'''
添加属性：
ZKM_AttributeClass().ZKM_AddAttributes(Curve,Type,AttributesName,HaveMin,min,HaveMax,max,Aefault)
Curve是控制器名称，Type是添加属性的类型，此代码仅支持double（浮点）和long（整形），AttributesName是属性具体名称，HaveMin是是否具有最小值，min最小
值，同理得HaveMax和max，Aefault是默认值。
下面是案例：
ZKM_AttributeClass().ZKM_AddAttributes('nurbsCircle1','long','a',1,0,1,5,1)

设置默认属性范围：
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange(Curve,AttributesName,HaveMin,min,HaveMax,max)
Curve是控制器名称，AttributesName属性名称，只接受tx、ty、tz、rx、ry、rz、sx、sy、sz,HaveMin是是否具有最小值，min最小值，同理得HaveMax和max
下面是案例：
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('nurbsCircle1','ry',0,0,1,3)
'''
#ZKM_AttributeClass().ZKM_AddAttributes('JawLine_Curve_M','long','test',1,-10,1,10,0)
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('JawLine_Curve_M','ty',1,0,1,1)
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('OrbicularisOculiMuscle1_Curve_L','ty',1,0,1,1)
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('OrbicularisOculiMuscle1_Curve_R','ty',1,0,1,1)
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('LaughingMuscle_Curve_L','ty',1,0,1,1)
