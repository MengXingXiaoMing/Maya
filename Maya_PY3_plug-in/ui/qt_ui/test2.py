#coding=gbk
import importlib

import maya.cmds as cmds
import maya.mel as mel
# 获取文件路径
import os
import sys
import inspect
import webbrowser
# 文件路径
file_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1]))
# 根路径
root_path = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))
# 版本号
maya_version = cmds.about(version=True)
# 库路径
library_path = root_path + '\\' + maya_version

# 库添加到系统路径
sys.path.append(library_path)


sel_f = cmds.ls(sl=1,fl=1)
for f in sel_f:
    mesh = sel_f[0].split('.')[0]
    cmds.select(mesh)
    mesh = cmds.ls(sl=1)
    copy_mesh = cmds.duplicate(mesh)

    cmds.setAttr(mesh[0]+'.rotatePivot', 0,0,0)
    cmds.setAttr(mesh[0]+'.scalePivot', 0,0,0)
    cmds.select(mesh[0]+'.f[*]')
    cmds.scale(1e-05, 0, 0, r=1, ws=1)

    blendShape = cmds.blendShape(copy_mesh, mesh)

    cmds.setAttr(blendShape[0]+'.'+copy_mesh[0], 1)
    cmds.symmetricModelling(f, e=1, ts=True)
    cmds.select(f)
    cmds.blendShape(blendShape[0]+'.'+copy_mesh[0], ss=0, md=1, sa="x", e=1, mt=(0, 0))
    cmds.select(mesh)
    cmds.DeleteHistory()
    cmds.delete(copy_mesh)
    cmds.symmetricModelling(s=0)

import pymel as pm
sel_f = cmds.ls(sl=1,fl=1)
mesh = [sel_f[0].split('.')[0]]
point = cmds.ls(mesh[0]+'.vtx[*]',fl=1)
r_point = []
for p in point:
    pos = cmds.xform(p, q=1, ws=1, t=1)
    if pos[0] < 0.001:
        r_point.append(p)
str_r_point = str(r_point)[1:-2]
new_s = str_r_point.replace("'", "\"")
for f in sel_f:
    cmds.select(f)
    common = ('activateTopoSymmetry("'+f+'", {'+new_s+'"}, {"'+mesh[0]+'"}, "facet", "dR_symmetrize", 1);')
    mel.eval(common)
cmds.select(cl=1)


# 获取Maya的完整版本信息
full_version_string = cmds.about(iv=True)

# 打印完整版本信息
print("Maya的完整版本信息:", full_version_string[14:])




cone = cmds.cone(esw=360, ch=0, d=3, hr=2, ut=0, ssw=0, p=(0, -1, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))
# print(cone)
cmds.rebuildSurface("nurbsCone1", rt=0, kc=0, fr=0, ch=0, end=1, sv=4, su=4, kr=0, dir=2, kcp=1, tol=0.01, dv=3, du=3, rpo=1)
cmds.setAttr(cone[0]+'.scaleX', 10)
cmds.setAttr(cone[0]+'.scaleY', 10)
cmds.setAttr(cone[0]+'.scaleZ', 10)
# cmds.makeIdentity(cone,n=0, s=1, r=1, t=1, apply=True, pn=1)
cluster = cmds.cluster(cone)
# print(cluster)
cmds.setAttr(cluster[1]+'.rotatePivot', 0, 0, 0)
cmds.setAttr(cluster[1]+'.scalePivot', 0, 0, 0)
sphere = cmds.sphere(esw=360, ch=0, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))
# print(sphere)
new_surface = cmds.nurbsBoolean('nurbsCone1', 'nurbsSphere1', ch=1, nsf=1, op=2)
cmds.setAttr(new_surface[0]+'.template', 1)
# print(new_surface)
grp_1 = cmds.group(sphere,cluster)
cmds.setAttr(grp_1 + '.visibility', 0)
grp_2 = cmds.group(cone,grp_1)

ls_loc = cmds.spaceLocator(p=(0, 0, 0))
cmds.setAttr(ls_loc[0]+'.translateX', -10)
cmds.setAttr(ls_loc[0]+'.translateY', -20)

shape = cmds.listRelatives(cone, s=1)
TypeNurbs = cmds.ls(shape[0], type='nurbsSurface')
cpom = cmds.createNode('closestPointOnSurface')
cmds.connectAttr((shape[0] + '.worldSpace[0]'), (cpom + '.inputSurface'), f=1)

