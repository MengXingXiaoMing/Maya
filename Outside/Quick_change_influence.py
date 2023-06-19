#coding=gbk
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds
import shiboken2
import maya.mel as mel
from PySide2 import QtWidgets
from PySide2 import QtGui
#获取鼠标在屏幕的位置
def getScenePos():
    view = omui.M3dView.active3dView()
    view_height = view.portHeight()
    QWidget_view = shiboken2.wrapInstance(long(view.widget()), QtWidgets.QWidget)
    global_pos = QtGui.QCursor.pos()
    local_pos = QWidget_view.mapFromGlobal(global_pos)
    return local_pos.x(),view_height - local_pos.y()
#通过鼠标光标获取FaceID
def getFaceIDbyMouseCursor(mesh_name):
    if cmds.objExists(mesh_name):
        scenes_pos = getScenePos()

        pos = om.MPoint()
        dir = om.MVector()

        # 射线求交命中点 声明
        hitpoint = om.MFloatPoint()
        # 视口空间 pos 转为 3d view pos

        omui.M3dView().active3dView().viewToWorld(int(scenes_pos[0]), int(scenes_pos[1]), pos, dir)

        pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)

        unit = om.MScriptUtil()
        int_ptr = unit.asIntPtr()

        selectionList = om.MSelectionList()#创建空列表
        selectionList.add(mesh_name)#把元素添加到列表
        dagPath = om.MDagPath()#创建地址路径
        selectionList.getDagPath(0, dagPath)#获取地址路径给列表
        fnMesh = om.MFnMesh(dagPath)

        intersection = fnMesh.closestIntersection(om.MFloatPoint(pos2),om.MFloatVector(dir),None,None,False,
        om.MSpace.kWorld,99999,False,None,hitpoint,None,# hitRayParam
        int_ptr,# hitFace
        None,None,None)

        if intersection:
            face_id = unit.getInt(int_ptr)
            return mesh_name + '.f[{0}]'.format(face_id)
        else:
            face_id = None
            cmds.warning('No mesh')
#按面获取最大影响
def getMaxInfluenceByFace(face_id,skin_name):
    vertex_list = cmds.polyListComponentConversion(face_id, ff=True, tv=True)
    vertex_list_fl = cmds.ls(vertex_list,fl=True)
    max_inf = []
    for ii in range(len(vertex_list_fl)):
       influence = cmds.skinPercent(skin_name, vertex_list_fl[ii], query=True, t=None)
       value = cmds.skinPercent(skin_name, vertex_list_fl[ii], query=True, v=1)
       max_inf.append(influence[value.index(max(value))])
    return list(set(max_inf))[0]
#呼出权重绘制窗口
def callPaintListWindowWithSetInfluence(max_inf):
    mel.eval('artSkinInflListChanging "{0}" 1'.format(max_inf))
    mel.eval('artSkinInflListChanged artAttrSkinPaintCtx;')
    cmds.headsUpMessage('{0}'.format(max_inf),t=1)
#使用影响集蒙皮列表
def UseInfluenceSetSkinList(mesh_name):
    face_id = getFaceIDbyMouseCursor(mesh_name)
    if face_id:
        skin = mel.eval('findRelatedSkinCluster("{0}");'.format(mesh_name))
        if skin:
            max_inf = getMaxInfluenceByFace(face_id,skin)
            if cmds.treeView('theSkinClusterInflList',q=True,ex=True) == False:
                mel.eval('ArtPaintSkinWeightsToolOptions')
                callPaintListWindowWithSetInfluence(max_inf)
            else:
                if cmds.treeView('theSkinClusterInflList',q=True,io=True) == True:
                    mel.eval('ArtPaintSkinWeightsToolOptions')
                    callPaintListWindowWithSetInfluence(max_inf)
                else:
                    callPaintListWindowWithSetInfluence(max_inf)
    
def mainFunc():
    mesh = cmds.ls(sl=True)
    if mesh:
        if '.' not in mesh[0]:
            UseInfluenceSetSkinList(mesh[0])
        else:
            name = mesh[0].split('.')[0]
            if cmds.objExists(name):
                UseInfluenceSetSkinList(name)

mainFunc()
