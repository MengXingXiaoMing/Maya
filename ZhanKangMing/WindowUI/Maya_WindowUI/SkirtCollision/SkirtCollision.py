#coding=gbk
import os
import sys
import inspect

#根目录
#sys.dont_write_bytecode = True
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))

sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *

class ZKM_SkirtCollisionWindowClass:
    def __init__(self):
        pass
    def ZKM_Window(self):
        if pm.window('WindowSkirtCollision', ex=1):
            pm.deleteUI('WindowSkirtCollision')
        pm.window('WindowSkirtCollision', s=1, t="裙子碰撞")
        pm.rowColumnLayout(nc=2)
        pm.rowColumnLayout(nc=1, adj=1)
        pm.textFieldButtonGrp('WindowSkirtCollision_SoureDrver', bl="加载", text="Hip_R,Hip_L", cw3=(50, 150, 65), l=("影响骨骼"),bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'WindowSkirtCollision_SoureDrver\')')
        pm.textFieldButtonGrp('WindowSkirtCollision_DrverTarget', bl="加载", text="", cw3=(50, 150, 65), l=("跟随样条"),bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'WindowSkirtCollision_DrverTarget\')')
        pm.textFieldButtonGrp('WindowSkirtCollision_Axial', bl="加载", text="-y", cw3=(50, 150, 65), l=("轴向"),bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'WindowSkirtCollision_Axial\')')
        pm.button(c='ZKM_SkirtCollisionWindowClass().ZKM_Create()', l="生成")
        pm.showWindow()
    def ZKM_Create(self):
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'WindowSkirtCollision_SoureDrver')
        HipJoint = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'WindowSkirtCollision_DrverTarget')
        Curve = pm.ls(sl=1)
        axial = ''
        DirectionNum = 1
        Axial = pm.textFieldButtonGrp('WindowSkirtCollision_Axial', q=1,text=1)
        Direction = [1,-1,1,-1,1,-1]
        AxialList = [u'x',u'-x',u'y',u'-y',u'z',u'-z']
        for i in range(0,len(AxialList)):
            if Axial == AxialList[i]:
                axial = 'Y'
                DirectionNum = Direction[i]

        for Hip in HipJoint:
            for Cur in Curve:
                if not pm.objExists((Cur + '_SikrtCollision_Grp')):
                    pm.select(Cur)
                    pm.pickWalk(d='up')
                    pm.mel.doGroup(0, 1, 1)
                    pm.mel.rename(Cur + '_SikrtCollision_Grp')
                else:
                    pm.select((Cur + '_SikrtCollision_Grp'))
                SikrtCollisionGrp = pm.ls(sl=1)
                if not pm.objExists((SikrtCollisionGrp[0] + '.remapValue')):
                    pm.addAttr(SikrtCollisionGrp[0], ln='remapValue', dv=0, at='double')
                    pm.setAttr((SikrtCollisionGrp[0] + '.remapValue'), e=1, keyable=True)
                pm.spaceLocator(p=(0, 0, 0), n=(Cur + '_' + Hip + 'FollowHipLoc'))
                pm.setAttr((Cur + '_' + Hip + 'FollowHipLoc.visibility'), 0)
                pm.delete(pm.parentConstraint(Cur, (Cur + '_' + Hip + 'FollowHipLoc'), weight=1))
                pm.parent((Cur + '_' + Hip + 'FollowHipLoc'), Cur)
                pm.spaceLocator(p=(0, 0, 0), n=(Cur + '_' + Hip + 'FollowSkirtLoc'))
                pm.setAttr((Cur + '_' + Hip + 'FollowSkirtLoc.visibility'), 0)
                pm.delete(pm.parentConstraint(pm.listRelatives(HipJoint, c=1), (Cur + '_' + Hip + 'FollowSkirtLoc'),
                                              weight=1))
                pm.parent((Cur + '_' + Hip + 'FollowSkirtLoc'), Hip)

                distanceBetween = pm.shadingNode('distanceBetween', asUtility=1)
                pm.connectAttr((Cur + '_' + Hip + 'FollowHipLoc.worldPosition[0]'), (distanceBetween + '.point1'), f=1)
                pm.connectAttr((Cur + '_' + Hip + 'FollowSkirtLoc.worldPosition[0]'), (distanceBetween + '.point2'),
                               f=1)

                multiplyDivide_1 = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.setAttr((multiplyDivide_1 + '.operation'), 2)
                pm.setAttr((multiplyDivide_1 + '.input1X'), 1)
                pm.connectAttr((distanceBetween + '.distance'), (multiplyDivide_1 + '.input2X'), f=1)

                multiplyDivide_2 = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.setAttr((multiplyDivide_2 + '.operation'), 2)
                pm.connectAttr((multiplyDivide_1 + '.outputX'), (multiplyDivide_2 + '.input1X'), f=1)
                pm.setAttr((multiplyDivide_2 + '.input2X'), pm.getAttr((multiplyDivide_2 + '.input1X')))

                remapValue = pm.shadingNode('remapValue', asUtility=1)
                pm.connectAttr((multiplyDivide_2 + '.outputX'), (remapValue + '.inputValue'), f=1)
                pm.addAttr(remapValue, ln='remapValue', dv=0, at='double')
                pm.setAttr((remapValue + '.remapValue'), e=1, keyable=True)
                pm.connectAttr((SikrtCollisionGrp[0] + '.remapValue'), (remapValue + '.remapValue'), f=1)

                ##################

                pm.addAttr(Cur, ln=(Hip + 'InputMin'), dv=1.1, at='double')
                pm.setAttr((Cur + '.' + Hip + 'InputMin'), e=1, keyable=True)
                pm.connectAttr((Cur + '.' + Hip + 'InputMin'), (remapValue + '.inputMin'), f=1)
                pm.addAttr(Cur, ln=Hip + 'InputMax', dv=2, at='double')
                pm.setAttr((Cur + '.' + Hip + 'InputMax'), e=1, keyable=True)
                pm.connectAttr((Cur + '.' + Hip + 'InputMax'), (remapValue + '.inputMax'), f=1)

                pm.addAttr(Cur, ln=Hip + 'OutputMin', dv=0, at='double')
                pm.setAttr((Cur + '.' + Hip + 'OutputMin'), e=1, keyable=True)
                pm.connectAttr((Cur + '.' + Hip + 'OutputMin'), (remapValue + '.outputMin'), f=1)
                pm.addAttr(Cur, ln=Hip + 'OutputMax', dv=1, at='double')
                pm.setAttr((Cur + '.' + Hip + 'OutputMax'), e=1, keyable=True)
                pm.connectAttr((Cur + '.' + Hip + 'OutputMax'), (remapValue + '.outputMax'), f=1)
        for Cur in Curve:
            AllRemapValue = pm.listConnections((Cur + '_SikrtCollision_Grp'), s=1, d=1, scn=1)
            print AllRemapValue
            LinkCondition = []
            for i in range(1, len(AllRemapValue)):
                print i
                condition = pm.shadingNode('condition', asUtility=1)
                pm.select(AllRemapValue[i - 1])
                type = pm.ls(sl=1, type='condition')
                if type:
                    pm.connectAttr((AllRemapValue[i - 1] + '.outColorR'), (condition + '.firstTerm'), f=1)
                    pm.connectAttr((AllRemapValue[i - 1] + '.outColorR'), (condition + '.colorIfTrueR'), f=1)
                else:
                    pm.connectAttr((AllRemapValue[i - 1] + '.outValue'), (condition + '.firstTerm'), f=1)
                    pm.connectAttr((AllRemapValue[i - 1] + '.outValue'), (condition + '.colorIfTrueR'), f=1)
                pm.connectAttr((AllRemapValue[i] + '.outValue'), (condition + '.secondTerm'), f=1)
                pm.setAttr((condition + '.operation'), 2)
                pm.connectAttr((AllRemapValue[i] + '.outValue'), (condition + '.colorIfFalseR'), f=1)
                AllRemapValue[i] = condition
                LinkCondition = condition
            multiplyDivide_3 = pm.shadingNode('multiplyDivide', asUtility=1)

            pm.addAttr(Cur, ln='Magnification', dv=DirectionNum*50, at='double')
            pm.setAttr((Cur + '.' + 'Magnification'), e=1, keyable=True)
            if LinkCondition:
                pm.connectAttr((LinkCondition + '.outColorR'), (multiplyDivide_3 + '.input1X'), f=1)
            else:
                pm.connectAttr((AllRemapValue[0] + '.outValue'), (multiplyDivide_3 + '.input1X'), f=1)
            pm.connectAttr((Cur + '.' + 'Magnification'), (multiplyDivide_3 + '.input2X'), f=1)
            pm.connectAttr((multiplyDivide_3 + '.outputX'), (Cur + '_SikrtCollision_Grp.rotate' + axial), f=1)

ShowWindow = ZKM_SkirtCollisionWindowClass()
ShowWindow.ZKM_Window()