pos = cmds.xform(ls_loc[0], q=1, a=1, ws=1, t=1)
cmds.setAttr((cpom + '.inPositionX'), pos[0])
cmds.setAttr((cpom + '.inPositionY'), pos[1])
cmds.setAttr((cpom + '.inPositionZ'), pos[2])
u = float(cmds.getAttr(cpom + ".parameterU"))
v = float(cmds.getAttr(cpom + ".parameterV"))
follicleShape = (ls_loc[0] + '_follicleShape')
follicle = (ls_loc[0] + '_follicle')
cmds.createNode('follicle', n=(ls_loc[0] + "_follicleShape"))
shape = cmds.listRelatives(cone, s=1, type='nurbsSurface')
cmds.connectAttr((shape[0] + '.worldSpace[0]'), (follicleShape + '.inputSurface'), f=1)
cmds.connectAttr((shape[0] + '.worldMatrix[0]'), (follicleShape + '.inputWorldMatrix'),f=1)
cmds.connectAttr((follicleShape + ".outTranslate"), (follicle + ".translate"),f=1)
# cmds.connectAttr((follicleShape + ".outRotate"), (follicle + ".rotate"), f=1)
cmds.setAttr((follicleShape + ".parameterU"), u)
cmds.setAttr((follicleShape + ".parameterV"), v)

cmds.setAttr(follicle + '.visibility', 0)

cmds.delete(cpom)

cmds.delete(ls_loc)

ls_loc = cmds.spaceLocator(p=(0, 0, 0))
cmds.setAttr(ls_loc[0]+ '.translateY', -1)
cmds.setAttr(ls_loc[0]+ '.visibility', 0)

move_grp = cmds.group(em=1)
cmds.parent(ls_loc, new_surface[0], follicle, move_grp)
curve = cmds.curve(p=[(0.0, 0.0, 0.0), (1.3246660753366768e-16, -1.0151220316349963, 0.0), (0.0399518620411479, -1.0205214288941349, 0.0), (0.07719707184685853, -1.03594916120812, 0.0), (0.1092661723850182, -1.0603803444126723, 0.0), (0.13369754874488846, -1.0924495608444404, 0.0), (0.14912501063975567, -1.1296946933878147, 0.0), (0.15452572135840073, -1.169646602968543, 0.0), (0.0, -1.1696465940573089, 0.0), (1.3246660753366768e-16, -1.0151220316349963, 0.0), (-0.0399518620411479, -1.0205214288941349, 0.0), (-0.07719707184685853, -1.03594916120812, 0.0), (-0.1092661723850182, -1.0603803444126723, 0.0), (-0.13369754874488846, -1.0924495608444404, 0.0), (-0.14912501063975567, -1.1296946933878147, 0.0), (-0.15452572135840073, -1.169646602968543, 0.0), (-0.14912501063975567, -1.2095984560975157, 0.0), (-0.13369754874488846, -1.24684366590469, 0.0), (-0.1092661723850182, -1.2789127664433722, 0.0), (-0.07719707184685853, -1.3033441428048105, 0.0), (-0.0399518620411479, -1.3187716046981095, 0.0), (1.7031435161511713e-16, -1.3241723154157095, 0.0), (0.0399518620411479, -1.3187716046981095, 0.0), (0.07719707184685853, -1.3033441428048105, 0.0), (0.1092661723850182, -1.2789127664433722, 0.0), (0.13369754874488846, -1.24684366590469, 0.0), (0.14912501063975567, -1.2095984560975157, 0.0), (0.15452572135840073, -1.169646602968543, 0.0), (-0.15452572135840073, -1.169646602968543, 0.0), (0.0, -1.1696465940573089, 0.0), (1.7031435161511713e-16, -1.3241723154157095, 0.0)], k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0], d=1)
cmds.setAttr((curve + '.tx'), lock=1)
cmds.setAttr((curve + '.ty'), lock=1)
cmds.setAttr((curve + '.tz'), lock=1)
cmds.connectAttr((curve + '.scaleX'), (curve + '.scaleY'),f=1)
cmds.connectAttr((curve + '.scaleX'), (curve + '.scaleZ'),f=1)
cmds.addAttr(curve, ln='range', min=-10, max=10, dv=1, at='double')
cmds.setAttr((curve + '.range'), e=1, keyable=True)
cmds.connectAttr((curve + '.range'), (cluster[1] + '.scaleY'),f=1)
cmds.addAttr(curve, ln='num', dv=1, at='double')
cmds.setAttr((curve + '.num'), e=1, keyable=True)
grp_3 = cmds.group(em=1)
cmds.parent(curve, grp_3)
cmds.parent(grp_3, grp_2)
cmds.parent(move_grp, curve)

vectorProduct = cmds.createNode('vectorProduct')
cmds.setAttr(vectorProduct + '.input1Y', -1)
cmds.connectAttr((follicle + '.translate'), (vectorProduct + '.input2'),f=1)
cmds.setAttr(vectorProduct + '.normalizeOutput', 1)

