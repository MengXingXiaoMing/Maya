#coding=gbk
import pymel.core as pm
import maya.cmds as cmds
from os import listdir
# 获取文件路径
import os
import inspect
import sys
sys.dont_write_bytecode = True
# 加载文本
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-4]))

#加载文本
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *
#权重类
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaWeight')
from JointWeightProcessing import *
#创建模型类
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaModel')
from GenerateModel import *

class ZKM_QvanZhongChuLiWindowClass:
    def __init__(self):
        cur_dir = '\\'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_path = os.path.join(cur_dir)  # 获取文件路径
        cur_dirA = '/'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathReversion = os.path.join(cur_dirA)  # 获取文件路径A
        # 通过self向新建的对象中初始化属性
        self.file_path = file_path
        self.file_pathReversion = file_pathReversion
    def ZKM_Window(self):
        if pm.window('WindowQvanZhongChuLiPY', ex=1):
            pm.deleteUI('WindowQvanZhongChuLiPY')

        pm.window('WindowQvanZhongChuLiPY', t='权重处理')
        pm.columnLayout()
        pm.rowColumnLayout(nc=1, adj=1)
        pm.rowColumnLayout(nc=3, adj=3)
        pm.rowColumnLayout(nc=2, adj=3)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'XZKBY\')', l='选择拷贝源:')
        pm.textFieldButtonGrp('XZKBY', bl='加载', text='', cw3=(0, 100, 65), l='选择拷贝源:',
                              bc='ZKM_QvanZhongChuLiCommandsClass().ZKM_LoadText(\'textFieldButtonGrp\',\'XZKBY\')')
        pm.setParent('..')
        pm.rowColumnLayout(nc=2, adj=3)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'XZKBMXHD\')', l='选择需拷贝点:')
        pm.textFieldButtonGrp('XZKBMXHD', bl='加载', text='', cw3=(0, 100, 65), l='选择需拷贝点:',
                              bc='ZKM_QvanZhongChuLiCommandsClass().ZKM_LoadText(\'textFieldButtonGrp\',\'XZKBMXHD\')')
        pm.setParent('..')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_CopyPointWeightApply()', l='拷贝点权重')
        pm.rowColumnLayout(nc=2, adj=2)
        pm.button(c='pm.mel.CopyVertexWeights()', l='复制顶点权重')
        pm.button(c='pm.mel.PasteVertexWeights()', l='粘贴顶点权重')
        pm.button(c='pm.mel.removeUnusedInfluences()', l='移除无权重骨骼')
        #pm.button(c='ZKM_QvanZhongChuLiCommandsClass().AbsolutePositionMirrorWeight()', l='绝对位置镜像权重(停用)')
        pm.setParent('..')
        pm.rowColumnLayout(nc=7, adj=1)
        pm.iconTextButton(i='paintSkinWeights.png', flat=0, style='iconAndTextCentered',
                          c='pm.mel.ArtPaintSkinWeightsTool()', l='')
        pm.iconTextButton(flat=0, style='iconAndTextCentered', i='weightHammer.png', h=45,
                          c='pm.mel.weightHammerVerts()', l='')
        pm.iconTextButton(i='copySkinWeight.png', flat=0, style='iconAndTextCentered', c='pm.mel.CopySkinWeights()',
                          l='')
        pm.iconTextButton(i='mirrorSkinWeight.png', flat=0, style='iconAndTextCentered', c='pm.mel.MirrorSkinWeights()',
                          l='')
        pm.iconTextButton(i='moveSkinnedJoint.png', flat=0, style='iconAndTextCentered',
                          c='pm.mel.MoveSkinJointsTool()', l='')
        pm.iconTextButton(i='moveVertexWeights.png', flat=0, style='iconAndTextCentered',
                          c='pm.mel.artAttrMoveInfluence()', l='')
        pm.iconTextButton(i='showInfluence.png', flat=0, style='iconAndTextCentered',
                          c='pm.mel.artAttrShowInfluences(\'artAttrSkinPaintCtx\')', l='')
        pm.setParent('..')
        pm.rowColumnLayout(nc=1, adj=1)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_CopyModelWeightApply()', l='拷贝权重(先选源模型)')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_HalfCopyModelWeightApply()', l='对半拷贝权重')
        pm.setParent('..')
        pm.setParent('..')
        pm.rowColumnLayout(nc=3, adj=3)
        pm.optionMenu('NormalizeWeight', label='')
        pm.menuItem(label='后期')
        pm.menuItem(label='交互')
        pm.optionMenu('NormalizeWeight', edit=1, select=1)
        pm.intSliderGrp('SmoothWeightType', min=1, max=100, cw3=(60, 40, 258), f=1, fieldMaxValue=9999, l='平滑次数：', v=1)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_SmoothWeightApply()', l='平滑权重', w=60)
        pm.setParent('..')
        pm.rowColumnLayout(nc=4, adj=3)
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'XZYMX\')', l='选择原模型:')
        pm.textFieldButtonGrp('XZYMX', bl='加载', bc='ZKM_QvanZhongChuLiCommandsClass().ZKM_LoadText(\'textFieldButtonGrp\',\'XZYMX\')')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_MergeWeightsToTargetsApply()', l='选择模型合并权重到目标')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ExportWeights()', l='导出权重')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'ZYQZ\')', l='选择模型:')
        pm.textFieldButtonGrp('ZYQZ', bl='加载', bc='ZKM_QvanZhongChuLiCommandsClass().ZKM_LoadText(\'textFieldButtonGrp\',\'ZYQZ\')')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().TransferWeights()', l='转移权重(先选要转移的骨骼)')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().ImportWeights()', l='导入权重')
        pm.setParent('..')
        pm.rowColumnLayout(bgc=(0.7, 0.7, 1), adj=2, nc=8)
        pm.textFieldGrp('ModelFace', text='2000', cw2=(80, 70), l='模型面数(大致):')
        pm.floatSliderGrp('ReduceDetail', min=1, max=100, cw3=(50, 30, 100), f=1, fieldMaxValue=9999, l='减少细节', v=20)
        pm.floatSliderGrp('Smoothness', min=1, max=100, cw3=(50, 40, 100), f=1, fieldMaxValue=9999, l='平滑程度', v=100)
        pm.setParent('..')
        pm.rowColumnLayout(bgc=(0.7, 0.7, 1), adj=1, nc=9)
        
        pm.text(l='简模镜像方向(世界轴)')
        pm.radioCollection('FKKZQSC_ModelMirror')
        pm.radioButton('None', label='None')
        pm.radioButton('X', label='X→-X')
        pm.radioButton('FX', label='-X→X')
        pm.radioButton('Y', label='Y→-Y')
        pm.radioButton('FY', label='-Y→Y')
        pm.radioButton('Z', label='Z→-Z')
        pm.radioButton('FZ', label='-Z→Z')
        pm.radioCollection('FKKZQSC_ModelMirror', edit=1, select='X')
        pm.button(c='ZKM_QvanZhongChuLiCommandsClass().GeneratingSimpleModuleApply()', l='生成简模(先清理模型)')
        
        pm.setParent('..')
        pm.setParent('..')
        pm.showWindow()
