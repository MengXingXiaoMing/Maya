#coding=gbk
'''import sys
import os
import inspect
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
sys.path.append(file_path)'''
from Attribute import *
'''
�������ԣ�
ZKM_AttributeClass().ZKM_LinkAttributes(Soure,Target,NodeType,Multiplier,SoureMappingMin,SoureMappingMax,TargetMappingMin,TargetMappingMax)
Soure��ԭ���ԣ�Target��Ŀ�����ԣ�NodeType������multiplyDivide��setRange��multiplyDivide�ǳ˽ڵ㣬Multiplier�ǳ��Ե���ֵ�����NodeType����multiplyDivide��
��Multiplier�������������֣�setRange�Ƿ�Χӳ��ڵ㣬SoureMappingMin��SoureMappingMax�������Դ����ֵ��Χ��TargetMappingMin��
TargetMappingMax�������Ŀ�����ֵ��Χ�����NodeType����setRange����SoureMappingMin,SoureMappingMax,TargetMappingMin,TargetMappingMax
������������֡�
�����ǰ�����
ZKM_AttributeClass().ZKM_HideUselessAttributes('nurbsCircle1.translateX','blendShape1.pSphere2','setRange',1,0,1,0,10)

���ز������������ԣ�
ZKM_AttributeClass().ZKM_HideUselessAttributes(Sel)
sel�ǿ��������ơ�
�����ǰ�����
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