vectorProduct_2 = cmds.createNode('vectorProduct')
cmds.setAttr(vectorProduct_2 + '.input1Y', -1)
cmds.connectAttr((ls_loc[0] + '.translate'), (vectorProduct_2 + '.input2'),f=1)
cmds.setAttr(vectorProduct_2 + '.normalizeOutput', 1)

setRange = cmds.createNode('setRange')
cmds.setAttr(setRange + '.maxX', 1)
cmds.setAttr(setRange + '.oldMaxX', 1)
cmds.connectAttr((vectorProduct + '.outputX'), (setRange + '.oldMinX'),f=1)
cmds.connectAttr((vectorProduct_2 + '.outputX'), (setRange + '.valueX'),f=1)

cmds.connectAttr((setRange + '.outValueX'), (curve + '.num'),f=1)











num = 1
cone = cmds.cone(n=('dot_cone_'+str(num)), esw=360, ch=0, d=3, hr=2, ut=0, ssw=0, p=(0, -1, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))
# print(cone)
cmds.rebuildSurface(cone, rt=0, kc=0, fr=0, ch=0, end=1, sv=4, su=4, kr=0, dir=2, kcp=1, tol=0.01, dv=3,
                    du=3, rpo=1)
cmds.setAttr(cone[0] + '.scaleX', 10)
cmds.setAttr(cone[0] + '.scaleY', 10)
cmds.setAttr(cone[0] + '.scaleZ', 10)
# cmds.makeIdentity(cone,n=0, s=1, r=1, t=1, apply=True, pn=1)
cluster = cmds.cluster(cone)
# print(cluster)
cmds.setAttr(cluster[1] + '.rotatePivot', 0, 0, 0)
cmds.setAttr(cluster[1] + '.scalePivot', 0, 0, 0)
sphere = cmds.sphere(n=('dot_sphere_'+str(num)), esw=360, ch=0, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))
# print(sphere)
new_surface = cmds.nurbsBoolean(cone, sphere, ch=1, nsf=1, op=2, n='dot_drver_cluster'+str(num))
print(new_surface)
sphere_shape = cmds.listRelatives(new_surface[0], c=1)
# new_surface = cmds.nurbsBoolean( 'dot_drver_cluster0Shape_2','nurbsCone1', ch=1, nsf=1, op=1)
cmds.setAttr(new_surface[0] + '.template', 1)
# 开始创建内圆
cone_inside = cmds.cone(n=('dot_cone_inside_' + str(num)), esw=360, ch=0, d=3, hr=2, ut=0, ssw=0, p=(0, -1, 0), s=8, r=1,tol=0.01, nsp=1, ax=(0, 1, 0))
cmds.rebuildSurface(cone_inside, rt=0, kc=0, fr=0, ch=0, end=1, sv=4, su=4, kr=0, dir=2, kcp=1, tol=0.01, dv=3,du=3, rpo=1)
cmds.setAttr(cone_inside[0] + '.scaleY', 10)
cluster_inside = cmds.cluster(cone_inside)
cmds.setAttr(cluster_inside[1] + '.rotatePivot', 0, 0, 0)
cmds.setAttr(cluster_inside[1] + '.scalePivot', 0, 0, 0)
new_surface_2 = cmds.nurbsBoolean(new_surface[0], cone_inside, ch=1, nsf=1, op=1)
cmds.setAttr(new_surface_2[0]+ '.inheritsTransform', 0)


cmds.nurbsBoolean('dot_drver_cluster0Shape', 'dot_cone_inside_0', ch=1, nsf=1, op=1)










num = 0

curve = cmds.curve(n='dot_drver'+str(num),p=[(0, -2, 0), (0, 0, 0), (0, -2, 0)], k=[0, 1, 2], d=1)

all_cluster_grp = []
all_loc = []
for i in [0, 2]:
    cluster = cmds.cluster(curve + '.cv[' + str(i) + ']')
    grp = cmds.group(cluster,n=cluster[0] + '_grp')
    all_cluster_grp.append(grp)
    cmds.setAttr(grp + '.rotatePivot', 0, 0, 0)
    cmds.setAttr(grp + '.scalePivot', 0, 0, 0)
    loc = cmds.spaceLocator(n=cluster[1] + '_t_loc', p=(0, 0, 0))[0]
    cmds.setAttr(loc + '.ty', -2)
    all_loc.append(loc)
    cmds.pointConstraint(cluster[1], loc, offset=(0, 0, 0), weight=1)
    if i == 0:
        cmds.setAttr(grp + '.rz', 30)
    else:
        cmds.setAttr(grp + '.rz', 10)

