#coding=gbk
import pymel.core as cmds
#创建基础
Joint = cmds.textFieldButtonGrp('ZKM_RopeWindow_AddJoint',  q=1 , text=1)#加载顶骨骼
Curve = cmds.textFieldButtonGrp('ZKM_RopeWindow_AddCurve',  q=1 , text=1)#加载样条
Prefix = cmds.textFieldButtonGrp('ZKM_RopeWindow_Prefix', q=1 , text=1)#加载前缀
print Joint
print Curve
print Prefix
cmds.select(Joint)
cmds.mel.SelectHierarchy()
Joint = cmds.ls(sl=1,type='joint')
print Joint
cmds.select(Curve+'.cv[*]')
CurvePoint = cmds.ls(sl=1,fl=1)
print CurvePoint[0]
All_BaseController_Grp = cmds.group(em=1,n=(Prefix+'All_BaseController_Grp'))

Cluster = []
Num = []
for i in range(-1,1):
    cmds.select(CurvePoint[i])
    C = cmds.mel.newCluster(" -envelope 1")
    num = cmds.getAttr(C[1]+'.rotatePivot')
    Num.append(num)
    Cluster.append(C[1])

Num = abs(Num[0]-Num[1])
SurfaceDirection = [0, 0, 1]
if Num[2] > Num[0]:
    SurfaceDirection = [1, 0, 0]
cmds.delete(Cluster)



#创建基础控制器
i = 0
for Point in CurvePoint:
    cmds.select(Point)
    Cluster = cmds.mel.newCluster(" -envelope 1")
    cmds.setAttr((Cluster[1] + '.v'), 0)
    BaseCurve = cmds.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(0, 1, 0),
                n=(Prefix + str(i) + '_BaseController'))
    cmds.group(n=(Prefix + str(i) + '_BaseController_Grp2'))
    TopGrp = cmds.group(n=(Prefix + str(i) + '_BaseController_Grp1'))
    cmds.delete(cmds.parentConstraint(Cluster[1],TopGrp,w=1))
    cmds.parent(Cluster[1], BaseCurve[0])
    cmds.parent(TopGrp,All_BaseController_Grp)
    i = i + 1
#创建IK
cmds.select(Joint[0],Joint[-1],Curve)
cmds.ikHandle(ccv=False, sol='ikSplineSolver')
IK = cmds.ls(sl=1)
#创建曲面
cmds.extrude(Curve, upn=0, dl=1, ch=0, rotation=0, d=SurfaceDirection, length=1, scale=1, et=0, rn=True, po=0)
Surface = cmds.ls(sl=1)
cmds.move(0, 0, -0.5, r=1, os=1, wd=1)
cmds.mel.channelBoxCommand('-freezeTranslate')
#创建控制曲面的蔟
for i in range(0,len(CurvePoint)):
    cmds.select(Surface[0]+'.cv['+ str(i) + '][0:*]')
    Cluster = cmds.mel.newCluster(" -envelope 1")
    cmds.setAttr((Cluster[1] + '.v'), 0)
    cmds.parent(Cluster[1], (Prefix + str(i) + '_BaseController'))
