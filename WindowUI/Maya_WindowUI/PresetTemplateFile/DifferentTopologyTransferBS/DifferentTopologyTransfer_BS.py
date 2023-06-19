# coding=gbk
import pymel.core as pm
# 获取文件路径
import os
import inspect
import sys
sys.dont_write_bytecode = True
# 加载文本
ZKM_RootDirectory = os.path.join('\\'.join(os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-5]))
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaUI')
from LoadText import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaBS')
from BsModelEdit import *
sys.path.append(ZKM_RootDirectory + '\\Maya\\MayaWeight')
from JointWeightProcessing import *
import webbrowser

class ZKM_WindowBsChuLiWindowClass:
    def __init__(self):
        cur_dir = '\\'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_path = os.path.join(cur_dir)  # 获取文件路径
        cur_dirA = '/'.join(
            os.path.abspath(inspect.getsourcefile(lambda: 0)).split('\\')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        file_pathReversion = os.path.join(cur_dirA)  # 获取文件路径A
        # 通过self向新建的对象中初始化属性
        self.file_path = file_path
        self.file_pathA = file_pathReversion
    def ZKM_WindowBsChuLi(self):
        if pm.window('WindowBsChuLi', ex=1):
            pm.deleteUI('WindowBsChuLi')
        pm.window('WindowBsChuLi', t="BS处理")
        pm.columnLayout()
        pm.rowColumnLayout(nc=2, adj=1)
        pm.rowColumnLayout(nc=1, adj=2)
        pm.rowColumnLayout(nc=6, adj=1)
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_OpenWrap4D()', l="选择模型开始创建中间态模型(先选模板模型)")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().ImportIntermediate()', l="导入中间态模型")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_TransferUV()', l="传递UV（先选中间态模型，再选目标模型）")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_SelectPointCorrectUV()', l="选择点修正UV(不能重叠，只修正飞点部分)")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_TestTemplate()', bgc=(1, 1, 1), l="模板")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BsCL_UsingHelp()', bgc=(1, 1, 1), l="帮助")
        pm.setParent('..')
        pm.rowColumnLayout(nc=8, adj=8)
        pm.text(l="异拓补传递BS：")
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_TransmitSource\')', l="含BS的模型:")
        pm.textFieldButtonGrp('BsCL_TransmitSource', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_TransmitSource\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_IntermediateState\')', l="中间态模型:")
        pm.textFieldButtonGrp('BsCL_IntermediateState', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_IntermediateState\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_TransmitTarget\')', l="BS传递目标:")
        pm.textFieldButtonGrp('BsCL_TransmitTarget', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_TransmitTarget\')')
        pm.rowColumnLayout(nc=8, adj=8)
        pm.button(c='ZKM_WindowBsChuLiWindowClass().TransferDifferentTopologies_BS()', l="传递bs")
        pm.button(c='ZKM_WindowBsChuLiWindowClass().UVCopyWeight()', l='UV复制权重')
        pm.setParent('..')
        pm.text(l="烘焙bs到模型：")
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_BakingModel\')', l="需烘焙模型:")
        pm.textFieldButtonGrp('BsCL_BakingModel', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BakingModel\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_BakingModel_BS\')', l="选择BS节点:")
        pm.textFieldButtonGrp('BsCL_BakingModel_BS', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BakingModel_BS\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_BakingBsAttribute\')', l="具体BS属性:")
        pm.textFieldButtonGrp('BsCL_BakingBsAttribute', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BakingBsAttribute\')')
        pm.button(c='ZKM_WindowBsChuLiWindowClass().BakingBS()', l="烘焙BS")
        pm.text(l="分解BS：")
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_DecomposeSource\')', l="分解源模型:")
        pm.textFieldButtonGrp('BsCL_DecomposeSource', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_DecomposeSource\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_DecomposeSource_BS\')', l="具体BS属性:")
        pm.textFieldButtonGrp('BsCL_DecomposeSource_BS', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_DecomposeSource_BS\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',\'BsCL_DecomposereFerence\')', l="分解参考模型")
        pm.textFieldButtonGrp('BsCL_DecomposereFerence', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_DecomposereFerence\')')
        pm.button(c='ZKM_WindowBsChuLiWindowClass().DecomposeBS()', l="开始分解")
        pm.text(l="BS转权重：")
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',"BsCL_BsTransmitWeightModel")', l="含BS的模型:")
        pm.textFieldButtonGrp('BsCL_BsTransmitWeightModel', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BsTransmitWeightModel\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',"BsCL_BsTransmitWeightModel_BS")', l="选择BS节点:")
        pm.textFieldButtonGrp('BsCL_BsTransmitWeightModel_BS', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BsTransmitWeightModel_BS\')')
        pm.button(c='ZKM_ReadTextClass().ZKM_ReadLoadText(\'textFieldButtonGrp\',"BsCL_BsTransmitWeightJoint")', l="脸部骨骼:")
        pm.textFieldButtonGrp('BsCL_BsTransmitWeightJoint', bl="加载", text="", cw3=(0, 100, 65), l=(""),
                              bc='ZKM_LoadTextClass().ZKM_LoadText(\'textFieldButtonGrp\',\'BsCL_BsTransmitWeightJoint\')')
        pm.button(c='ZKM_WindowBsChuLiWindowClass().HairFollicleAdsorption()', l="开始转换")
        pm.setParent('..')
        pm.setParent('..')
        pm.setParent('..')
        pm.showWindow()

    # 打开模板文件，进入Wrap4D
    def BsCL_OpenWrap4D(self):
        Sel = pm.ls(sl=1)
        pm.select(Sel[0], r=1)
        pm.mel.eval(
            'file -force -options \"groups=1;ptgroups=1;materials=0;smoothing=1;normals=1\" -typ \"OBJexport\" -pr -es (\"' + self.file_pathA + '/WrapPreset/source.obj\");')
        pm.select(Sel[1], r=1)
        pm.mel.eval(
            'file -force -options \"groups=1;ptgroups=1;materials=0;smoothing=1;normals=1\" -typ \"OBJexport\" -pr -es (\"' + self.file_pathA + '/WrapPreset/target.obj\");')
        os.startfile(self.file_path + '\\WrapPreset\\WrapTemplate.wrap')

    # 导入中间态模型
    def ImportIntermediate(self):
        pm.mel.eval(
            'file -import -type "OBJ"  -ignoreVersion -mergeNamespacesOnClash false -rpr "WrapObject" -options "mo=1"  -pr  -importTimeRange "combine" (\"' + self.file_pathA + '/WrapPreset/WrapObject.obj\");')

    # 按规范传递UV
    def BsCL_TransferUV(self):
        Sel = pm.ls(sl=1)
        pm.select(Sel[0])
        UVsetA = pm.polyUVSet(q=1, currentUVSet=1)[0]
        pm.select(Sel[1])
        UVsetB = pm.polyUVSet(q=1, currentUVSet=1)[0]
        pm.select(Sel[0],Sel[1])
        pm.transferAttributes(flipUVs=0, transferPositions=0, transferUVs=2, sourceUvSpace=str(UVsetA), searchMethod=3,
                              transferNormals=0, transferColors=2, targetUvSpace=str(UVsetB), colorBorders=1, sampleSpace=0)
        pm.select(Sel[1], r=1)
        pm.DeleteHistory()

    # 选择点修正UV
    def BsCL_SelectPointCorrectUV(self):
        Sel = pm.ls(fl=1, sl=1)
        Model = Sel[0].split(".")
        pm.mel.polyPerformAction('polyMapSew', 'e', 0)
        pm.select(cl=1)
        pm.select(Sel, r=1)
        pm.mel.performUnfold(0)
        pm.select(cl=1)
        pm.select(Model[0], r=1)
        pm.DeleteHistory()

    # 测试模板
    def BsCL_TestTemplate(self):
        os.startfile(self.file_path + '\ZKM_TransferDifferentTopologies_BS.mb')
        print ('\n使用教程视频链接：\nhttps://space.bilibili.com/173984578')
        webbrowser.open("https://space.bilibili.com/173984578")

    # 使用帮助
    def BsCL_UsingHelp(self):
        os.startfile(self.file_path + '\help.png')
        print ('\n使用教程视频链接：\nhttps://space.bilibili.com/173984578')
        webbrowser.open("https://space.bilibili.com/173984578")
    # 不同拓补传递BS
    def TransferDifferentTopologies_BS(self):
        TransmitSource = str(pm.textFieldButtonGrp('BsCL_TransmitSource', q=1, text=1))
        TransmitTarget = str(pm.textFieldButtonGrp('BsCL_TransmitTarget', q=1, text=1))
        IntermediateState = str(pm.textFieldButtonGrp('BsCL_IntermediateState', q=1, text=1))
        ZKM_DifferentTopologiesBSClass().ZKM_TransferDifferentTopologies_BS(TransmitSource, TransmitTarget, IntermediateState)


    # 烘焙BS
    def BakingBS(self):
        BakingModel = str(pm.textFieldButtonGrp('BsCL_BakingModel', q=1, text=1))
        BakingModel_BS = str(pm.textFieldButtonGrp('BsCL_BakingModel_BS', q=1, text=1))
        BakingBsAttribute = str(pm.textFieldButtonGrp('BsCL_BakingBsAttribute', q=1, text=1))
        BakingBsAttributeAll = BakingBsAttribute.split(",")
        ZKM_DifferentTopologiesBSClass().ZKM_BakingBS(BakingModel, BakingModel_BS,BakingBsAttributeAll)

    # 分解BS
    def DecomposeBS(self):
        DecomposeSource = str(pm.textFieldButtonGrp('BsCL_DecomposeSource', q=1, text=1))
        DecomposeSource_BS = str(pm.textFieldButtonGrp('BsCL_DecomposeSource_BS', q=1, text=1))
        DecomposereFerence = str(pm.textFieldButtonGrp('BsCL_DecomposereFerence', q=1, text=1))
        DecomposeSourceAll = DecomposeSource_BS.split(",")
        ZKM_DifferentTopologiesBSClass().ZKM_DecomposeBS(DecomposeSource,DecomposeSourceAll,DecomposereFerence)

    # UV拷贝权重
    def UVCopyWeight(self):
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp','BsCL_TransmitSource')
        DecomposeSource = pm.ls(sl=1)
        UVsetA = pm.polyUVSet(q=1, currentUVSet=1)[0]
        ZKM_ReadTextClass().ZKM_ReadLoadText('textFieldButtonGrp', 'BsCL_TransmitTarget')
        DecomposereFerence = pm.ls(sl=1)
        UVsetB = pm.polyUVSet(q=1, currentUVSet=1)[0]
        ZKM_JointWeightProcessingClass().ZKM_CopyWeight('UV', DecomposeSource[0], DecomposereFerence, UVsetA, UVsetB)

    # bs转权重
    def HairFollicleAdsorption(self):
        print '暂未开发\n'


if __name__ == '__main__':
    ZKM_WindowBsChuLiWindowClass().ZKM_WindowBsChuLi()