cone = cmds.revolve(curve, esw=360, ch=1, ulp=1, degree=3, ut=0, ssw=0, s=8, tol=0.01, ax=(0, 1, 0), rn=0, po=0)

sphere = cmds.sphere(n=('dot_sphere_' + str(num)), esw=360, ch=0, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1,
                     tol=0.01, nsp=4, ax=(0, 1, 0))

new_surface = cmds.nurbsBoolean(cone[0], sphere, ch=1, nsf=1, op=2, n='dot_drver_cluster' + str(num))

cmds.setAttr(new_surface[0] + '.template', 1)
# 建立数值定位器
ls_loc = cmds.spaceLocator(p=(0, 0, 0), n=('dot_' + str(num) + '_loc0'))
num_curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)], d=1, n=(ls_loc[0] + '_num'))
cmds.setAttr(num_curve + ".overrideEnabled", 1)
cmds.setAttr(num_curve + ".overrideDisplayType", 2)
# cmds.setAttr((curve + '.sx'), 0.0001)
# cmds.setAttr((curve + '.sy'), 0.0001)
# cmds.setAttr((curve + '.sz'), 0.0001)
cmds.addAttr(ls_loc[0], ln='num', dv=1, at='double')
cmds.setAttr((ls_loc[0] + '.num'), e=1, keyable=True)
shape = cmds.listRelatives(num_curve, c=1, type='nurbsCurve')
paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
cmds.parent(num_curve, ls_loc)
cmds.connectAttr((ls_loc[0] + '.num'), (paramDimension + '.uParamValue'), f=1)
cmds.setAttr(ls_loc[0] + '.translateY', -1)

grp_1 = cmds.group(curve, all_cluster_grp, all_loc, cone, sphere, n='dot_count_' + str(num) + '_Grp')
cmds.setAttr(grp_1 + '.visibility', 0)
# 建立控制器
curve = cmds.curve(p=[(0.0, 0.0, 0.0), (1.3246660753366768e-16, -1.0151220316349963, 0.0),
                      (0.0399518620411479, -1.0205214288941349, 0.0),
                      (0.07719707184685853, -1.03594916120812, 0.0),
                      (0.1092661723850182, -1.0603803444126723, 0.0),
                      (0.13369754874488846, -1.0924495608444404, 0.0),
                      (0.14912501063975567, -1.1296946933878147, 0.0),
                      (0.15452572135840073, -1.169646602968543, 0.0), (0.0, -1.1696465940573089, 0.0),
                      (1.3246660753366768e-16, -1.0151220316349963, 0.0),
                      (-0.0399518620411479, -1.0205214288941349, 0.0),
                      (-0.07719707184685853, -1.03594916120812, 0.0),
                      (-0.1092661723850182, -1.0603803444126723, 0.0),
                      (-0.13369754874488846, -1.0924495608444404, 0.0),
                      (-0.14912501063975567, -1.1296946933878147, 0.0),
                      (-0.15452572135840073, -1.169646602968543, 0.0),
                      (-0.14912501063975567, -1.2095984560975157, 0.0),
                      (-0.13369754874488846, -1.24684366590469, 0.0),
                      (-0.1092661723850182, -1.2789127664433722, 0.0),
                      (-0.07719707184685853, -1.3033441428048105, 0.0),
                      (-0.0399518620411479, -1.3187716046981095, 0.0),
                      (1.7031435161511713e-16, -1.3241723154157095, 0.0),
                      (0.0399518620411479, -1.3187716046981095, 0.0),
                      (0.07719707184685853, -1.3033441428048105, 0.0),
                      (0.1092661723850182, -1.2789127664433722, 0.0),
                      (0.13369754874488846, -1.24684366590469, 0.0),
                      (0.14912501063975567, -1.2095984560975157, 0.0),
                      (0.15452572135840073, -1.169646602968543, 0.0),
                      (-0.15452572135840073, -1.169646602968543, 0.0), (0.0, -1.1696465940573089, 0.0),
                      (1.7031435161511713e-16, -1.3241723154157095, 0.0)],
                   k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0,
                      16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0],
                   d=1, n=('dot_curve_' + str(num)))
cmds.setAttr((curve + '.tx'), lock=1)
cmds.setAttr((curve + '.ty'), lock=1)
cmds.setAttr((curve + '.tz'), lock=1)
cmds.connectAttr((curve + '.scaleX'), (curve + '.scaleY'), f=1)
cmds.connectAttr((curve + '.scaleX'), (curve + '.scaleZ'), f=1)

cmds.addAttr(curve, ln='range', min=0.1, max=179.9, dv=30, at='double')
cmds.setAttr((curve + '.range'), e=1, keyable=True)
cmds.connectAttr((curve + '.range'), (all_cluster_grp[0] + '.rotateZ'), f=1)

