# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import math
from math import pi, sin
import sys


class GetSpineWeight(ompx.MPxNode):
    def __init__(self):
        super(GetSpineWeight, self).__init__()

    node_name = "GetSpineWeight"
    n = 1  # 0-63
    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    Uv_id = om.MTypeId(target_id)

    # 属性声明
    input = om.MObject()

    def compute(self, plug, data_block):
        # 获取钳制范围
        clamp_Handle = data_block.inputValue(self.clamp)
        clamp_Value = clamp_Handle.asFloat()

        # 获取基础权重
        base_weight_Handle = data_block.inputValue(self.base_weight)
        base_weight_Value = base_weight_Handle.asFloat()

        # 获取对象数量
        number_objects_Handle = data_block.inputValue(self.number_objects)
        number_objects_Value = number_objects_Handle.asInt()


        # 获取整体偏移
        time_Handle = data_block.inputValue(self.time)
        time_Value = time_Handle.asFloat()

        # 基础频率
        base_frequency_Handle = data_block.inputValue(self.base_frequency)
        base_frequency_Value = base_frequency_Handle.asFloat()


        # 获取偏移速度
        range_Handle = data_block.inputValue(self.range)
        range_Value = range_Handle.asFloat()

        # 两端收缩切换重映射
        shrink_remapping_Handle = data_block.inputValue(self.shrink_remapping)
        shrink_remapping_Value = shrink_remapping_Handle.asFloat()

        # 前端收缩
        front_shrink_Handle = data_block.inputValue(self.front_shrink)
        front_shrink_Value = front_shrink_Handle.asFloat()

        # 前端收缩倍率
        front_shrink_magnification_Handle = data_block.inputValue(self.front_shrink_magnification)
        front_shrink_magnification_Value = front_shrink_magnification_Handle.asFloat()

        # 后端收缩
        back_shrink_Handle = data_block.inputValue(self.back_shrink)
        back_shrink_Value = back_shrink_Handle.asFloat()

        # 后端收缩倍率
        back_shrink_magnification_Handle = data_block.inputValue(self.back_shrink_magnification)
        back_shrink_magnification_Value = back_shrink_magnification_Handle.asFloat()

        # 每个独立偏移
        # all_offset_Handle = data_block.inputValue(self.all_offset)
        # all_offset_Value = all_offset_Handle.asFloat()
        """处理稀疏数组属性的方法"""
        all_offset_Value = []
        array_handle = om.MArrayDataHandle(data_block.inputArrayValue(self.all_offset))
        # 获取实际存在的元素数量
        element_count = array_handle.elementCount()
        # 但要注意：elementCount() 返回的是已设置值的元素数量，不一定是连续索引
        for i in range(element_count):
            array_handle.jumpToArrayElement(i)
            # 获取当前元素的逻辑索引（可能不连续）
            # logical_index = array_handle.elementIndex()
            element_handle = array_handle.inputValue()
            all_offset_Value.append(element_handle.asFloat())
            # print(f"逻辑索引: {logical_index}, 值: {element_handle.asFloat()}")

        # 获取输出数组的句柄######################################################
        output_array_handle = om.MArrayDataHandle(data_block.outputArrayValue(self.output))

        # 创建数组数据构建器
        outputArrayBuilder = om.MArrayDataHandle(output_array_handle)  # 转换为MArrayDataHandle

        # 确保构建器有足够的元素
        current_count = outputArrayBuilder.elementCount()
        # 如果number_objects为-1，则使用all_offset数组的长度
        if current_count > len(all_offset_Value):
            need_add = current_count - len(all_offset_Value)
            for i in range(need_add):
                all_offset_Value.append(0.0)

        if number_objects_Value < 0:
            # num_elements = len(all_offset_Value)
            number_objects_Value = current_count

        # 计算并设置每个元素的值
        for i in range(current_count):
            # 安全地获取偏移值
            num = all_offset_Value[i]
            index = i
            # print(self.clamp_commend(0, 1, self.remap_commend(shrink_remapping_Value, 0, 1, sin(self.clamp_commend(0, 1.570796, 1.570796 /number_objects_Value * (front_shrink_Value+index) * front_shrink_magnification_Value)), 1)))
            out = self.clamp_commend(clamp_Value * -1, clamp_Value, self.clamp_commend(0, 1, self.remap_commend(shrink_remapping_Value, 0, 1, sin(self.clamp_commend(0, 1.570796, 1.570796 /number_objects_Value * (front_shrink_Value+index) * front_shrink_magnification_Value)), 1)) *
                                                                    self.clamp_commend(0, 1, self.remap_commend(shrink_remapping_Value, 0, 1, sin(self.clamp_commend(0, 1.570796, 1.570796 /number_objects_Value * (back_shrink_Value+number_objects_Value-index-1) * back_shrink_magnification_Value)), 1)) *
                                                                    base_weight_Value * sin(base_frequency_Value * time_Value * 2 * 3.141592 +range_Value *index +num))

            # 为输出数组的当前索引位置设置值
            outputArrayBuilder.jumpToElement(i)
            outputValueHandle = outputArrayBuilder.outputValue()
            outputValueHandle.setFloat(out)
        # 将构建器设置回数组句柄
        # output_array_handle.set(builder)
        # 标记plug为已计算，避免重复计算
        data_block.setClean(plug)

    def remap_commend(self, value, old_min, old_max, new_min, new_max):
        # 检查原始区间是否有效，避免除零错误
        if old_max - old_min == 0:
            raise ValueError("原始区间的最小值和最大值不能相同")

        # 计算公式：新值 = 新最小值 + (原值 - 原最小值) * (新范围) / (原范围)
        return new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)

    def clamp_commend(self, min_value, max_value, value):
        # 使用内置的 max 和 min 函数进行钳制
        return max(min_value, min(value, max_value))

    @classmethod
    def nodeInitializer(self):
        # 创建数值属性函数集
        nAttr = om.MFnNumericAttribute()

        # 钳制
        self.clamp = nAttr.create('clamp', 'clamp', om.MFnNumericData.kFloat, 1.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)

        # 基础权重
        self.base_weight = nAttr.create('base_weight', 'base_weight', om.MFnNumericData.kFloat, 1.0)
        nAttr.setStorable(True)  # 允许属性被存储到文件中
        nAttr.setKeyable(True)  # 允许在通道盒中设置关键帧
        nAttr.setWritable(True)  # 允许属性可写

        # 对象数量，-1为自动获取全部
        self.number_objects = nAttr.create('number_objects', 'number_objects', om.MFnNumericData.kInt, -1)
        nAttr.setMin(-1)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)

        # 获取整体偏移
        self.time = nAttr.create('time', 'time', om.MFnNumericData.kFloat, 0.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)

        # 基础频率
        self.base_frequency = nAttr.create('frequency', 'frequency', om.MFnNumericData.kFloat, 0.1)
        nAttr.setStorable(True)  # 允许属性被存储到文件中
        nAttr.setKeyable(True)  # 允许在通道盒中设置关键帧
        nAttr.setWritable(True)  # 允许属性可写

        # 获取偏移速度
        self.range = nAttr.create('range', 'range', om.MFnNumericData.kFloat, 1.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)

        # 两端收缩切换重映射
        self.shrink_remapping = nAttr.create('shrink_remapping', 'shrink_remapping', om.MFnNumericData.kFloat, 1.0)
        nAttr.setMin(0)
        nAttr.setMax(1)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)

        # 前端收缩
        self.front_shrink = nAttr.create('front_shrink', 'front_shrink', om.MFnNumericData.kFloat, 0.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        # 前端收缩倍率
        self.front_shrink_magnification = nAttr.create('front_shrink_magnification', 'front_shrink_magnification', om.MFnNumericData.kFloat, 0.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)

        # 后端收缩
        self.back_shrink = nAttr.create('back_shrink', 'back_shrink', om.MFnNumericData.kFloat, 0.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)
        # 后端收缩倍率
        self.back_shrink_magnification = nAttr.create('back_shrink_magnification', 'back_shrink_magnification', om.MFnNumericData.kFloat, 0.0)
        nAttr.setStorable(True)
        nAttr.setKeyable(True)
        nAttr.setWritable(True)

        # 每个独立偏移
        self.all_offset = nAttr.create("all_offset", "ao", om.MFnNumericData.kFloat, 0.0)
        nAttr.setArray(True)
        nAttr.setStorable(True)
        # nAttr.setKeyable(True)
        nAttr.setReadable(True)
        nAttr.setWritable(True)
        nAttr.setUsesArrayDataBuilder(True)  # 允许使用数组数据构建器

        # 创建数组属性的“父”属性
        self.output = nAttr.create('output', 'out', om.MFnNumericData.kFloat, 0.0)
        nAttr.setStorable(False)
        nAttr.setWritable(False)
        nAttr.setReadable(True)
        nAttr.setArray(True)  # 将其标记为数组属性
        # nAttr.setIndexMatters(True)  # 索引很重要
        nAttr.setUsesArrayDataBuilder(True)  # 新增这行代码

        # 将属性添加到节点
        self.addAttribute(self.clamp)
        self.addAttribute(self.base_weight)
        self.addAttribute(self.number_objects)
        self.addAttribute(self.time)
        self.addAttribute(self.base_frequency)
        self.addAttribute(self.range)
        self.addAttribute(self.shrink_remapping)
        self.addAttribute(self.front_shrink)
        self.addAttribute(self.front_shrink_magnification)
        self.addAttribute(self.back_shrink)
        self.addAttribute(self.back_shrink_magnification)
        self.addAttribute(self.all_offset)
        self.addAttribute(self.output)

        # 设置属性依赖关系
        self.attributeAffects(self.clamp, self.output)
        self.attributeAffects(self.base_weight, self.output)
        self.attributeAffects(self.number_objects, self.output)
        self.attributeAffects(self.time, self.output)
        self.attributeAffects(self.range, self.output)
        self.attributeAffects(self.shrink_remapping, self.output)
        self.attributeAffects(self.front_shrink, self.output)
        self.attributeAffects(self.front_shrink_magnification, self.output)
        self.attributeAffects(self.back_shrink, self.output)
        self.attributeAffects(self.back_shrink_magnification, self.output)
        self.attributeAffects(self.all_offset, self.output)


    @classmethod
    def nodeCreator(cls):
        return ompx.asMPxPtr(GetSpineWeight())


# 插件注册保持不变
def initializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject, "KangmingZhan", "1.0.0")
    try:
        plugin.registerNode(
            GetSpineWeight.node_name,
            GetSpineWeight.Uv_id,
            GetSpineWeight.nodeCreator,
            GetSpineWeight.nodeInitializer
        )
    except:
        sys.stderr.write(f"注册节点失败: {GetSpineWeight.node_name}")


def uninitializePlugin(mobject):
    plugin = ompx.MFnPlugin(mobject)
    plugin.deregisterNode(GetSpineWeight.Uv_id)