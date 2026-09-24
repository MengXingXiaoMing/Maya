# -*- coding: utf-8 -*-
import os
import inspect
import maya.cmds as cmds
import maya.mel as mel


def instal():
    # 获取文件路径
    file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
    file_path_reverse = os.path.join('/'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
    gShelfTopLevel = mel.eval('string $my_gShelfTopLevel = $gShelfTopLevel')
    current_shelf = str(cmds.tabLayout(gShelfTopLevel, query=1, selectTab=1))
    cmds.setParent(current_shelf)
    name = '体积'
    file = 'volume_window'
    cmds.shelfButton(
        sourceType='python',
        label=name,
        iol=(''),
        command=('import sys\nsys.path.append(r\"' + file_path + '\")\n'
                 'import ' + file + '\n'
                 'import importlib\n'
                 'importlib.reload(' + file + ')\n'
                 'from ' + file + ' import *\n'
                 'window.show()'),
        annotation=name)
    print(name + ' 已安装到当前工具架')


instal()