cmds.addAttr(curve, ln='inside_range', min=0.1, max=179.9, dv=0.1, at='double')
cmds.setAttr((curve + '.inside_range'), e=1, keyable=True)
cmds.connectAttr((curve + '.inside_range'), (all_cluster_grp[1] + '.rotateZ'), f=1)

cmds.addAttr(curve, ln='num', dv=1, at='double')
cmds.setAttr((curve + '.num'), e=1, keyable=True)
cmds.connectAttr((curve + '.num'), (ls_loc[0] + '.num'), f=1)

cmds.parent(new_surface[0], ls_loc[0], curve)

grp_2 = cmds.group(em=1, n=(curve + '_grp'))
cmds.parent(curve, grp_2)
grp_3 = cmds.group(grp_1, grp_2, n='dot_drver_keep_grp' + str(num))

vectorProduct_2 = cmds.createNode('vectorProduct')
cmds.setAttr(vectorProduct_2 + '.input1Y', -1)

cmds.connectAttr((ls_loc[0] + '.translate'), (vectorProduct_2 + '.input2'), f=1)
cmds.setAttr(vectorProduct_2 + '.normalizeOutput', 1)

setRange = cmds.createNode('setRange')
cmds.setAttr(setRange + '.maxX', 1)
cmds.setAttr(setRange + '.oldMaxX', 1)

all_vectorProduct = []
for fo in all_loc:
    vectorProduct = cmds.createNode('vectorProduct')
    cmds.setAttr(vectorProduct + '.input1Y', -1)
    cmds.connectAttr((fo + '.translate'), (vectorProduct + '.input2'), f=1)
    cmds.setAttr(vectorProduct + '.normalizeOutput', 1)
    all_vectorProduct.append(vectorProduct)
cmds.connectAttr((all_vectorProduct[0] + '.outputX'), (setRange + '.oldMinX'), f=1)
cmds.connectAttr((all_vectorProduct[1] + '.outputX'), (setRange + '.oldMaxX'), f=1)

cmds.connectAttr((vectorProduct_2 + '.outputX'), (setRange + '.valueX'), f=1)

cmds.connectAttr((setRange + '.outValueX'), (curve + '.num'), f=1)














sel = cmds.ls(sl=1)
top_num = sel[0][10:]
# print(top_num)
all_loc = cmds.ls('dot_' + top_num + '_loc*')
# print(all_loc)
new_loc = []
for loc in all_loc:
    child = cmds.listRelatives(loc, c=1, type='locator')
    if child:
        new_loc.append(loc)
# print(new_loc)
# print(new_loc[0][8+len(top_num):])
num = 0
if new_loc:
    all_loc_num = []
    for loc in new_loc:
        num = int(loc[8 + len(top_num):])
        all_loc_num.append(num)
    # 求最大值
    max_num = max(all_loc_num)
    num = max_num + 1
print(num)


cmds.addAttr(sel[0], ln='num' + str(num), dv=1, at='double')
cmds.setAttr((sel[0] + '.num' + str(num)), e=1, keyable=True)

ls_loc = cmds.spaceLocator(p=(0, 0, 0), n=('dot_' + top_num + '_loc' + str(num)))
curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)], d=1, n=(ls_loc[0] + '_num'))
cmds.setAttr(curve + '.overrideEnabled', 1)
cmds.setAttr(curve + '.overrideDisplayType', 2)
cmds.addAttr(ls_loc[0], ln='num', dv=1, at='double')
cmds.setAttr((ls_loc[0] + '.num'), e=1, keyable=True)
shape = cmds.listRelatives(curve, c=1, type='nurbsCurve')
paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
cmds.parent(curve, ls_loc)
cmds.connectAttr((ls_loc[0] + '.num'), (paramDimension + '.uParamValue'), f=1)

cmds.parent(ls_loc, sel)


all_range_loc = [('dot_drver' + top_num + '_t_loc0'),('dot_drver' + top_num + '_t_loc2')]
vectorProduct_1 = cmds.listConnections(all_range_loc[0], d=1, s=1,type='vectorProduct')
vectorProduct_2 = cmds.listConnections(all_range_loc[1], d=1, s=1,type='vectorProduct')

vectorProduct_3 = cmds.createNode('vectorProduct')
cmds.setAttr(vectorProduct_3 + '.input1Y', -1)
cmds.connectAttr((ls_loc[0] + '.translate'), (vectorProduct_3 + '.input2'), f=1)
cmds.setAttr(vectorProduct_3 + '.normalizeOutput', 1)


