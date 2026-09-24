# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import sys


class SelfSpaceName(ompx.MPxNode):
    def __init__(self):
        super(SelfSpaceName, self).__init__()

    node_name = "SelfSpaceName"
    n = 27  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    id = om.MTypeId(target_id)

    # 属性声明
    # inMesh = om.MObject()
    # outMesh = om.MObject()
    # input = om.MObject()
    # targetMesh = om.MObject()

    def compute(self, plug, data_block):
        # 只处理 outMesh 插头
        # envelope = data_block.inputValue(self.envelope).asFloat()  # 封套权重（0~1）
        # if envelope == 0:
        #     return

        soure = data_block.inputValue(self.soure).asFloat()
        if soure == 0:
            return

        # 检查是否需要计算的是 outputAttr
        if plug == self.out:
            # 获取输入属性的数据句柄
            # inputDataHandle = self.inputValue(self.soure)
            # 获取当前节点的MObject
            thisNode = self.thisMObject()

            # 创建MFnDependencyNode函数集
            depFn = om.MFnDependencyNode(thisNode)

            # 获取节点名称
            nodeName = depFn.name()
            print(nodeName)
            # 字符串 -> 字节序列 -> 整数
            bytes_representation = nodeName.encode('utf-8')
            int_representation = int.from_bytes(bytes_representation, 'little')
            print(int_representation)
            # print(int_representation)

            # 准备输出数组的构建器
            outputArrayHandle = data_block.outputArrayValue(self.out)
            outputArrayBuilder = outputArrayHandle.builder()  # 获取 MArrayDataBuilder 用于写入输出数组

            # 获取输入数组的元素数量
            # elementCount = inputArrayBuilder.elementCount()
            # 确保输出数组有足够的元素
            # outputArrayBuilder.setSize(len(str(int_representation)))

            # 遍历输入数组的每个元素
            for i in range(len(str(int_representation))):
                # # 获取输入数组中第 i 个元素的句柄
                # inputElementHandle = inputArrayBuilder.inputValue(i)
                # inputValue = inputElementHandle.asFloat()  # 获取该元素的浮点值
                #
                # # 进行计算：这里我们计算平方
                # resultValue = inputValue * inputValue

                # 获取输出数组中第 i 个元素的句柄，并设置计算结果
                # outputElementHandle = outputArrayBuilder.outputValue(i)
                outputElementHandle = outputArrayBuilder.addElement(i)
                outputElementHandle.setInt(int(str(int_representation)[i]))
                # outputElementHandle = outputArrayBuilder.addElement(0)
                # outputElementHandle.setInt(int_representation)

            # 将构建好的输出数组设置回数据块
            outputArrayHandle.set(outputArrayBuilder)
            outputArrayHandle.setAllClean()  # 标记所有元素为已计算

            # # 获取输出属性的数据句柄，并设置其值
            # outputDataHandle = data_block.outputValue(self.out)
            # # outputDataHandle.setString(nodeName)
            # outputDataHandle.setInt([int_representation])

            # 标记该插值为已计算（清洁）
            data_block.setClean(plug)

    @classmethod
    def nodeInitializer(cls):
        # 创建输入属性
        # # 创建输入属性
        nAttr = om.MFnNumericAttribute()
        cls.soure = nAttr.create("soure", "inValue", om.MFnNumericData.kFloat, 1.0)  # 改用inValue避免冲突
        nAttr.setStorable(True)  # 必须可存储
        nAttr.setKeyable(True)  # 关键帧支持
        nAttr.setHidden(False)  # 显示在界面
        nAttr.setReadable(True)  # 可读
        nAttr.setWritable(True)  # 可写
        # nAttr.setMin(0.0)
        # nAttr.setMax(1.0)
        nAttr.setDisconnectBehavior(om.MFnAttribute.kDelete)  # 连接断开时保留值
        # 添加属性到节点
        cls.addAttribute(cls.soure)

        # # 创建输出out属性
        # cls.out = nAttr.create("out", "om", om.MFnData.kMesh)
        # nAttr.setStorable(False)  # 动态计算，不存储
        # nAttr.setWritable(False)  # 禁止用户直接修改
        # cls.addAttribute(cls.out)

        # 使用 MFnTypedAttribute 来定义字符串属性
        nAttr = om.MFnNumericAttribute()
        cls.out = nAttr.create("output", "out", om.MFnNumericData.kInt, 0)
        nAttr.setArray(True)  # 将其设置为数组属性
        nAttr.setUsesArrayDataBuilder(True)  # 允许使用 MArrayDataBuilder 来构建数组数据
        # tAttr.setStorable(False)  # 输出属性通常不存储，由计算得到
        nAttr.setStorable(False)  # 输出属性通常不存储，由计算得到（建议）
        nAttr.setWritable(False)  # 输出属性通常不可直接写入（正确）
        cls.addAttribute(cls.out)

        # 设置属性关联：当 inputAttr 改变时，需要重新计算 outputAttr
        cls.attributeAffects(cls.soure, cls.out)

    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(SelfSpaceName())


# 插件注册保持不变
def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(
            SelfSpaceName.node_name,
            SelfSpaceName.id,
            SelfSpaceName.nodeCreator,
            SelfSpaceName.nodeInitializer
        )
    except:
        sys.stderr.write(f"注册节点失败: {SelfSpaceName.node_name}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(SelfSpaceName.id)