#创建毛囊附着表面跟随骨骼
All_JointFollicle_Grp = cmds.group(em=1,n=(Prefix+'All_JointFollicle_Grp'))
shape = cmds.listRelatives(Surface,s=1)
for i in range(0,len(Joint)):
    cpom = cmds.createNode('closestPointOnSurface')
    cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
    decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
    cmds.connectAttr((Joint[i] + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
    cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
    follicleShape = cmds.createNode('follicle', n=(Joint[i] + '_follicleShape'))
    follicle = cmds.listRelatives(follicleShape,p=1)
    cmds.connectAttr((shape[0] + '.worldSpace[0]'), (Joint[i] + '_follicleShape' + '.inputSurface'), f=1)
    cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (Joint[i] + '_follicleShape' + '.inputWorldMatrix'), f=1)
    cmds.connectAttr((Joint[i] + '_follicleShape' + ".outTranslate"), (Joint[i] + '_follicle' + '.translate'), f=1)
    cmds.connectAttr((Joint[i] + '_follicleShape' + ".outRotate"), (Joint[i] + '_follicle' + ".rotate"), f=1)
    cmds.connectAttr((cpom + '.parameterU'), (Joint[i] + '_follicle' + '.parameterU'), f=1)
    cmds.connectAttr((cpom + '.parameterV'), (Joint[i] + '_follicle' + '.parameterV'), f=1)
    cmds.select(cl=1)
    joint = cmds.joint(p=(0, 0, 0),n=(Joint[i] + 'SkinJoint'))
    cmds.delete(cmds.parentConstraint(follicle[0],joint))
    if i > 0:
        cmds.parent(joint,(Joint[i-1] + 'SkinJoint'))
    cmds.parent(follicle[0],All_JointFollicle_Grp)
cmds.select(Joint[0] + 'SkinJoint')
cmds.mel.channelBoxCommand('-freezeAll')
cmds.joint(zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')
for i in range(0,len(Joint)):
    cmds.parentConstraint((Joint[i] + '_follicle'),(Joint[i] + 'SkinJoint'),mo=1,w=1)

#cmds.setAttr((Prefix + Joint[0] + '_SkinJoint_Grp.v'), 0)

#整理文件
cmds.group(Joint[0],Curve,IK[0],n=(Prefix+'SpineIkSys_Grp'))
cmds.group((Joint[0] + 'SkinJoint'),n=(Prefix + Joint[0] + '_SkinJoint_Grp'))
cmds.setAttr('Rope_Joint0_SkinJoint_Grp.useOutlinerColor', True)
cmds.setAttr('Rope_Joint0_SkinJoint_Grp.outlinerColor', 1, 0, 0)
cmds.group(Surface[0],All_JointFollicle_Grp,n=(Prefix+'follicleAttachmentSys_Grp'))
cmds.group(All_BaseController_Grp,(Prefix + Joint[0] + '_SkinJoint_Grp'),(Prefix+'SpineIkSys_Grp'),(Prefix+'follicleAttachmentSys_Grp'),
           n=(Prefix+'BasicPart_Grp'))
#创建总控制
BaseCurve = cmds.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=2, tol=0.01, nr=(0, 1, 0),
                n=(Prefix + 'TotalControl_Curve'))
cmds.group(n=(Prefix + 'TotalControl_Grp2'))
cmds.group(n=(Prefix + 'TotalControl_Grp1'))
cmds.delete(cmds.parentConstraint((Prefix + str(len(CurvePoint)-1) + '_BaseController'),(Prefix + 'TotalControl_Grp1'),w=1))
cmds.parentConstraint((Prefix + 'TotalControl_Curve'),(Prefix+'BasicPart_Grp'),mo=1,w=1)
cmds.scaleConstraint((Prefix + 'TotalControl_Curve'),(Prefix+'BasicPart_Grp'),mo=1)
cmds.setAttr((Curve+'.inheritsTransform'), 0)
cmds.setAttr((Prefix+'follicleAttachmentSys_Grp.inheritsTransform'), 0)

cmds.group((Prefix + 'TotalControl_Grp1'),(Prefix+'BasicPart_Grp'),n=(Prefix+'All_Grp'))
cmds.setAttr((Prefix+'SpineIkSys_Grp.v'), 0)
cmds.setAttr((Prefix+'follicleAttachmentSys_Grp.v'), 0)
######################################################################################################################
#拉伸修改版本
All_JointFollicle_Grp = cmds.group(em=1,n=(Prefix+'All_JointLongFollicle_Grp'))
shape = cmds.listRelatives(Surface,s=1)
#创建固定毛囊
for i in range(0,len(Joint)):
    cpom = cmds.createNode('closestPointOnSurface')
    cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
    decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
    cmds.connectAttr((Joint[i] + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
    cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
    follicleShape = cmds.createNode('follicle', n=(Joint[i] + '_LongfollicleShape'))
    follicle = cmds.listRelatives(follicleShape,p=1)
    cmds.connectAttr((shape[0] + '.worldSpace[0]'), (Joint[i] + '_LongfollicleShape' + '.inputSurface'), f=1)
    cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (Joint[i] + '_LongfollicleShape' + '.inputWorldMatrix'), f=1)
    cmds.connectAttr((Joint[i] + '_LongfollicleShape' + ".outTranslate"), (Joint[i] + '_Longfollicle' + '.translate'), f=1)
    cmds.connectAttr((Joint[i] + '_LongfollicleShape' + ".outRotate"), (Joint[i] + '_Longfollicle' + ".rotate"), f=1)
    cmds.setAttr((Joint[i] + '_Longfollicle' + '.parameterU'), cmds.getAttr(cpom + '.parameterU'))
    cmds.setAttr((Joint[i] + '_Longfollicle' + '.parameterV'), cmds.getAttr(cpom + '.parameterV'))
    cmds.select(cl=1)
    cmds.parent(follicle[0], All_JointFollicle_Grp)
#创建曲面
cmds.extrude(Curve, upn=0, dl=1, ch=0, rotation=0, d=(0, 0, 1), length=1, scale=1, et=0, rn=True, po=0)
Surface = cmds.ls(sl=1)
All_JointFollicle_Grp = cmds.group(em=1,n=(Prefix+'All_JointBaseFollicle_Grp'))
shape = cmds.listRelatives(Surface,s=1)
#创建固定毛囊
for i in range(0,len(Joint)):
    cpom = cmds.createNode('closestPointOnSurface')
    cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
    decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
    cmds.connectAttr((Joint[i] + '.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
    cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
    follicleShape = cmds.createNode('follicle', n=(Joint[i] + '_BasefollicleShape'))
    follicle = cmds.listRelatives(follicleShape,p=1)
    cmds.connectAttr((shape[0] + '.worldSpace[0]'), (Joint[i] + '_BasefollicleShape' + '.inputSurface'), f=1)
    cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (Joint[i] + '_BasefollicleShape' + '.inputWorldMatrix'), f=1)
    cmds.connectAttr((Joint[i] + '_BasefollicleShape' + ".outTranslate"), (Joint[i] + '_Basefollicle' + '.translate'), f=1)
    cmds.connectAttr((Joint[i] + '_BasefollicleShape' + ".outRotate"), (Joint[i] + '_Basefollicle' + ".rotate"), f=1)
    cmds.setAttr((Joint[i] + '_Basefollicle' + '.parameterU'),cmds.getAttr(cpom + '.parameterU'))
    cmds.setAttr((Joint[i] + '_Basefollicle' + '.parameterV'),cmds.getAttr(cpom + '.parameterV'))
    cmds.select(cl=1)
    cmds.parent(follicle[0], All_JointFollicle_Grp)
#创建前后两个距离
for i in range(1,len(Joint)):
    # 新毛囊之间的距离
    New_distanceBetween = cmds.shadingNode('distanceBetween', asUtility=1)
    cmds.connectAttr((Joint[i-1]+'_Longfollicle.translate'), (New_distanceBetween + '.point1'), force=1)
    cmds.connectAttr((Joint[i] + '_Longfollicle.translate'), (New_distanceBetween + '.point2'), force=1)
    # 旧毛囊之间的距离
    Old_distanceBetween = cmds.shadingNode('distanceBetween', asUtility=1)
    cmds.connectAttr((Joint[i - 1] + '_Basefollicle.translate'), (Old_distanceBetween + '.point1'), force=1)
    cmds.connectAttr((Joint[i] + '_Basefollicle.translate'), (Old_distanceBetween + '.point2'), force=1)
    # 查询新旧毛囊距离的缩放比例
    multiplyDivide_Divid = cmds.shadingNode('multiplyDivide', asUtility=1)
    cmds.setAttr((multiplyDivide_Divid+'.operation'),2)
    cmds.connectAttr((Old_distanceBetween + '.distance'), (multiplyDivide_Divid + '.input1.input1X'), force=1)
    cmds.connectAttr((New_distanceBetween+'.distance'), (multiplyDivide_Divid + '.input2.input2X'), force=1)
    # 确定需修改u值
    Differ_U_Num = cmds.getAttr(Joint[i] + '_follicleShape.parameterU') - cmds.getAttr(Joint[i - 1] + '_follicleShape.parameterU')
    multiplyDivide_multiply = cmds.shadingNode('multiplyDivide', asUtility=1)
    cmds.connectAttr((multiplyDivide_Divid + '.output.outputX'), (multiplyDivide_multiply + '.input1.input1X'), force=1)
    cmds.setAttr((multiplyDivide_multiply + '.input2.input2X'),Differ_U_Num)
    # 给毛囊赋予准确数值
    plusMinusAverage = cmds.shadingNode('plusMinusAverage', asUtility=1)
    cmds.connectAttr((multiplyDivide_multiply + '.output.outputX'), (plusMinusAverage + '.input1D[0]'), force=1)
    cmds.connectAttr((Joint[i - 1] + '_follicleShape.parameterU'), (plusMinusAverage + '.input1D[1]'), force=1)
    #cmds.setAttr((plusMinusAverage + '.input1D[1]'), cmds.getAttr(Joint[i - 1] + '_follicleShape.parameterU'))
    #链接到输出位置的毛囊
    cmds.connectAttr((plusMinusAverage + '.output1D'), (Joint[i] + '_follicleShape.parameterU'), force=1)












########################################################################################################################
#添加拉伸
CurveShape = cmds.listRelatives(Curve,s=1)
cmds.select(cmds.duplicate(Curve,rr=1))
CopyCurve = cmds.ls(sl=1)
CopyCurveShape = cmds.listRelatives(CopyCurve,s=1)
multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
cmds.setAttr((multiplyDivide+'.operation'), 2)
curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
cmds.connectAttr((CurveShape[0]+'.worldSpace[0]'), (curveInfo+'.inputCurve'), force=1)
cmds.connectAttr((curveInfo+'.arcLength'), (multiplyDivide+'.input1X'), f=1)
curveInfo = cmds.shadingNode('curveInfo', asUtility=1)
cmds.connectAttr((CopyCurveShape[0]+'.worldSpace[0]'), (curveInfo+'.inputCurve'), force=1)
cmds.connectAttr((curveInfo+'.arcLength'), (multiplyDivide+'.input2X'), f=1)
#添加拉伸开关
cmds.addAttr((Prefix + 'TotalControl_Curve'), ln='stretch', at='bool')
cmds.setAttr((Prefix + 'TotalControl_Curve.stretch'), e=1, keyable=True)
cmds.addAttr((Prefix + 'TotalControl_Curve'), ln='StretchMagnification', dv=1, at='double')
cmds.setAttr((Prefix + 'TotalControl_Curve.StretchMagnification'), e=1, keyable=True)
condition = cmds.shadingNode('condition', asUtility=1)
cmds.connectAttr((multiplyDivide+'.outputX'), (condition+'.colorIfFalseR'), f=1)
cmds.connectAttr((Prefix + 'TotalControl_Curve.stretch'), (condition+'.firstTerm'), f=1)
cmds.setAttr((condition+'.colorIfTrueR'), 1)
multiplyDivideStretch = cmds.shadingNode('multiplyDivide', asUtility=1)
cmds.connectAttr((condition + '.outColorR'), (multiplyDivideStretch+'.input1X'), f=1)
cmds.connectAttr((Prefix + 'TotalControl_Curve.StretchMagnification'), (multiplyDivideStretch+'.input2X'), f=1)
for i in range(0,len(Joint)):
    cmds.connectAttr((multiplyDivideStretch + '.outputX'), (Joint[i] + '.scaleX'), f=1)
    cmds.connectAttr((multiplyDivideStretch+'.outputX'), (Joint[i]+'SkinJoint.scaleX'), f=1)
cmds.setAttr(CopyCurve[0]+'.inheritsTransform',1)
########################################################################################################################
#添加收缩
cmds.addAttr((Prefix + 'TotalControl_Curve'), ln='Contract', dv=0, at='double')
cmds.setAttr((Prefix + 'TotalControl_Curve.Contract'), e=1, keyable=True)
multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
cmds.setAttr((multiplyDivide+'.input2X'), 0.01)
cmds.connectAttr((Prefix + 'TotalControl_Curve.Contract'), (multiplyDivide+'.input1X'), f=1)
cmds.connectAttr((multiplyDivide+'.outputX'), (IK[0]+'.offset'), f=1)
#修正方案
cmds.addAttr((Prefix + 'TotalControl_Curve'), ln='Contract', dv=0,max=100,min=-100, at='double')
cmds.setAttr((Prefix + 'TotalControl_Curve.Contract'), e=1, keyable=True)
multiplyDivide = cmds.shadingNode('multiplyDivide', asUtility=1)
cmds.setAttr((multiplyDivide + '.input2X'),0.01)
cmds.connectAttr((Prefix + 'TotalControl_Curve.Contract'), (multiplyDivide + '.input1X'), f=1)
for i in range(0,len(Joint)):
    plusMinusAverage = cmds.shadingNode('plusMinusAverage', asUtility=1)
    cmds.connectAttr((multiplyDivide+'.outputX'), (plusMinusAverage + '.input1D[0]'), f=1)
    cmds.setAttr((plusMinusAverage + '.input1D[1]'),cmds.getAttr(Joint[i]+'_follicleShape.parameterU'))
    cmds.connectAttr((plusMinusAverage + '.output1D'), (Joint[i]+'_follicleShape.parameterU'), f=1)
########################################################################################################################
#添加FK
FK_List = []
for i in range(0,len(CurvePoint)):
    FK_List.append(i)
for i in range(0, len(CurvePoint)-1):
    FK_List.append(len(CurvePoint)-i-2)
FKCurve = []
print FK_List
j=0
All_TopGrp = []
for i in FK_List:
    FKCurve = cmds.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=2, tol=0.01, nr=(0, 1, 0),
                          n=(Prefix + 'FKController'+ str(j)))
    if j >= (len(CurvePoint)):
        Shape = cmds.listRelatives(FKCurve[0], s=1)
        cmds.select((Shape[0] + ".cv[0:]"))
        cmds.scale(0.8,0.8,0.8, r=1)
    cmds.select(FKCurve)
    cmds.group(n=(Prefix + 'FKController_Grp2_'+ str(j)))
    TopGrp = cmds.group(n=(Prefix + 'FKController_Grp1_'+ str(j)))
    All_TopGrp.append(TopGrp)
    cmds.delete(cmds.parentConstraint((Prefix + str(FK_List[j]) + '_BaseController'), TopGrp, w=1))
    if j > 0:
        cmds.parent((Prefix + 'FKController_Grp1_' + str(j)),
                    (Prefix + 'FKController' + str(j-1)))
    if j > (len(CurvePoint)-2):
        cmds.parentConstraint((Prefix + 'FKController' + str(j)),
                    (Prefix + str(FK_List[j]) + '_BaseController_Grp1'),w=1)
    j = j + 1
j=0
All_Loc = []
for i in FK_List:
    if j < (len(CurvePoint)-1):
        cmds.spaceLocator(p=(0, 0, 0), n=(Prefix + 'Loc' + str(j)))
        cmds.setAttr((Prefix + 'Loc' + str(j) + '.v'),0)
        Loc = cmds.ls(sl=1)
        All_Loc.append(Loc)
        cmds.parent(Loc, (Prefix + 'FKController_Grp1_' + str(len(CurvePoint)-1)))
        cmds.delete(cmds.parentConstraint((Prefix + 'FKController_Grp1_' + str(j), Loc[0]), w=1))
        cmds.connectAttr((Loc[0] + '.translate'),(Prefix + 'FKController_Grp1_'+ str(len(FK_List)-1-j)+ '.translate'), f=1)
        cmds.connectAttr((Loc[0] + '.rotate'),(Prefix + 'FKController_Grp1_'+ str(len(FK_List)-1-j)+ '.rotate'), f=1)
        if cmds.objExists((Prefix + 'Loc' + str(j-1))):
            cmds.parent((Prefix + 'Loc' + str(j-1)),(Prefix + 'Loc' + str(j)))
        cmds.parentConstraint((Prefix + 'FKController' + str(j)), All_Loc[j], w=1)
    j = j + 1
cmds.parent((Prefix + 'FKController_Grp1_0'),(Prefix+'All_Grp'))
cmds.parentConstraint((Prefix + 'TotalControl_Curve'),(Prefix + 'FKController_Grp1_0'),mo=1,w=1)
cmds.scaleConstraint((Prefix + 'TotalControl_Curve'),(Prefix + 'FKController_Grp1_0'),mo=1)

########################################################################################################################
#添加拖拽
Drag_Curve = cmds.curve(p=[(-12, 0, 0), (-11, 0, 0), (11, 0, 0), (12, 0, 0)], k=[0, 0, 0, 1, 1, 1], d=3)
cmds.select(Drag_Curve+'.cv[0:]')
Drag_CurvePoint = cmds.ls(sl=1,fl=1)
#创建基础控制器
i = 0
for Point in Drag_CurvePoint [0:4]:
    cmds.select(Point)
    Cluster = cmds.mel.newCluster(" -envelope 1")
    cmds.setAttr((Cluster[1] + '.v'), 0)
    DragCurve = cmds.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=5, tol=0.01, nr=(0, 1, 0),
                n=(Prefix + str(i) + '_DragController'))
    cmds.group(n=(Prefix + str(i) + '_DragController_Grp2'))
    TopGrp = cmds.group(n=(Prefix + str(i) + '_DragController_Grp1'))
    if i<2:
        cmds.delete(cmds.parentConstraint((Prefix + '0_BaseController'),TopGrp,w=1))
    else:
        cmds.delete(cmds.parentConstraint((Prefix + str(len(CurvePoint)-1) + '_BaseController'), TopGrp, w=1))
    cmds.delete(Cluster)
    #cmds.parent(TopGrp,All_BaseController_Grp)
    i = i + 1
#创建曲面
cmds.extrude(Drag_Curve, upn=0, dl=1, ch=0, rotation=0, d=(0, 0, 1), length=1, scale=1, et=0, rn=True, po=0)
Surface = cmds.ls(sl=1)
cmds.move(0, 0, -0.5, r=1, os=1, wd=1)
cmds.mel.channelBoxCommand('-freezeTranslate')
#创建控制曲面的蔟
for i in range(0,len(Drag_CurvePoint)):
    cmds.select(Surface[0]+'.cv['+ str(i) + '][0:*]')
    Cluster = cmds.mel.newCluster(" -envelope 1")
    cmds.setAttr((Cluster[1] + '.v'), 0)
    cmds.parent(Cluster[1], (Prefix + str(i) + '_DragController'))
#创建毛囊附着表面
All_DragFollicle_Grp = cmds.group(em=1,n=(Prefix+'All_DragFollicle_Grp'))
All_DragLoc_Grp = cmds.group(em=1,n=(Prefix+'All_DragLoc_Grp'))
shape = cmds.listRelatives(Surface,s=1)
for i in range(0,len(CurvePoint)):
    cpom = cmds.createNode('closestPointOnSurface')
    cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)
    decomposeMatrix = cmds.shadingNode('decomposeMatrix', asUtility=1)
    cmds.connectAttr((Prefix + str(i) + '_BaseController.worldMatrix[0]'), (decomposeMatrix + '.inputMatrix'), force=1)
    cmds.connectAttr((decomposeMatrix + '.outputTranslate'), (cpom + '.inPosition'), force=1)
    follicleShape = cmds.createNode('follicle', n=(Prefix + str(i) + '_BaseController_Grp1' + '_follicleShape'))
    follicle = cmds.listRelatives(follicleShape,p=1)
    cmds.connectAttr((shape[0] + '.worldSpace[0]'), (Prefix + str(i) + '_BaseController_Grp1_follicleShape.inputSurface'), f=1)
    cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (Prefix + str(i) + '_BaseController_Grp1_follicleShape.inputWorldMatrix'), f=1)
    cmds.connectAttr((Prefix + str(i) + '_BaseController_Grp1_follicleShape.outTranslate'), (Prefix + str(i) + '_BaseController_Grp1_follicle.translate'), f=1)
    cmds.connectAttr((Prefix + str(i) + '_BaseController_Grp1_follicleShape.outRotate'), (Prefix + str(i) + '_BaseController_Grp1_follicle.rotate'), f=1)
    cmds.setAttr((Prefix + str(i) + '_BaseController_Grp1_follicle.parameterU'),cmds.getAttr((cpom + '.parameterU')))
    cmds.setAttr((Prefix + str(i) + '_BaseController_Grp1_follicle.parameterV'), cmds.getAttr((cpom + '.parameterV')))
    cmds.select(cl=1)
    cmds.parent(follicle[0],All_DragFollicle_Grp)
    cmds.spaceLocator(p=(0, 0, 0), n=(Prefix + 'DragLoc' + str(i)))
    cmds.parent((Prefix + 'DragLoc' + str(i)),(Prefix+'All_DragLoc_Grp'))
    cmds.delete(cmds.parentConstraint((Prefix + 'FKController' + str(i)), (Prefix + 'DragLoc' + str(i)), w=1))
    cmds.parentConstraint(follicle[0], (Prefix + 'DragLoc' + str(i)), mo=1,w=1)
    cmds.delete(cpom,decomposeMatrix)