setRange = cmds.createNode('setRange')
cmds.setAttr(setRange + '.maxX', 1)
cmds.connectAttr((vectorProduct_1[0] + '.outputX'), (setRange + '.oldMinX'), f=1)
cmds.connectAttr((vectorProduct_2[0] + '.outputX'), (setRange + '.oldMaxX'), f=1)
cmds.connectAttr((vectorProduct_3 + '.outputX'), (setRange + '.valueX'), f=1)
print(vectorProduct)

cmds.connectAttr((setRange + '.outValueX'), (sel[0] + '.num' + str(num)), f=1)
cmds.connectAttr((sel[0] + '.num' + str(num)), (ls_loc[0] + '.num'), f=1)




sel = cmds.ls(sl=1)
all_range_grp = cmds.ls('distance_drver*_curve')
num = 0
all_num = []
grp = cmds.ls('dot_grp_*')
if grp:
    for g in grp:
        num = int(g[8:])
        all_num.append(num)
    # 求最大值
    max_num = max(all_num)
    num = max_num + 1
print(sel)
print(all_range_grp)
if not sel or (not sel[0] in all_range_grp):
    print(num)
    loc_num = 0
    # 创建距离显示曲面
    sphere_1 = cmds.sphere(n=('dot_sphere1_' + str(num)), esw=360, ch=1, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1,
                         tol=0.01, nsp=4, ax=(0, 1, 0))
    cmds.setAttr(sphere_1[0] + '.template', 1)
    sphere_2 = cmds.sphere(n=('dot_sphere2_' + str(num)), esw=360, ch=1, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1,
                         tol=0.01, nsp=4, ax=(0, 1, 0))
    cmds.setAttr(sphere_2[0] + '.template', 1)
    curve = cmds.curve(n=('distance_drver' + str(num) + '_curve'), p=[(-3.7551395312306146e-17, 1.1053200580606237, -7.566895313483482e-16), (0.5526600290326463, 0.9572348032834932, -7.566895313483482e-16), (0.9572348032834932, 0.5526600290326463, -7.566895313483482e-16), (1.1053200580606237, -1.7471036244928595e-16, -7.566895313483482e-16), (0.9572348032834932, -0.5526600290326463, -7.566895313483482e-16), (0.5526600290326463, -0.9572348032834932, -7.566895313483482e-16), (-3.7551395312306146e-17, -1.1053200580606237, -7.566895313483482e-16), (-0.5526600290326463, -0.9572348032834932, -7.566895313483482e-16), (-0.9572348032834932, -0.5526600290326463, -7.566895313483482e-16), (-1.1053200580606237, -1.7471036244928595e-16, -7.566895313483482e-16), (-0.9572348032834932, 0.5526600290326463, -7.566895313483482e-16), (-0.5526600290326463, 0.9572348032834932, -7.566895313483482e-16), (-3.7551395312306146e-17, 1.1053200580606237, -7.566895313483482e-16), (-3.7551395312306146e-17, 0.7815795502970119, 0.7815795502970119), (-3.7551395312306146e-17, -1.7471036244928595e-16, 1.1053200580606237), (-3.7551395312306146e-17, -0.7815795502970119, 0.7815795502970119), (-3.7551395312306146e-17, -1.1053200580606237, -7.566895313483482e-16), (-3.7551395312306146e-17, -0.7815795502970119, -0.7815795502970119), (-3.7551395312306146e-17, -1.7471036244928595e-16, -1.1053200580606237), (0.5526600290326463, -1.7471036244928595e-16, -0.9572348032834932), (0.9572348032834932, -1.7471036244928595e-16, -0.5526600290326463), (1.1053200580606237, -1.7471036244928595e-16, -7.566895313483482e-16), (0.9572348032834932, -1.7471036244928595e-16, 0.5526600290326463), (0.5526600290326463, -1.7471036244928595e-16, 0.9572348032834932), (-3.7551395312306146e-17, -1.7471036244928595e-16, 1.1053200580606237), (-0.5526600290326463, -1.7471036244928595e-16, 0.9572348032834932), (-0.9572348032834932, -1.7471036244928595e-16, 0.5526600290326463), (-1.1053200580606237, -1.7471036244928595e-16, -7.566895313483482e-16), (-0.9572348032834932, -1.7471036244928595e-16, -0.5526600290326463), (-0.5526600290326463, -1.7471036244928595e-16, -0.9572348032834932), (-3.7551395312306146e-17, -1.7471036244928595e-16, -1.1053200580606237), (-3.7551395312306146e-17, 0.7815795502970119, -0.7815795502970119), (-3.7551395312306146e-17, 1.1053200580606237, -7.566895313483482e-16)], k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0], d=1)
    cmds.addAttr(curve, ln='range0', min=0, dv=0.01, at='double')
    cmds.setAttr((curve + '.range0'), e=1, keyable=True)
    cmds.addAttr(curve, ln='range1', min=0, dv=1, at='double')
    cmds.setAttr((curve + '.range1'), e=1, keyable=True)

    cmds.connectAttr((curve + '.range1'), (curve + '.scaleX'), f=1)
    cmds.connectAttr((curve + '.range1'), (curve + '.scaleY'), f=1)
    cmds.connectAttr((curve + '.range1'), (curve + '.scaleZ'), f=1)

    cmds.connectAttr((curve + '.range0'), (sphere_1[1] + '.radius'), f=1)
    cmds.connectAttr((curve + '.range1'), (sphere_2[1] + '.radius'), f=1)

