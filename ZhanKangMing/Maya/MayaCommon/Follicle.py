#coding=gbk
import pymel.core as pm
class ZKM_FollicleClass:
    # 毛囊约束
    def ZKM_FollicleConstraint(self,MD,Sel,Keep):
        pm.select(cl=1)
        if not pm.objExists('AllFollicle_Grp'):
            pm.group(n='AllFollicle_Grp')
        shape = pm.listRelatives(MD,s=1)
        TypeMesh = pm.ls(shape[0],type='mesh')
        if TypeMesh:
            pm.createNode('closestPointOnMesh', n=("cpom"))
            pm.connectAttr((shape[0] + '.outMesh'), ('cpom' + '.inMesh'), f=1)
        TypeNurbs = pm.ls(shape[0], type='nurbsSurface')
        if TypeNurbs:
            pm.createNode('closestPointOnSurface', n=("cpom"))
            pm.connectAttr((shape[0] + '.worldSpace[0]'), ('cpom' + '.inputSurface'), f=1)
        pm.spaceLocator(p=(0, 0, 0), n=("Loc"))
        for i in range(0, len(Sel)):
            pm.delete(pm.pointConstraint(Sel[i], "Loc", weight=1, offset=(0, 0, 0)))
            pos = pm.xform(("Loc"), q=1, a=1, ws=1, t=1)
            pm.setAttr(("cpom" + ".inPositionX"), pos[0])
            pm.setAttr(("cpom" + ".inPositionY"), pos[1])
            pm.setAttr(("cpom" + ".inPositionZ"), pos[2])
            u = float(pm.getAttr("cpom" + ".parameterU"))
            v = float(pm.getAttr("cpom" + ".parameterV"))
            pm.createNode('follicle', n=(Sel[i] + "_follicleShape"))
            if TypeMesh:
                pm.connectAttr((MD + "Shape" + ".outMesh"), (Sel[i] + "_follicleShape" + ".inputMesh"), f=1)
                pm.connectAttr((MD + "Shape" + ".worldMatrix[0]"), (Sel[i] + "_follicleShape" + ".inputWorldMatrix"),f=1)
            if TypeNurbs:
                pm.connectAttr((shape[0] + '.worldSpace[0]'), (Sel[i] + '_follicleShape' + '.inputSurface'), f=1)
                pm.connectAttr((shape[0] + '.worldMatrix[0]'), (Sel[i] + '_follicleShape' + '.inputWorldMatrix'),f=1)
            pm.connectAttr((Sel[i] + "_follicleShape" + ".outTranslate"), (Sel[i] + "_follicle" + ".translate"), f=1)
            pm.connectAttr((Sel[i] + "_follicleShape" + ".outRotate"), (Sel[i] + "_follicle" + ".rotate"), f=1)
            pm.setAttr((Sel[i] + "_follicleShape" + ".parameterU"), u)
            pm.setAttr((Sel[i] + "_follicleShape" + ".parameterV"), v)
            if Keep == 'True':
                if not i == 'FaceLoc_head_loc_M':
                    pm.parentConstraint((Sel[i] + "_follicle"), Sel[i], mo=1, weight=1)
            else:
                pm.parentConstraint((Sel[i] + "_follicle"), Sel[i], weight=1)
            if pm.objExists('AllFollicle_Grp'):
                pm.parent((Sel[i] + "_follicle"), 'AllFollicle_Grp')
        pm.delete("Loc")
        pm.delete("cpom")
        # ZKM_FollicleClass().ZKM_FollicleConstraint('bace_bs_Mesh',['nurbsCircle1','nurbsCircle2'],'Ture')
