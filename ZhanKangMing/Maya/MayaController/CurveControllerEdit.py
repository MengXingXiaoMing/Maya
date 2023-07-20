# coding=gbk
import maya.cmds as cmds
import random
import pymel.core as pm
import os
import sys
import inspect
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
File_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-2]))
sys.path.append(File_RootDirectory + '\\MayaCurve')
# 加载曲线编辑
from CreateAndEditCurve import *
# 加载文本
class ZKM_CurveControllerEditClass:
    # ADV改控制器（为了兼容ADV我稍微改下就直接用了）
    # ZKM_CurveControllerEditClass().ZKM_asSwapCurve('T',[1,0,0])
    def ZKM_asSwapCurve(self,Name,Color):
        Select = pm.ls(sl=1)
        AllSet = []
        if pm.objExists('AllSet'):
            pm.select('AllSet')
            pm.mel.SelectHierarchy()
            AllSet = pm.ls(sl=1)
        ZKM_CreateAndEditCurveClass().ZKM_CreateCurve((File_RootDirectory + '\MayaCommon\CurveShapeWithPicture'),Name)
        self.ZKM_ModifyControllerShapeTRS('SoftSelectionSize', 0, 0, 0)
        EndSelect = pm.ls(sl=1)
        pm.select(Select, r=1)
        pm.select(EndSelect, add=1)
        side = ""
        oppositeSide = ""
        allSet = ""
        tempString = []
        tempString2 = []
        tempString3 = []
        sel = pm.ls(sl=1)
        last = len(sel) - 1
        selShapes = []
        if len(sel) < 2:
            pm.pm.mel.error("Selected both controls to replace, and the new curve to use")

        for i in range(0, len(sel)):
            tempString = pm.listRelatives(sel[i], s=1)
            selShapes.append(tempString[0])
            if pm.mel.gmatch(sel[i], "*Extra*"):
                continue

            if not pm.objExists(selShapes[i]):
                pm.pm.mel.error("selected object:\"" + sel[i] + "\" is not a nurbsCurve")

            tempString = pm.listRelatives(sel[i], s=1)
            if pm.objectType(selShapes[i]) != "nurbsCurve" and pm.objectType(selShapes[i]) != "nurbsSurface":
                pm.pm.mel.error("selected object:\"" + sel[i] + "\" is not a nurbsCurve")

        pm.select(sel[last])
        pm.mel.DeleteHistory()
        for i in range(0, len(sel) - 1):
            tempString = pm.listRelatives(sel[i], s=1)
            tempString3 = []
            if len(tempString):
                tempString3 = pm.listConnections((tempString[0] + ".v"),
                                                 p=1, s=1, d=0)
                pm.delete(tempString)

            pm.duplicate(sel[last], n='tempXform')
            tempString = pm.listRelatives('tempXform', s=1, f=1)
            for y in range(0, len(tempString)):
                pm.rename(tempString[y],
                          (sel[i] + "Shape"))

            allSet = "AllSet"
            if pm.objExists('FaceAllSet'):
                if pm.mel.eval('sets -im FaceAllSet ' + sel[i] + ';'):
                    allSet = "FaceAllSet"

            tempString = pm.listRelatives('tempXform', s=1)
            for y in range(0, len(tempString)):
                tempString2 = pm.parent(tempString[y], sel[i], add=1, s=1)
                tempString[y] = tempString2[0]
                rot = pm.xform(sel[i], q=1, ro=1, ws=1)
                #		if(!(`gmatch $sel[0] "IK*"` || `gmatch $sel[0] "Pole*"` || `gmatch $sel[0] "RootX*"`))
                if not (rot[0] == 0 and rot[1] == 0 and rot[2] == 0):
                    pm.rotate(-90, -90, 0,(tempString[y] + ".cv[0:9999]"),r=1, os=1)#####
                if sel[i] in AllSet:
                    if pm.objExists('AllSet') :
                        pm.mel.eval('sets -add ' + allSet + ' ' + tempString[y] + ';')
                    # cmds.sets(tempString[y], add=allSet)

                if tempString3:
                    pm.catch(pm.mel.eval("connectAttr " + tempString3[0] + " " + tempString[y] + ".v"))

            pm.delete('tempXform')
        pm.dgdirty(a=1)
        pm.delete(EndSelect)
        pm.select(Select)
        ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor(Select,Color)

    # 旋转控制器
    # ZKM_CurveControllerEditClass().ZKM_RotationController('X')
    def ZKM_RotationController(self,Rotate):
        pm.mel.reflectionSetMode('none')
        X = 0.0
        Y = 0.0
        Z = 0.0
        if Rotate == "X":
            X = float(90)
            Y = float(0)
            Z = float(0)
        if Rotate == "Y":
            X = float(0)
            Y = float(90)
            Z = float(0)
        if Rotate == "Z":
            X = float(0)
            Y = float(0)
            Z = float(90)
        self.ZKM_ModifyControllerShapeTRS("rotate", X, Y, Z)

    # 修改控制器大小
    # ZKM_CurveControllerEditClass().ZKM_ModifyControllerShapeTRS('SoftSelectionSize', 0, 0, 0)
    def ZKM_ModifyControllerShapeTRS(self,Type, X, Y, Z):
        Curve = pm.ls(sl=1)
        for i in range(0, len(Curve)):
            Shape = pm.listRelatives(Curve[i], s=1)
            pm.select(cl=1)
            pm.select((Shape[0] + ".cv[0:]"))
            if Type == "translate":
                pm.move((X), (Y), (Z), localSpace=1)
            if Type == "rotate":
                pm.rotate((X), (Y), (Z), r=1)
            if Type == "scale":
                pm.scale((X), (Y), (Z), r=1)
            if Type == "SoftSelectionSize":
                size = pm.softSelect(q=1, ssd=1)
                shape = pm.listRelatives(Curve[i],c=1,type='nurbsCurve')
                AllNum = pm.getAttr(shape[0] + '.boundingBox.boundingBoxSize')
                num = max(AllNum)
                Scale = size / num * 2.14
                pm.scale((Scale), (Scale), (Scale), r=1)
            pm.select(cl=1)
        pm.select(Curve)

    # 旧版生成控制器
    def ZKM_OldChuangJianFK(self,Name,C_GrpNum,Suffix,RemoveJoint,Colour):
        pm.mel.SelectHierarchy()
        joint = pm.ls(typ='joint', sl=1)
        ALL = pm.ls(sl=1)
        if RemoveJoint == True:
            for j in joint:
                q = pm.listRelatives(j, c=1)
                if len(q) == 0:
                    joint.remove(j)
        # 建立控制器
        TopGrp = []
        nurbs = []
        for i in range(0, len(joint)):
            pm.rename(ZKM_CreateAndEditCurveClass().ZKM_CreateCurve((File_RootDirectory + '\MayaCommon\CurveShapeWithPicture'),Name), joint[i] + "_C" + Suffix)
            nurbs.append(joint[i] + "_C" + Suffix)
            ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor(nurbs, Colour)
            self.ZKM_ModifyControllerShapeTRS('SoftSelectionSize', 0, 0, 0)
            for j in range(0, C_GrpNum):
                pm.mel.doGroup(0, 1, 1)
                # 建立样条组
                pm.mel.rename(joint[i] + "_G" + str((C_GrpNum - j)) + Suffix)
            TopGrp.append(joint[i] + "_G1" + Suffix)
            pm.delete(pm.pointConstraint(joint[i], (joint[i] + "_G1" + Suffix)))
            pm.delete(pm.orientConstraint(joint[i], (joint[i] + "_G1" + Suffix)))
        # 进行父化
        for i in range(1, len(joint)):
            Parent = pm.listRelatives(joint[i], p=1)
            pm.select(Parent)
            jointLX = pm.ls(typ='joint', sl=1)
            if not jointLX:
                for k in range(0, len(ALL)):
                    Parent = pm.listRelatives(p=1)
                    pm.select(Parent, r=1)
                    jointLX = pm.ls(typ='joint', sl=1)
                    if jointLX:
                        break
            Parent = pm.ls(sl=1)
            for j in range(0, len(joint)):
                if joint[j] == Parent[0]:
                    pm.parent(TopGrp[i], nurbs[j])
                    break
        # 是否提取约束
        ExtractConstraints = pm.checkBox('WindowControllerProcessingExtractConstraints', q=1, value=1)
        # 进行约束
        if ExtractConstraints == 1:
            pm.select(cl=1)
            if not pm.objExists("ZiJianKZQyveshu"):
                pm.rename(pm.mel.doGroup(0, 1, 1), "ZiJianKZQyveshu")
        for i in range(0, len(joint)):
            pm.parentConstraint((joint[i] + "_C" + Suffix), joint[i])
            pm.scaleConstraint((joint[i] + "_C" + Suffix), joint[i])
            if ExtractConstraints == 1:
                pm.parent((joint[i] + "_scaleConstraint1"), (joint[i] + "_parentConstraint1"), "ZiJianKZQyveshu")

    # 创建生成FK控制器前置
    def ZKM_ChuangJianFKPreconditions(self):
        if pm.objExists('ZKM_FK_Root') or pm.objExists('ZKM_FK_Root_Grp') or pm.objExists('ZKM_AllFK_TopGrp'):
            pm.error('已经有 ZKM_FK_Root 、 ZKM_FK_Root_Grp 、 ZKM_AllFK_TopGrp 其中至少一个，请勿重名')
        else:
            pm.select(cl=1)
            pm.joint(p=(0, 0, 0), n='ZKM_FK_Root')
            pm.group(n='ZKM_FK_Root_Grp')
            pm.group(n='ZKM_AllFK_TopGrp')
            pm.setAttr("ZKM_FK_Root_Grp.inheritsTransform", 0)

    # 添加选定位数到Notes
    def ZKM_SetNumToNotes(self, sel, factorial):
        notes = ''
        if not sel.hasAttr('notes'):
            for i in range(0, factorial):
                j = str(random.randrange(0, 10, 1))
                notes = notes + j
            sel.addAttr('notes', type='string')
            sel.attr('notes').set(notes)
            note = []
            note.append(notes)
            return note
        else:
            notes = pm.getAttr(sel + '.notes')
            return notes
        # print (pm.getAttr(pm.ls(sl=1)[0] + '.notes'))

    # 选择特定字典的物体名称
    def ZKM_ReturnNotesToModel(self, range, Dictionary ,DictionaryProperties,list):
        DictionaryNotes = Dictionary[DictionaryProperties][list]
        Have = 0
        for r in range:
            if pm.objExists(r):
                if r.hasAttr('notes'):
                    SelNotes = ''
                    SelNotes = SelNotes + (pm.getAttr(r+'.notes'))
                    SelNotes = SelNotes.encode('utf-8')  # 字符通用码转为字符串
                    if SelNotes == DictionaryNotes:
                        pm.select(r)
                        Have = 1
                        break
        if Have == 0:
            pm.select(cl=1)

    # 控制器归零
    def ZKM_ControllerHoming(self):
        pm.select('ZKM_FK_AllController')
        pm.mel.SelectHierarchy()
        CurveShape = pm.ls(sl=1,type='nurbsCurve')
        for Shape in CurveShape:
            parent = pm.listRelatives(Shape, p=1)
            pm.setAttr(parent[0] + ".translateX", 0)
            pm.setAttr(parent[0] + ".translateY", 0)
            pm.setAttr(parent[0] + ".translateZ", 0)
            pm.setAttr(parent[0] + ".rotateX", 0)
            pm.setAttr(parent[0] + ".rotateY", 0)
            pm.setAttr(parent[0] + ".rotateZ", 0)
            pm.setAttr(parent[0] + ".scaleZ", 1)
            pm.setAttr(parent[0] + ".scaleX", 1)
            pm.setAttr(parent[0] + ".scaleY", 1)
            pm.setAttr(parent[0] + ".visibility", 1)
        pm.select(cl=1)

    # 切换控制器
    def ZKM_ChuangJianFKSwitch(self,ExtractConstraints):
        self.ZKM_ControllerHoming()
        Now = pm.parentConstraint('ZKM_FK_Root', q=1, tl=1)
        pm.select('ZKM_FK_Root')
        pm.mel.SelectHierarchy()
        if Now:
            pm.setAttr("ZKM_FK_AllController.visibility", 0)
            pm.mel.DeleteConstraints()
        else:
            pm.setAttr("ZKM_FK_AllController.visibility", 1)
            joint = pm.ls(sl=1)
            # 进行约束
            if ExtractConstraints == 1:
                pm.select(cl=1)
                if not pm.objExists('ZKM_AllControllerConstraint_Grp'):
                    pm.rename(pm.mel.doGroup(0, 1, 1), 'ZKM_AllControllerConstraint_Grp')
                    pm.parent('ZKM_AllControllerConstraint_Grp', 'ZKM_AllFK_TopGrp')
            for i in range(0, len(joint)):
                if pm.objExists(joint[i] + "_C*"):
                    pm.parentConstraint((joint[i] + "_C*"), joint[i])
                    pm.scaleConstraint((joint[i] + "_C*"), joint[i])
                    if ExtractConstraints == 1:
                        pm.parent((joint[i] + "_scaleConstraint1"), (joint[i] + "_parentConstraint1"),
                                  'ZKM_AllControllerConstraint_Grp')

    # 生成控制器
    def ZKM_ChuangJianFK(self, Name, C_GrpNum, Suffix, RemoveJoint,Colour):
        if pm.objExists('ZKM_FK_AllController'):
            pm.setAttr("ZKM_FK_AllController.visibility", 1)
        pm.select(cl=1)
        pm.select('ZKM_FK_Root')
        pm.mel.SelectHierarchy()
        joint = pm.ls(typ='joint', sl=1)
        if RemoveJoint == True:
            for j in joint:
                q = pm.listRelatives(j, c=1)
                if len(q) == 0:
                    joint.remove(j)
        # 清除不需要创建控制器的
        NoCreate = []
        for j in joint:
            if pm.objExists(j+'.NotGenerate'):
                AttributeName = pm.getAttr(j+'.NotGenerate')
                Dictionary = {}
                if AttributeName == 0:#字符通用码
                    p = pm.listRelatives(j, p=1)
                    c = pm.listRelatives(j,c=1)
                    pm.parent(c,p[0])
                    pm.parent(j,w=1)
                    Dictionary = {'parent':p,'self':j,'child':c}
                    joint.remove(j)
                if AttributeName == 1:#字符通用码
                    pm.select(j)
                    pm.mel.SelectHierarchy()
                    RemoveJoint = pm.ls(typ='joint', sl=1)
                    for r in RemoveJoint:
                        try:
                            joint.remove(r)
                        except:
                            pass
                    p = pm.listRelatives(j, p=1)
                    pm.parent(j,w=1)
                    Dictionary = {'parent':p,'self':j,'child':[]}
                NoCreate.append(Dictionary)
        '''查询其他系统打的组并且转移'''

        # 建立独立控制器
        # 建立总控制器组
        pm.select(cl=1)
        # 创建总字典
        AllDictionary = []
        # 查询是否有创建过，覆盖字典
        HaveAllDictionary = pm.objExists('ZKM_FK_Root_Grp.notes')
        if HaveAllDictionary and pm.objExists('ZKM_FK_AllController'):
            # 清理骨骼约束
            pm.select('ZKM_FK_Root')
            pm.mel.SelectHierarchy()
            pm.mel.DeleteConstraints()
            # 修复骨骼note
            Jnt = pm.ls(typ='joint', sl=1)
            for J in Jnt:
                self.ZKM_SetNumToNotes(J, 32)
            #将上次生成的通用字符数据转换成字典列表
            HaveAllDictionary = pm.getAttr('ZKM_FK_Root_Grp.notes')
            HaveAllDictionary = HaveAllDictionary.encode('utf-8')  # 字符通用码转为字符串
            HaveAllDictionary = HaveAllDictionary.split('\n')
            del HaveAllDictionary[-1:]
            for h in range(0, len(HaveAllDictionary)):  # 把字符串列表转换成字典列表
                StrDictionary = eval(HaveAllDictionary[h])
                HaveAllDictionary[h] = StrDictionary
            # 修复所有组的note
            pm.select('ZKM_FK_Root_G1*')
            RootGrp = pm.ls(sl=1)
            OldSuffix = RootGrp[0][14:]
            pm.mel.SelectHierarchy()
            Transform = pm.ls(typ='transform', sl=1)
            for G in Transform:
                self.ZKM_SetNumToNotes(G, 32)
            # 查询上次生成的样条是否缺失，缺失的话进行补充,没有缺失就进行改名，改成对应骨骼名称的上次生成的结构
            LastGrpNum = HaveAllDictionary[0].get('Grp')#获取上次生成打的组
            for Dictionary in HaveAllDictionary:
                self.ZKM_ReturnNotesToModel(joint, Dictionary, 'joint', 0)
                J = pm.ls(sl=1)
                C_Num = str(Dictionary.get('Curve'))
                self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Curve', 0)
                C = pm.ls(sl=1)
                if J:
                    if not C:
                        # 建立基础控制器并改名
                        pm.rename(ZKM_CreateAndEditCurveClass().ZKM_CreateCurve(
                            (File_RootDirectory + '\MayaCommon\CurveShapeWithPicture'), Name), J[0] + "_C" + Suffix)
                        nurbs = pm.ls(sl=1)
                        self.ZKM_ModifyControllerShapeTRS('SoftSelectionSize', 0, 0, 0)
                        if not nurbs[0].hasAttr('notes'):
                            nurbs[0].addAttr('notes', type='string')
                        nurbs[0].attr('notes').set(C_Num)#按原样修复样条note
                        ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor(nurbs, Colour)
                        pm.parent(nurbs[0],'ZKM_FK_Root_C' + OldSuffix)
                        # 建立旧样条组，并将旧32位绝对数还原到修复组中
                        for n in range(0,len(LastGrpNum)):
                            if pm.objExists(J[0] + "_G" + str((len(LastGrpNum)-n)) + OldSuffix):
                                pm.select((J[0] + "_G" + str((len(LastGrpNum)-n)) + OldSuffix))
                                TopGrp = pm.ls(sl=1)
                            else:
                                if n == 0:
                                    pm.select(nurbs[0])
                                else:
                                    pm.select(J[0] + "_G" + str((len(LastGrpNum) - n + 1)) + OldSuffix)
                                pm.mel.doGroup(0, 1, 1)
                                pm.mel.rename(J[0] + "_G" + str((len(LastGrpNum)-n)) + OldSuffix)
                                TopGrp = pm.ls(sl=1)
                            if not TopGrp[0].hasAttr('notes'):
                                TopGrp[0].addAttr('notes', type='string')
                            TopGrp[0].attr('notes').set(Dictionary['Grp'][n])#按原样修复样条note
                        for n in range(0, len(LastGrpNum)-1):
                            pm.parent((J[0] + "_G" + str((len(LastGrpNum)-n)) + OldSuffix), (J[0] + "_G" + str((len(LastGrpNum)-1-n)) + OldSuffix))
                        pm.parent(nurbs[0],(J[0] + "_G" + str(len(LastGrpNum)) + OldSuffix))
                    else:
                        G_Num = Dictionary.get('Grp')
                        self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Curve', 0)
                        pm.mel.rename(J[0] + "_C" + OldSuffix)  # 修复所有存在样条的名称
                        for g in range(0,len(G_Num)):
                            self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Grp', g)
                            G = pm.ls(sl=1)
                            if not G[0]:
                                pm.select(J[0] + '_C' + OldSuffix)
                                pm.mel.doGroup(0, 1, 1)
                                pm.mel.rename(J[0] + "_G" + str(len(G_Num) - g) + OldSuffix)
                                TopGrp = pm.ls(sl=1)
                                if not TopGrp[0].hasAttr('notes'):
                                    TopGrp[0].addAttr('notes', type='string')
                                TopGrp[0].attr('notes').set(Dictionary['Grp'][g])#按原样修复样条note
                            else:
                                pm.mel.rename(J[0] + "_G" + str(len(G_Num) - g) + OldSuffix)#修复所有存在样条组的名称
                else:
                    self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Curve', 0)
                    Cur = pm.ls(sl=1)
                    AllDelete = []
                    if Cur:
                        Transform.remove(Cur[0])
                        AllDelete.append(Cur)
                    G_Num = Dictionary.get('Grp')
                    for g in range(0, len(G_Num)):
                        self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Grp', g)
                        Grp = pm.ls(sl=1)
                        if Grp:
                            Transform.remove(Grp[0])
                            AllDelete.append(Grp[0])
                    for D in AllDelete:
                        Parent = pm.listRelatives(D,p=1)
                        subset = pm.listRelatives(D,c=1,type='transform')
                        for s in subset:
                            pm.parent(s,Parent[0])
                        pm.delete(D)
                    # 此时已经完成了现存原骨骼所有组的新名称旧后缀还原###################################

            # 假如要生成的组数比原本的组少则进行解组
            if C_GrpNum < len(LastGrpNum):
                WantingGrpNum = len(LastGrpNum) - C_GrpNum
                # 查询需解组的组是否存在
                for Dictionary in HaveAllDictionary:
                    for l in range(0, WantingGrpNum):
                        self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Grp', l)
                        sel = pm.ls(sl=1)
                        if sel:
                            Transform.remove(sel[0])
                            pm.mel.ungroup()

            # 假如要生成的组数比原本的组多则进行加组
            if C_GrpNum > len(LastGrpNum):
                WantingGrpNum = C_GrpNum - len(LastGrpNum)
                for Dictionary in HaveAllDictionary:
                    for l in range(0, WantingGrpNum):
                        self.ZKM_ReturnNotesToModel(Transform, Dictionary, 'Curve', 0)
                        C = pm.ls(sl=1)
                        pm.mel.doGroup(0, 1, 1)
                        pm.mel.rename(str(C[0][:-2]) + "_G" + str((len(LastGrpNum) + 1 + l)) + OldSuffix)
                        TopGrp = pm.ls(sl=1)
                        self.ZKM_SetNumToNotes(TopGrp[0], 32)

            # 修正后缀
            for T in Transform:
                if pm.objExists(T):
                    if len(OldSuffix) == 0:
                        pm.rename(T, T + Suffix)
                    if T[-1*len(OldSuffix):] == OldSuffix:
                        pm.rename(T,T[:-1*len(OldSuffix)]+Suffix)

            # 判断是否有添加的骨骼，进行正常生成控制器
            for J in joint:
                if not pm.objExists(J + "_C" + Suffix):
                    # 建立控制器
                    pm.rename(ZKM_CreateAndEditCurveClass().ZKM_CreateCurve(
                        (File_RootDirectory + '\MayaCommon\CurveShapeWithPicture'), Name), J + "_C" + Suffix)
                    nurbs = pm.ls(sl=1)
                    self.ZKM_ModifyControllerShapeTRS('SoftSelectionSize', 0, 0, 0)
                    ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor(nurbs, Colour)
                    self.ZKM_SetNumToNotes(nurbs[0], 32)
                    for j in range(0, C_GrpNum):
                        pm.mel.doGroup(0, 1, 1)
                        # 建立样条组
                        pm.mel.rename(J + "_G" + str((C_GrpNum - j)) + Suffix)
                        Grp = pm.ls(sl=1)
                        self.ZKM_SetNumToNotes(Grp[0], 32)
            pm.select(cl=1)
            for J in joint:
                pm.select(J + "_G1" + Suffix)
                TopGrp = pm.ls(sl=1)
                pm.parent(TopGrp[0],'ZKM_FK_AllController')
            # 创建新字典AllDictionary
            for J in joint:
                J_NumList = []
                J_Num = pm.getAttr(J+'.notes')
                J_Num = J_Num.encode('utf-8')
                J_NumList.append(J_Num)
                C_NumList = []
                C_Num = pm.getAttr(J + "_C" + Suffix+'.notes')
                C_Num = C_Num.encode('utf-8')
                C_NumList.append(C_Num)
                G_Num = []
                for i in range(0,C_GrpNum):
                    GrpNum = pm.getAttr((J + "_G" + str((C_GrpNum - i)) + Suffix+'.notes'))
                    GrpNum = GrpNum.encode('utf-8')
                    G_Num.append(GrpNum)
                Dictionary = {'joint':J_NumList,'Curve':C_NumList,'Grp':G_Num}
                AllDictionary.append(Dictionary)
        else:
            pm.select(cl=1)
            pm.group(n='ZKM_FK_AllController')
            pm.parent('ZKM_FK_AllController', 'ZKM_AllFK_TopGrp')
            for J in joint:
                J_nume = []
                #给骨骼添加32位随机数
                if not J.hasAttr('notes'):
                    self.ZKM_SetNumToNotes(J, 32)
                J_nume.append(pm.getAttr(J + '.notes').encode('utf-8'))
                #建立基础控制器并改名
                pm.rename(ZKM_CreateAndEditCurveClass().ZKM_CreateCurve((File_RootDirectory + '\MayaCommon\CurveShapeWithPicture'), Name), str(J) + "_C" + Suffix)
                nurbs = pm.ls(sl=1)
                self.ZKM_ModifyControllerShapeTRS('SoftSelectionSize', 0, 0, 0)
                ZKM_CreateAndEditCurveClass().ZKM_ChangeCurveColor(nurbs, Colour)
                # 给曲线添加32位随机数
                if not nurbs[0].hasAttr('notes'):
                    self.ZKM_SetNumToNotes(nurbs[0], 32)
                nurbs_nume = []
                nurbs_nume.append(pm.getAttr(nurbs[0] + '.notes').encode('utf-8'))
                TopGrp_Num = []
                #循环创建控制器组，且给添加32位随机数
                for j in range(0, C_GrpNum):
                    pm.mel.doGroup(0, 1, 1)
                    # 建立样条组
                    pm.mel.rename(str(J) + "_G" + str((C_GrpNum - j)) + Suffix)
                    Grp = pm.ls(sl=1)
                    if not Grp[0].hasAttr('notes'):
                        self.ZKM_SetNumToNotes(Grp[0], 32)
                    Grp_Num = pm.getAttr(Grp[0] + '.notes')
                    TopGrp_Num.append(Grp_Num.encode('utf-8'))
                pm.parent((str(J) + "_G1"+ Suffix),'ZKM_FK_AllController')
                #建立骨骼关联字典
                LocalDictionary = {'joint':J_nume,'Curve':nurbs_nume,'Grp':TopGrp_Num}
                #将关联字典添加到总字典
                AllDictionary.append(LocalDictionary)
        #将总字典添加到骨骼组
        pm.select('ZKM_FK_Root_Grp')
        RootGrp = pm.ls(sl=1)
        if not RootGrp[0].hasAttr('notes'):
            RootGrp[0].addAttr('notes', type='string')
        Txt = ''
        for D in AllDictionary:
            Txt = Txt + str(D) + '\n'
        RootGrp[0].attr('notes').set(Txt)

        # 创建控制器查询范围
        pm.select('ZKM_FK_AllController')
        pm.mel.SelectHierarchy()
        pm.select(cl=1)
        NeedDeleteConstraint = []
        for J in joint:#开始矫正位置
            for i in range(0,C_GrpNum):
                # 查询是否有约束，有则进行偏移处理
                # 将约束分为位移和旋转两部分
                try:
                    Constraint = pm.parentConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                    TranslateConstraint = Constraint
                    RotateConstraint = Constraint
                except:
                    try:
                        Constraint = pm.pointConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                        TranslateConstraint = Constraint
                    except:
                        TranslateConstraint = []
                    try:
                        Constraint = pm.orientConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                        RotateConstraint = Constraint
                    except:
                        try:
                            Constraint = pm.aimConstraint((str(J) + "_G" + str(i + 1) + Suffix), wal=1)
                            RotateConstraint = Constraint
                        except:
                            RotateConstraint = []
                # 开始处理位移和旋转
                # 把定位器p到对应的约束源
                # 获取需要的位移和旋转值赋予到对应约束的偏移值
                # 删除定位器
                if TranslateConstraint:
                    NumLoc = pm.spaceLocator()
                    parent = pm.listRelatives(TranslateConstraint, p=1)
                    parent = pm.listRelatives(parent, p=1)
                    pm.parent(NumLoc, parent[0])
                    pm.parentConstraint(J, NumLoc)
                    Num = pm.getAttr(str(NumLoc) + '.t')
                    pm.setAttr((str(J) + "_G" + str(i + 1) + Suffix + '.t'), Num)
                    if pm.ls(TranslateConstraint, type='parentConstraint'):
                        Soure = pm.parentConstraint(TranslateConstraint, q=1, tl=1)
                        pm.parentConstraint(Soure, TranslateConstraint, mo=1, e=1)
                        '''SoureT = pm.listConnections(str(TranslateConstraint) + ".target[*].targetTranslate", s=True, scn=True,d=False)
                        n = 0
                        pm.spaceLocator(p=(0, 0, 0))
                        locT = pm.ls(sl=1)
                        pm.delete(pm.parentConstraint(J, locT))
                        for ST in SoureT:
                            # 建立定位器被对应的骨骼约束
                            pm.parent(locT,ST)
                            TX = pm.getAttr(locT[0] + '.translateX')
                            TY = pm.getAttr(locT[0] + '.translateY')
                            TZ = pm.getAttr(locT[0] + '.translateZ')
                            pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetTranslateX', TX)
                            pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetTranslateY', TY)
                            pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetTranslateZ', TZ)
                            n = n + 1
                        pm.delete(locT)'''
                    if pm.ls(TranslateConstraint, type='pointConstraint'):
                        Soure = pm.pointConstraint(TranslateConstraint, q=1, tl=1)
                        pm.pointConstraint(Soure, TranslateConstraint, mo=1, e=1)
                    pm.delete(NumLoc)
                if RotateConstraint:
                    NumLoc = pm.spaceLocator()
                    parent = pm.listRelatives(RotateConstraint, p=1)
                    parent = pm.listRelatives(parent, p=1)
                    pm.parent(NumLoc, parent[0])
                    pm.parentConstraint(J, NumLoc)
                    Num = pm.getAttr(str(NumLoc) + '.r')
                    pm.setAttr((str(J) + "_G" + str(i + 1) + Suffix + '.r'), Num)
                    if pm.ls(RotateConstraint, type='parentConstraint'):
                        Soure = pm.parentConstraint(RotateConstraint, q=1, tl=1)
                        pm.parentConstraint(Soure, RotateConstraint, mo=1, e=1)
                        '''SoureR = pm.listConnections(str(RotateConstraint) + ".target[*].targetRotate", s=True, scn=True, d=False)
                        n = 0
                        pm.spaceLocator(p=(0, 0, 0))
                        locR = pm.ls(sl=1)
                        pm.delete(pm.parentConstraint(J, locR))
                        for ST in SoureR:
                            # 建立定位器被对应的骨骼约束
                            pm.parent(locR, ST)
                            TX = pm.getAttr(locR[0] + '.rotateX')
                            TY = pm.getAttr(locR[0] + '.rotateY')
                            TZ = pm.getAttr(locR[0] + '.rotateZ')
                            pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetRotateX', TX)
                            pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetRotateY', TY)
                            pm.setAttr(str(TranslateConstraint) + '.target[' + str(n) + '].targetOffsetRotateZ', TZ)
                            n = n + 1
                        pm.delete(locR)'''
                    if pm.ls(RotateConstraint, type='orientConstraint'):
                        Soure = pm.orientConstraint(RotateConstraint, q=1, tl=1)
                        pm.orientConstraint(Soure, RotateConstraint, mo=1, e=1)
                    if pm.ls(RotateConstraint, type='aimConstraint'):
                        Soure = pm.aimConstraint(RotateConstraint, q=1, tl=1)
                        pm.aimConstraint(Soure, RotateConstraint, mo=1, e=1)
                    pm.delete(NumLoc)
                ###################################################
                if not (TranslateConstraint and RotateConstraint):
                    NeedDeleteConstraint.append(pm.parentConstraint(str(J),(str(J) + "_G" + str(i+1) + Suffix)))
            NeedDeleteConstraint.append(pm.parentConstraint(str(J), (str(J) + "_C" + Suffix)))
        for D in NeedDeleteConstraint:
            pm.delete(D)
        # 进行父化
        for i in range(1, len(joint)):
            Parent = pm.listRelatives(joint[i], p=1)
            pm.select(Parent)
            jointLX = pm.ls(typ='joint', sl=1)
            while not jointLX:
                Parent = pm.listRelatives(p=1)
                pm.select(Parent, r=1)
                jointLX = pm.ls(typ='joint', sl=1)
            Parent = pm.ls(sl=1)
            for j in range(0, len(joint)):
                if joint[j] == Parent[0]:
                    pm.parent(joint[i]+'_G1' + Suffix, joint[j]+'_C' + Suffix)
                    break
        # 是否提取约束
        ExtractConstraints = pm.checkBox('WindowControllerProcessingExtractConstraints', q=1, value=1)
        # 进行约束
        if ExtractConstraints == 1:
            pm.select(cl=1)
            if not pm.objExists('ZKM_AllControllerConstraint_Grp'):
                pm.rename(pm.mel.doGroup(0, 1, 1), 'ZKM_AllControllerConstraint_Grp')
                pm.parent('ZKM_AllControllerConstraint_Grp','ZKM_AllFK_TopGrp')
        for i in range(0, len(joint)):
            pm.parentConstraint((joint[i] + "_C" + Suffix), joint[i])
            pm.scaleConstraint((joint[i] + "_C" + Suffix), joint[i])
            if ExtractConstraints == 1:
                pm.parent((joint[i] + "_scaleConstraint1"), (joint[i] + "_parentConstraint1"), 'ZKM_AllControllerConstraint_Grp')
        # 还原原本的骨骼
        for NC in NoCreate:
            pm.parent(NC.get('self'),NC.get('parent')[0])
            if NC.get('child'):
                pm.parent(NC.get('child'), NC.get('self'))
        # 其他系统 #############################################################################################################
        if pm.objExists('ZKM_OtherSystem'):
            pm.setAttr('ZKM_OtherSystem.v',1)
            pm.setAttr("ZKM_OtherSystemShape.visibility", 0)
        else:
            pm.spaceLocator(n='ZKM_OtherSystem')
            pm.parent('ZKM_OtherSystem','ZKM_AllFK_TopGrp')
            pm.setAttr("ZKM_OtherSystemShape.visibility", 0)
        for n in ['IK','SplineIK','AIM','Wheel','Hand','foot']:
            if pm.objExists('ZKM_'+n+'_System'):
                pm.setAttr('ZKM_'+n+'_System.v',1)
                pm.setAttr('ZKM_'+n+'_SystemShape.visibility', 0)
            else:
                pm.spaceLocator(n='ZKM_'+n+'_System')
                pm.parent('ZKM_'+n+'_System','ZKM_OtherSystem')
                pm.setAttr('ZKM_'+n+'_SystemShape.visibility', 0)
        pm.select('ZKM_FK_Root')
        pm.mel.SelectHierarchy()
        joint = pm.ls(typ='joint', sl=1)
        '''for j in joint:
            Attribute = pm.listAttr(userDefined=True)
            if Attribute:
                for At in Attribute:
                    if At == 'IK':# 自带极向量和切换
                        IK_Joint = pm.attributeQuery('IK', node=j, listEnum=1)
                    if At == 'SplineIK': # 样条IK
                        SplineIK_Joint = pm.attributeQuery('SplineIK', node=j, listEnum=1)
                    if At == 'AIM': # 眼部朝向
                        SplineIK_Joint = pm.attributeQuery('SplineIK', node=j, listEnum=1)
                    if At == 'Wheel':# 轮胎驱动
                        pass
                    if At == 'Hand':# 手部驱动
                        SplineIK_Joint = pm.attributeQuery('Hand', node=j, listEnum=1)
                    if At == 'foot':  # 脚部驱动
                        SplineIK_Joint = pm.attributeQuery('foot', node=j, listEnum=1)'''
    def ZKM_ChuangJianFK_2(self, Name, C_GrpNum, Suffix, RemoveJoint):
        pm.select('ZKM_FK_Root')
        pm.mel.SelectHierarchy()
        joint = pm.ls(typ='joint', sl=1)
        ALL = pm.ls(sl=1)
        if RemoveJoint == True:
            for j in joint:
                q = pm.listRelatives(j, c=1)
                if len(q) == 0:
                    joint.remove(j)
        # 建立独立控制器
        # 建立总控制器组
        pm.select(cl=1)
        pm.group(n='ZKM_FK_AllController')
        pm.parent('ZKM_FK_AllController', 'ZKM_AllFK_TopGrp')
        # 创建总字典
        AllDictionary = []
        for J in joint:
            J_nume = []
            # 给骨骼添加32位随机数
            if not J.hasAttr('notes'):
                self.ZKM_SetNumToNotes(J, 32)
            J_nume.append(pm.getAttr(J + '.notes'))
            # 建立基础控制器并改名
            pm.rename(ZKM_CreateAndEditCurveClass().ZKM_CreateCurve(
                (File_RootDirectory + '\MayaCommon\CurveShapeWithPicture'), Name), str(J) + "_C" + Suffix)
            nurbs = pm.ls(sl=1)
            # 给曲线添加32位随机数
            if not nurbs[0].hasAttr('notes'):
                self.ZKM_SetNumToNotes(nurbs[0], 32)
            nurbs_nume = []
            nurbs_nume.append(pm.getAttr(nurbs[0] + '.notes'))
            TopGrp_Num = []
            # 循环创建控制器组，且给添加32位随机数
            for j in range(0, C_GrpNum):
                Grp_Num = []
                pm.mel.doGroup(0, 1, 1)
                # 建立样条组
                pm.mel.rename(str(J) + "_G" + str((C_GrpNum - j)) + Suffix)
                Grp = pm.ls(sl=1)
                if not Grp[0].hasAttr('notes'):
                    self.ZKM_SetNumToNotes(Grp[0], 32)
                Grp_Num = pm.getAttr(Grp[0] + '.notes')
                TopGrp_Num.append(Grp_Num)
            pm.parent((str(J) + "_G1" + Suffix), 'ZKM_FK_AllController')
            # 建立骨骼关联字典
            LocalDictionary = {'joint': J_nume, 'Curve': nurbs_nume, 'Grp': TopGrp_Num}
            # 将关联字典添加到总字典
            AllDictionary.append(LocalDictionary)
        # 将总字典添加到骨骼组
        pm.select('ZKM_FK_Root_Grp')
        RootGrp = pm.ls(sl=1)
        if not RootGrp[0].hasAttr('notes'):
            RootGrp[0].addAttr('notes', type='string')
        Txt = ''
        for D in AllDictionary:
            Txt = Txt + str(D) + '\n'
        RootGrp[0].attr('notes').set(Txt)

        pm.select('ZKM_FK_AllController')
        pm.mel.SelectHierarchy()
        AllControllerInformation = pm.ls(sl=1)
        pm.select(cl=1)
        # 进行父化
        for i in range(1, len(joint)):
            Parent = pm.listRelatives(joint[i], p=1)
            pm.select(Parent)
            jointLX = pm.ls(typ='joint', sl=1)
            while not jointLX:
                Parent = pm.listRelatives(p=1)
                pm.select(Parent, r=1)
                jointLX = pm.ls(typ='joint', sl=1)
            Parent = pm.ls(sl=1)
            self.ZKM_ReturnNotesToModel(AllControllerInformation, AllDictionary[i], 'Grp', -1)
            TopGrp = pm.ls(sl=1)
            for j in range(0, len(joint)):
                self.ZKM_ReturnNotesToModel(AllControllerInformation, AllDictionary[j], 'Curve', 0)
                nurbs = pm.ls(sl=1)
                if joint[j] == Parent[0]:
                    pm.parent(TopGrp[0], nurbs[0])
                    break
        # 是否提取约束
        ExtractConstraints = pm.checkBox('WindowControllerProcessingExtractConstraints', q=1, value=1)
        # 进行约束
        if ExtractConstraints == 1:
            pm.select(cl=1)
            if not pm.objExists("ZiJianKZQyveshu"):
                pm.rename(pm.mel.doGroup(0, 1, 1), "ZiJianKZQyveshu")
        for i in range(0, len(joint)):
            pm.parentConstraint((joint[i] + "_C" + Suffix), joint[i])
            pm.scaleConstraint((joint[i] + "_C" + Suffix), joint[i])
            if ExtractConstraints == 1:
                pm.parent((joint[i] + "_scaleConstraint1"), (joint[i] + "_parentConstraint1"), "ZiJianKZQyveshu")

        t = pm.getAttr('ZKM_FK_Root_Grp.notes')
        #print (t.split('\n')[0])