class ZKM_QvanZhongChuLiCommandsClass:
    # 加载选择为文本
    def ZKM_LoadText(self, Type, Name):
        ZKM_LoadTextClass().ZKM_LoadText(Type, Name)

    # 选择对应文本的内容
    def ZKM_ReadLoadText(self, Type, Name):
        ZKM_ReadTextClass().ZKM_ReadLoadText(Type, Name)

    # 拷贝点权重
    def ZKM_CopyPointWeightApply(self):
        Soure = pm.textFieldButtonGrp('XZKBY', q=1, text=1)
        Target = pm.textFieldButtonGrp('XZKBMXHD', q=1, text=1).split(',')
        ZKM_JointWeightProcessingClass().ZKM_CopyWeight('Normal', Soure, Target, '', '')

    # 拷贝模型权重
    def ZKM_CopyModelWeightApply(self):
        ZKM_JointWeightProcessingClass().ZKM_CopyModelWeightApply()

    # 对半拷贝模型权重
    def ZKM_HalfCopyModelWeightApply(self):
        ZKM_JointWeightProcessingClass().ZKM_HalfCopyModelWeightApply()

    # 平滑权重
    def ZKM_SmoothWeightApply(self):
        Model = pm.ls(sl=1)
        NormalizeWeight = int(pm.optionMenu('NormalizeWeight', q=1, select=1))
        CS = pm.intSliderGrp('SmoothWeightType', q=1, v=1)
        ZKM_JointWeightProcessingClass().ZKM_SmoothWeight(Model, NormalizeWeight, CS)

    # 把模型分离后处理出来的权重返回整体
    def ZKM_MergeWeightsToTargetsApply(self):
        ModelGrp = pm.ls(sl=1)
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'XZYMX')
        YvanModel = pm.ls(sl=1)
        ZKM_JointWeightProcessingClass().ZKM_MergeWeightsToTargets(YvanModel, ModelGrp)

    # 导出权重
    def ExportWeights(self):
        Model = pm.ls(sl=1)
        MD = []
        for M in Model:
            if pm.mel.findRelatedSkinCluster(M):
                MD.append(M)
                pm.select(M)
                pm.mel.removeUnusedInfluences()
        ZKM_JointWeightProcessingClass().ExportWeight(MD)

    # 导入权重
    def ImportWeights(self):
        Model = pm.ls(sl=1)
        ZKM_JointWeightProcessingClass().ImportWeight(Model)

    # 转移权重
    def TransferWeights(self):
        Model = str(pm.textFieldButtonGrp('ZYQZ', q=1, text=1))
        ZKM_JointWeightProcessingClass().TransferWeight(Model)

    def GeneratingSimpleModuleApply(self):
        ReduceDetail = float(pm.floatSliderGrp('ReduceDetail', q=1, v=1))
        Smoothness = float(pm.floatSliderGrp('Smoothness', q=1, v=1))
        ModelMirror = str(pm.radioCollection('FKKZQSC_ModelMirror', q=1, select=1))
        FaceNum = float(pm.textFieldGrp('ModelFace', q=1, text=1))
        sel = pm.ls(sl=1)
        ZKM_RegenerateExistingModelClass().GeneratingSimpleModule(sel, FaceNum, ModelMirror, ReduceDetail, Smoothness)

ShowWindow = ZKM_QvanZhongChuLiWindowClass()
if __name__ == '__main__':
    ShowWindow.ZKM_Window()