for i in range(0,len(CurvePoint)-1):
    cmds.parent((Prefix + 'DragLoc' + str(i+1)),(Prefix + 'DragLoc' + str(i)))
for i in range(0, len(CurvePoint)):
    cmds.connectAttr((Prefix + 'DragLoc' + str(i) + '.translate'),
                     (Prefix + 'FKController_Grp1_' + str(i) + '.translate'), f=1)
    cmds.connectAttr((Prefix + 'DragLoc' + str(i) + '.rotate'),
                     (Prefix + 'FKController_Grp1_' + str(i) + '.rotate'), f=1)
#整理文件
cmds.delete(Drag_Curve)
cmds.parent((Prefix + '1_DragController_Grp1'),(Prefix + '0_DragController'))
cmds.parent((Prefix + '2_DragController_Grp1'),(Prefix + '3_DragController'))
cmds.group(Surface,All_DragFollicle_Grp,All_DragLoc_Grp,n=(Prefix+'All_DragFollicleAttachment_Grp'))
cmds.group((Prefix+'All_DragFollicleAttachment_Grp'),(Prefix + '0_DragController_Grp1'),(Prefix + '3_DragController_Grp1'),
           n=(Prefix+'All_Drag_Grp'))
cmds.parent((Prefix+'All_Drag_Grp'),(Prefix+'All_Grp'))
cmds.setAttr((Prefix + 'All_DragFollicleAttachment_Grp.inheritsTransform'),0)
cmds.setAttr((Prefix + 'All_DragFollicleAttachment_Grp.v'),0)
cmds.parentConstraint((Prefix + 'TotalControl_Curve'),(Prefix+'All_Drag_Grp'),mo=1,w=1)
cmds.scaleConstraint((Prefix + 'TotalControl_Curve'),(Prefix+'All_Drag_Grp'),mo=1)