else:
    print('else')
    loc_num = 0
    all_num = []
    all_range_loc_grp = cmds.ls('distance_drver'+str(num)+'_loc1_*',type='locator')
    for loc in all_range_loc_grp:
        n = int(loc[20+len(str(num)):-5])
        all_num.append(n)
    # 求最大值
    max_num = max(all_num)
    loc_num = max_num + 1
    # print(loc_num)
    curve = sel[0]
    print(loc_num)

setRange = cmds.createNode('setRange')
cmds.setAttr((setRange + '.minX'), 1)
cmds.connectAttr((curve + '.range0'), (setRange + '.oldMinX'), f=1)
cmds.connectAttr((curve + '.range1'), (setRange + '.oldMaxX'), f=1)
# 创建距离判断
loc_0 = cmds.spaceLocator(n='distance_drver' + str(num) + '_loc0_' + str(loc_num))[0]
cmds.setAttr((loc_0 + '.visibility'), 0)
loc_2 = cmds.spaceLocator(n='distance_drver' + str(num) + '_loc1_' + str(loc_num))[0]
distanceDimShape = cmds.createNode('distanceDimShape')
cmds.setAttr((distanceDimShape + '.visibility'), 0)
print(distanceDimShape)
cmds.connectAttr((loc_0 + '.worldPosition[0]'), (distanceDimShape + '.startPoint'), f=1)
cmds.connectAttr((loc_2 + '.worldPosition[0]'), (distanceDimShape + '.endPoint'), f=1)

cmds.connectAttr((distanceDimShape + '.distance'), (setRange + '.valueX'),f=1)

cmds.addAttr(curve, ln='num'+ str(loc_num), dv=0, at='double')
cmds.setAttr((curve + '.num'+ str(loc_num)), e=1, keyable=True)
cmds.addAttr(loc_2, ln='num', dv=0, at='double')
cmds.setAttr((loc_2 + '.num'), e=1, keyable=True)

cmds.connectAttr((setRange + '.outValueX'),(curve + '.num'+ str(loc_num)),f=1)
cmds.connectAttr((setRange + '.outValueX'),(loc_2 + '.num'),f=1)

# 添加数值显示
num_curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)], d=1, n=(loc_2 + '_num'))
cmds.setAttr(num_curve + ".overrideEnabled", 1)
cmds.setAttr(num_curve + ".overrideDisplayType", 2)
shape = cmds.listRelatives(num_curve, c=1, type='nurbsCurve')
paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
cmds.parent(num_curve, loc_2)
cmds.connectAttr((loc_2 + '.num'), (paramDimension + '.uParamValue'), f=1)

# 整理文件
cmds.parent(loc_0, curve)
if not sel or (not sel[0] in all_range_grp):
    grp_1 = cmds.group(sphere_1, sphere_2, distanceDimShape, curve, loc_2, n=('dot_grp_' + str(num)))
    cmds.parentConstraint(curve, sphere_1, mo=1, w=1)
    cmds.parentConstraint(curve, sphere_2, mo=1, w=1)
else:
    print('aaaaa')
    cmds.parent(distanceDimShape, loc_2, ('dot_grp_' + str(num)))
    pass







# 创建不规则形状驱动定位器
sel = cmds.ls(sl=1)
loc_0 = cmds.spaceLocator()[0]


loc_1 = cmds.spaceLocator()[0]
cmds.parent(loc_1, loc_0)
cmds.geometryConstraint(sel, loc_0, weight=1)
cmds.normalConstraint(sel, loc_0, worldUpType="vector", aimVector=(1, 0, 0), upVector=(0, 1, 0), weight=1, worldUpVector=(0, 1, 0))
loc_2 = cmds.spaceLocator()[0]
cmds.pointConstraint(loc_2, loc_0, weight=1)
cmds.pointConstraint(loc_2, loc_1, weight=1)
# 创建点积计算，判断是否在法线正方向
vectorProduct_1 = cmds.createNode('vectorProduct')
cmds.setAttr(vectorProduct_1 + '.input1X', 1)
cmds.connectAttr((loc_1 + '.translate'), (vectorProduct_1 + '.input2'), f=1)
cmds.setAttr(vectorProduct_1 + '.normalizeOutput', 1)

