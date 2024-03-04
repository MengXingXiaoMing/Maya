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
        pm.textFieldButtonGrp('WindowSkirtCollision_SoureDrver', bl="加载", text="Hip_R,Hip_L", cw3=(70, 150, 65), l=("影响骨骼"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'WindowSkirtCollision_SoureDrver\')')
        pm.textFieldButtonGrp('WindowSkirtCollision_DrverTarget', bl="加载", text="", cw3=(70, 150, 65), l=("跟随样条"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'WindowSkirtCollision_DrverTarget\')')
        pm.button(c='ZKM_SkirtCollisionWindowClass().ZKM_CreateCurve()', l="创建裙底边缘样条")
        pm.textFieldButtonGrp('WindowSkirtCollision_Skirt_Edge', bl="加载", text="", cw3=(70, 150, 65), l=("裙底边缘样条"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'WindowSkirtCollision_Skirt_Edge\')')
        pm.textFieldButtonGrp('WindowSkirtCollision_Axial', bl="加载", text="z", cw3=(70, 150, 65), l=("轴向"),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\', \'WindowSkirtCollision_Axial\')')
        pm.button(c='ZKM_SkirtCollisionWindowClass().ZKM_Create()', l="生成")
        pm.showWindow()

    def ZKM_Create(self):
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'WindowSkirtCollision_SoureDrver')
        HipJoint = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'WindowSkirtCollision_DrverTarget')
        Curve = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'WindowSkirtCollision_Skirt_Edge')
        RangeCurve = pm.ls(sl=1)
        axial = ''
        DirectionNum = 1
        Axial = pm.textFieldButtonGrp('WindowSkirtCollision_Axial', q=1, text=1)
        Direction = [-1, 1, -1, 1, -1, 1]
        AxialList = [u'x', u'-x', u'y', u'-y', u'z', u'-z']
        AxialList_2 = ['X', 'X', 'Y', 'Y', 'Z', 'Z']
        for i in range(0, len(AxialList)):
            if Axial == AxialList[i]:
                axial = AxialList_2[i]
                DirectionNum = Direction[i]
        FollowLocGrp = pm.group(em=1, n=HipJoint[0] + '_' + HipJoint[1] + '_FollowLocGrp')
        locA = pm.spaceLocator(p=(0, 0, 0), n=('FollowSkirtScaleLocA'))
        locB = pm.spaceLocator(p=(0, 0, 0), n=('FollowSkirtScaleLocB'))
        pm.setAttr(locA+'.translateX',1)
        Scale_distanceBetween = pm.shadingNode('distanceBetween', asUtility=1)

        decomposeMatrix = pm.shadingNode('decomposeMatrix', asUtility=1)
        pm.connectAttr((locA + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
        pm.connectAttr((decomposeMatrix + '.outputTranslate'), (Scale_distanceBetween + '.point1'), f=1)
        decomposeMatrix = pm.shadingNode('decomposeMatrix', asUtility=1)
        pm.connectAttr((locB + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
        pm.connectAttr((decomposeMatrix + '.outputTranslate'), (Scale_distanceBetween + '.point2'), f=1)

        '''pm.connectAttr((locA + '.translate'), (Scale_distanceBetween + '.point1'), f=1)
        pm.connectAttr((locB + '.translate'), (Scale_distanceBetween + '.point2'), f=1)'''
        pm.parent(RangeCurve,locA,locB,FollowLocGrp)
        All_clamp = []
        clamp = []
        for Hip in HipJoint:
            pm.spaceLocator(p=(0, 0, 0), n=(Hip + '_FollowSkirtLoc'))
            pm.setAttr(Hip + '_FollowSkirtLoc.inheritsTransform', 0)
            HipDecomposeMatrix = pm.shadingNode('decomposeMatrix', asUtility=1)
            pm.connectAttr((Hip + '_FollowSkirtLoc.worldMatrix[0]'), (HipDecomposeMatrix+'.inputMatrix'), force=1)

            # pm.setAttr((Cur + '_' + Hip + 'FollowSkirtLoc.visibility'), 0)
            pm.parent((Hip + '_FollowSkirtLoc'), FollowLocGrp)
            pathAnimation = pm.pathAnimation(RangeCurve[0], (Hip + '_FollowSkirtLoc'))
            pm.select(cl=1)
            SubitemJoint = pm.listRelatives(Hip, c=1)
            J_A = pm.joint(p=(0, 0, 0), n=(Hip + '_' + SubitemJoint[0] + '_JointA'))
            J_B = pm.joint(p=(0, 0, 0), n=(Hip + '_' + SubitemJoint[0] + '_JointB'))
            pm.select(J_A)
            J_C = pm.joint(p=(0, 0, 0), n=(Hip + '_' + SubitemJoint[0] + '_JointC'))
            J_D = pm.joint(p=(0, 0, 0), n=(Hip + '_' + SubitemJoint[0] + '_JointD'))
            pm.delete(pm.parentConstraint(Hip, (Hip + '_' + SubitemJoint[0] + '_JointA'), w=1))
            pm.delete(pm.parentConstraint(SubitemJoint[0], (Hip + '_' + SubitemJoint[0] + '_JointB'), w=1))
            pm.delete(pm.parentConstraint(Hip, (Hip + '_' + SubitemJoint[0] + '_JointC'), w=1))
            pm.delete(pm.parentConstraint(SubitemJoint[0], (Hip + '_' + SubitemJoint[0] + '_JointD'), w=1))
            pm.spaceLocator(p=(0, 0, 0), n=(Hip + '_FollowSkirtDirectionLoc'))
            pm.delete(pm.parentConstraint(SubitemJoint[0], (Hip + '_FollowSkirtDirectionLoc'), w=1))
            pm.parent((Hip + '_FollowSkirtDirectionLoc'),FollowLocGrp)
            pm.parent(J_A, FollowLocGrp)
            pm.pointConstraint(Hip, (Hip + '_' + SubitemJoint[0] + '_JointA'), w=1)
            pm.aimConstraint(( Hip + '_FollowSkirtLoc'), (Hip + '_' + SubitemJoint[0] + '_JointA'), weight=1,
                             upVector=(0, 0, -1), worldUpObject=(Hip + '_FollowSkirtDirectionLoc'),
                             worldUpType="object",
                             offset=(0, 0, 0), aimVector=(1, 0, 0), worldUpVector=(0, 0, -1))#objectrotation
            pm.aimConstraint(SubitemJoint, (Hip + '_' + SubitemJoint[0] + '_JointC'), weight=1,
                             upVector=(0, -1, 0), worldUpObject=(Hip + '_' + SubitemJoint[0] + '_JointA'),
                             worldUpType="object",
                             offset=(0, 0, 0), aimVector=(1, 0, 0))
            '''pm.tangentConstraint(RangeCurve, (Hip + '_FollowSkirtLoc'),worldUpType="object",
                                 aimVector=(0, 1, 0),upVector=(0, 0, 1), weight=1,worldUpObject=Hip)'''
            decomposeMatrix = pm.shadingNode('decomposeMatrix', asUtility=1)
            pm.connectAttr((SubitemJoint[0] + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
            nearestPointOnCurve = pm.shadingNode('nearestPointOnCurve', asUtility=1)
            pm.connectAttr((decomposeMatrix + '.outputTranslate'), (nearestPointOnCurve + '.inPosition'), force=1)
            CurveShape = pm.listRelatives(RangeCurve, c=1, type='nurbsCurve')
            pm.connectAttr((CurveShape[0] + '.worldSpace[0]'), (nearestPointOnCurve + '.inputCurve'), force=1)
            pm.connectAttr((nearestPointOnCurve + '.parameter'), (pathAnimation + '.uValue'), f=1)

            for Cur in Curve:
                if not pm.objExists((Cur + '_SikrtCollision_Grp')):
                    pm.select(Cur)
                    pm.pickWalk(d='up')
                    pm.mel.doGroup(0, 1, 1)
                    pm.mel.rename(Cur + '_SikrtCollision_Grp')
                else:
                    pm.select((Cur + '_SikrtCollision_Grp'))
                SikrtCollisionGrp = pm.ls(sl=1)

                pm.spaceLocator(p=(0, 0, 0), n=(Cur + '_' + Hip + '_FollowHipLoc'))
                # pm.setAttr((Cur + '_' + Hip + 'FollowHipLoc.visibility'), 0)
                pm.parent((Cur + '_' + Hip + '_FollowHipLoc'), FollowLocGrp)
                pm.delete(pm.parentConstraint(Cur, (Cur + '_' + Hip + '_FollowHipLoc'), w=1))

                distanceBetween = pm.shadingNode('distanceBetween', asUtility=1)

                #pm.connectAttr((Cur + '_' + Hip + '_FollowHipLoc.translate'), (distanceBetween + '.point1'), f=1)
                decomposeMatrix = pm.shadingNode('decomposeMatrix', asUtility=1)
                pm.connectAttr((Cur + '_' + Hip + '_FollowHipLoc.worldMatrix[0]'), (decomposeMatrix+'.inputMatrix'), force=1)
                pm.connectAttr((decomposeMatrix+'.outputTranslate'), (distanceBetween + '.point1'), f=1)
                #pm.connectAttr((Hip + '_FollowSkirtLoc.translate'), (distanceBetween + '.point2'),f=1)
                pm.connectAttr((HipDecomposeMatrix+'.outputTranslate'), (distanceBetween + '.point2'), f=1)

                multiplyDivide_1 = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.setAttr((multiplyDivide_1 + '.operation'), 2)
                pm.setAttr((multiplyDivide_1 + '.input1X'), 1)
                pm.connectAttr((Scale_distanceBetween + '.distance'), (multiplyDivide_1 + '.input1X'), f=1)
                pm.connectAttr((distanceBetween + '.distance'), (multiplyDivide_1 + '.input2X'), f=1)

                '''multiplyDivide_2 = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.setAttr((multiplyDivide_2 + '.operation'), 2)
                pm.connectAttr((multiplyDivide_1 + '.outputX'), (multiplyDivide_2 + '.input1X'), f=1)
                pm.setAttr((multiplyDivide_2 + '.input2X'), pm.getAttr((multiplyDivide_2 + '.input1X')))'''

                multiplyDivide_2 = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.setAttr((multiplyDivide_2 + '.operation'), 2)
                pm.connectAttr((multiplyDivide_1 + '.outputX'), (multiplyDivide_2 + '.input1X'), f=1)

                multiplyDivide_X = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.addAttr(Cur, ln=(Hip + 'Range'), dv=0.402, at='double')
                pm.setAttr((Cur + '.' + Hip + 'Range'), e=1, keyable=True)
                pm.connectAttr((multiplyDivide_X + '.outputX'), (multiplyDivide_2 + '.input2X'), f=1)
                #pm.connectAttr((Scale_distanceBetween + '.distance'), (multiplyDivide_X + '.input2X'), f=1)
                pm.connectAttr((Cur + '.' + Hip + 'Range'), (multiplyDivide_X + '.input1X'), f=1)
                #pm.setAttr((multiplyDivide_2 + '.input2X'), pm.getAttr((multiplyDivide_2 + '.input1X')))

                remapValue = pm.shadingNode('remapValue', asUtility=1)
                pm.connectAttr((multiplyDivide_2 + '.outputX'), (remapValue + '.inputValue'), f=1)

                multiplyDivide_3 = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.connectAttr((remapValue + '.outValue'), (multiplyDivide_3 + '.input1X'), f=1)
                #pm.connectAttr((remapValue + '.outValue'), (multiplyDivide_3 + '.input1Y'), f=1)
                #pm.connectAttr((remapValue + '.outValue'), (multiplyDivide_3 + '.input1Z'), f=1)


                '''pm.addAttr(Cur,ln=Hip+"_axial", en="X:Y:Z:", at="enum")
                pm.setAttr((Cur+'.'+Hip+'_axial'),e=1, keyable=True)
                multiplyDivide_4 = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.connectAttr((J_C + '.rotate'), (multiplyDivide_4 + '.input1'), f=1)
                choice = pm.shadingNode('choice', asUtility=1)
                pm.connectAttr((multiplyDivide_4 + '.input1X'), (choice + '.input[0]'), f=1)
                pm.connectAttr((multiplyDivide_4 + '.input1Y'), (choice + '.input[1]'), f=1)
                pm.connectAttr((multiplyDivide_4 + '.input1Z'), (choice + '.input[2]'), f=1)
                pm.connectAttr((Cur + '.'+Hip+'_axial'), (choice + '.selector'), f=1)
                pm.connectAttr((choice + '.output'), (multiplyDivide_3 + '.input2X'), f=1)'''
                pm.connectAttr((J_C + '.rotateY'), (multiplyDivide_3 + '.input2X'), f=1)

                multiplyDivide_4 = pm.shadingNode('multiplyDivide', asUtility=1)
                pm.connectAttr((multiplyDivide_3 + '.outputX'), (multiplyDivide_4 + '.input1X'), f=1)
                pm.addAttr(Cur, ln=Hip + 'Magnification', dv=DirectionNum, at='double')
                pm.setAttr((Cur + '.' + Hip + 'Magnification'), e=1, keyable=True)
                pm.connectAttr((Cur + '.' + Hip + 'Magnification'), (multiplyDivide_4 + '.input2X'), f=1)

                clamp = pm.shadingNode('clamp', asUtility=1)
                pm.setAttr((clamp + '.maxR'), 180)
                pm.connectAttr((multiplyDivide_4 + '.outputX'), (clamp + '.inputR'), f=1)

                pm.addAttr(Cur, ln=(Hip + 'InputMin'), dv=0.9, at='double')
                pm.setAttr((Cur + '.' + Hip + 'InputMin'), e=1, keyable=True)
                pm.connectAttr((Cur + '.' + Hip + 'InputMin'), (remapValue + '.inputMin'), f=1)


                #pm.connectAttr((clamp + '.outputR'), (Cur + '_SikrtCollision_Grp.rotate' + axial), f=1)
                All_clamp.append(clamp)
        for j in range(0,len(Curve)):
            for k in range(0, len(HipJoint)):
                Soure = pm.listConnections((Curve[j] + '_SikrtCollision_Grp.rotate' + axial), s=1, d=1, scn=1)
                if not Soure:
                    condition = pm.shadingNode('condition', asUtility=1)
                    pm.setAttr((condition + '.operation'), 2)
                    pm.connectAttr((All_clamp[j] + '.outputR'),(condition + '.firstTerm'))
                    pm.connectAttr((All_clamp[j] + '.outputR'), (condition + '.colorIfTrueR'))
                    pm.connectAttr((condition + '.outColorR'), (Curve[j] + '_SikrtCollision_Grp.rotate' + axial), f=1)
                    pm.setAttr((condition + '.colorIfFalseR'), 0)
                else:
                    condition = pm.shadingNode('condition', asUtility=1)
                    pm.setAttr((condition + '.operation'), 2)
                    pm.connectAttr((All_clamp[j+len(Curve)] + '.outputR'), (condition + '.firstTerm'))
                    pm.connectAttr((All_clamp[j+len(Curve)] + '.outputR'), (condition + '.colorIfTrueR'))
                    pm.connectAttr((Soure[0] + '.outColorR'), (condition + '.colorIfFalseR'), f=1)
                    pm.connectAttr((Soure[0] + '.outColorR'), (condition + '.secondTerm'), f=1)
                    pm.connectAttr((condition + '.outColorR'), (Curve[j] + '_SikrtCollision_Grp.rotate' + axial), f=1)
    def ZKM_CreateCurve(self):
        pm.circle(c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=0.3502, tol=0, nr=(1, 0, 0))
        pm.mel.objectMoveCommand()
        pm.rebuildCurve( rt=0, ch=1, end=1, d=3, kr=0, s=12, kcp=1, tol=0, kt=0, rpo=1, kep=0)
        pm.mel.DeleteHistory()
ShowWindow = ZKM_SkirtCollisionWindowClass()
ShowWindow.ZKM_Window()