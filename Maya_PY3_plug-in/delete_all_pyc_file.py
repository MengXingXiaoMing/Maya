#coding=gbk
import pymel.core as pm
import maya.cmds as cmds
from os import listdir
# ��ȡ�ļ�·��
import os
import inspect
import sys
# �����ı�
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
path = ZKM_RootDirectory
for prefix, dirs, files in os.walk(path):
    for name in files:
        if name.endswith('.pyc'):
            filename = os.path.join(prefix, name)
            os.remove(filename)