#coding=gbk
'''import sys
import os
import inspect
cur_dir = '\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4])  # ��ȡ��ǰ����·�����ϲ�Ŀ¼ linux��Ӧ��'/'split��join
file_path = os.path.join(cur_dir)  # ��ȡ�ļ�·��
sys.path.append(file_path)'''
from Attribute import *
'''
������ԣ�
ZKM_AttributeClass().ZKM_AddAttributes(Curve,Type,AttributesName,HaveMin,min,HaveMax,max,Aefault)
Curve�ǿ��������ƣ�Type��������Ե����ͣ��˴����֧��double�����㣩��long�����Σ���AttributesName�����Ծ������ƣ�HaveMin���Ƿ������Сֵ��min��С
ֵ��ͬ���HaveMax��max��Aefault��Ĭ��ֵ��
�����ǰ�����
ZKM_AttributeClass().ZKM_AddAttributes('nurbsCircle1','long','a',1,0,1,5,1)

����Ĭ�����Է�Χ��
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange(Curve,AttributesName,HaveMin,min,HaveMax,max)
Curve�ǿ��������ƣ�AttributesName�������ƣ�ֻ����tx��ty��tz��rx��ry��rz��sx��sy��sz,HaveMin���Ƿ������Сֵ��min��Сֵ��ͬ���HaveMax��max
�����ǰ�����
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('nurbsCircle1','ry',0,0,1,3)
'''
#ZKM_AttributeClass().ZKM_AddAttributes('JawLine_Curve_M','long','test',1,-10,1,10,0)
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('JawLine_Curve_M','ty',1,0,1,1)
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('OrbicularisOculiMuscle1_Curve_L','ty',1,0,1,1)
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('OrbicularisOculiMuscle1_Curve_R','ty',1,0,1,1)
ZKM_AttributeClass().ZKM_SetDefaultAttributeRange('LaughingMuscle_Curve_L','ty',1,0,1,1)