cmds.addAttr(sel[0], ln='range', min=0, dv=1, at='double')
cmds.setAttr((sel[0] + '.range'), e=1, keyable=True)

#创建距离计算
setRange = cmds.createNode('setRange')
cmds.setAttr((setRange + '.minX'), 1)
cmds.connectAttr((sel[0] + '.range'), (setRange + '.oldMaxX'), f=1)
# 创建距离判断
loc_3 = loc_0
cmds.setAttr((loc_3 + '.visibility'), 0)
loc_4 = loc_2
distanceDimShape = cmds.createNode('distanceDimShape')
cmds.setAttr((distanceDimShape + '.visibility'), 0)
print(distanceDimShape)
cmds.connectAttr((loc_3 + '.worldPosition[0]'), (distanceDimShape + '.startPoint'), f=1)
cmds.connectAttr((loc_4 + '.worldPosition[0]'), (distanceDimShape + '.endPoint'), f=1)

cmds.connectAttr((distanceDimShape + '.distance'), (setRange + '.valueX'), f=1)

cmds.addAttr(sel[0], ln='num', dv=0, at='double')
cmds.setAttr((sel[0] + '.num'), e=1, keyable=True)
cmds.addAttr(loc_4, ln='num', dv=0, at='double')
cmds.setAttr((loc_4 + '.num'), e=1, keyable=True)

# 创建点积判断
condition = cmds.createNode('condition')
cmds.setAttr((condition + '.operation'), 2)

cmds.connectAttr((vectorProduct_1 + '.outputX'), (condition + '.firstTerm'), f=1)
cmds.connectAttr((setRange + '.outValueX'), (condition + '.colorIfTrueR'), f=1)

cmds.connectAttr((condition + '.outColorR'), (sel[0] + '.num'), f=1)
cmds.connectAttr((condition + '.outColorR'), (loc_4 + '.num'), f=1)

# 添加数值显示
num_curve = cmds.curve(p=[(0.0, 0.0, 0.0), (0.0, 0.0001, 0.0)], d=1, n=(loc_4 + '_num'))
cmds.setAttr(num_curve + ".overrideEnabled", 1)
cmds.setAttr(num_curve + ".overrideDisplayType", 2)
shape = cmds.listRelatives(num_curve, c=1, type='nurbsCurve')
paramDimension = cmds.paramDimension(shape[0] + '.u[0]')
cmds.parent(num_curve, loc_4)
cmds.connectAttr((loc_4 + '.num'), (paramDimension + '.uParamValue'), f=1)



'''import numpy as np

# 示例点
points = np.array([
    [2.802, 5.215, -2.584],
    [2.998, 4.925, -2.524],
    [3.271, 4.925, -2.75],
    [3.456, 4.6, -2.725],
    [3.592, 4.248, -2.706]
])
# 2. 椭球拟合
# 使用最小二乘法拟合椭球方程。我们将椭球方程表示为一个二次形式，并通过最小化误差来拟合数据。
#
# python
# 复制代码
# from scipy.optimize import least_squares

def ellipsoid_fit(X):
    # 确定 X 的形状
    X = np.asarray(X)
    if X.shape[1] != 3:
        raise ValueError("输入点应为 (n, 3) 的数组")

    # 创建设计矩阵 D
    D = np.hstack((X[:, 0:1]**2, X[:, 1:2]**2, X[:, 2:3]**2, 2*X[:, 0:1]*X[:, 1:2],
                   2*X[:, 0:1]*X[:, 2:3], 2*X[:, 1:2]*X[:, 2:3], 2*X[:, 0:1],
                   2*X[:, 1:2], 2*X[:, 2:3], np.ones((X.shape[0], 1))))

    # 使用最小二乘法求解
    _, _, V = np.linalg.svd(D, full_matrices=False)
    p = V[-1, :]

    # 构建椭球参数
    A = np.array([[p[0], p[3], p[4], p[6]],
                  [p[3], p[1], p[5], p[7]],
                  [p[4], p[5], p[2], p[8]],
                  [p[6], p[7], p[8], p[9]]])

    # 提取椭球中心
    center = np.linalg.solve(-A[:3, :3], p[6:9])

    # 提取椭球半径
    R = A[:3, :3]
    _, D, Vt = np.linalg.svd(R)
    radii = np.sqrt(1 / np.abs(D))

    return center, radii

# 调用函数拟合椭球
center, radii = ellipsoid_fit(points)
# 3. 提取椭球参数
# 从拟合的椭球方程中提取椭球的中心和三轴长度。
#
# python
# 复制代码
print("椭球中心:", center)
print("椭球半径:", radii)'''