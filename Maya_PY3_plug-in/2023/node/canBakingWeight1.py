# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.OpenMayaAnim as omAnim
import sys
import maya.cmds as cmds
import datetime
import numpy as np
import time

# 基础皮肤集群类 - 实现简单的线性混合蒙皮变形器
class basicSkinCluster(ompx.MPxSkinCluster):
    node_name = "basicSkinCluster"
    n = 21  # 0-63

    # 使用 datetime 模块，得到浮点数形式的时间戳（秒）
    # current_datetime = datetime.datetime.now()
    # timestamp_by_datetime = int(current_datetime.timestamp() * 100000) - 176284300000000
    # print(f"当前时间戳（秒，datetime.timestamp()）: {timestamp_by_datetime}")
    # n = timestamp_by_datetime

    start_id = 0x00141480  # 起始地址
    target_id = start_id + n
    # 更改节点ID避免冲突，确保唯一性
    kPluginNodeId = om.MTypeId(target_id)

    joint_matrix_data = []
    weights_cache = []

    # 定义属性
    def __init__(self):
        ompx.MPxSkinCluster.__init__(self)

    def deform(self, data_block, geom_iter, local_to_world_matrix, geometry_index):
        """修正后的变形函数"""
        envelope_handle = data_block.inputValue(self.envelope)
        envelope_value = envelope_handle.asFloat()
        if envelope_value == 0:
            return

        isBreak = data_block.inputValue(self.isBreak).asInt()

        # 1. 获取输入网格
        input_handle = data_block.outputArrayValue(self.outputGeom)
        input_handle.jumpToElement(geometry_index)
        input_element_handle = input_handle.outputValue()
        output_geom_obj = input_element_handle.child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()

        # 使用MFnMesh
        mesh_fn = om.MFnMesh(output_geom_obj)
        points = om.MPointArray()

        # 获取影响变换
        transforms_handle = data_block.inputArrayValue(self.matrix)
        num_transforms = transforms_handle.elementCount()

        # if num_transforms == 0:
        #     return

        # 获取所有变换矩阵
        transforms = []
        for i in range(num_transforms):
            transforms_handle.jumpToArrayElement(i)
            matrix_data_handle = transforms_handle.inputValue()
            matrix_data = om.MFnMatrixData(matrix_data_handle.data())
            transforms.append(matrix_data.matrix())

        # 应用绑定姿势矩阵
        if isBreak == 0:
            print('正常执行')
            self.joint_matrix_data = []
            self.weights_cache = []
            # self.point_index = []

            # print('即时运算')
            bind_handle = data_block.inputArrayValue(self.bindPreMatrix)
            for i in range(num_transforms):
                bind_handle.jumpToArrayElement(i)
                bind_matrix_data_handle = bind_handle.inputValue()
                bind_matrix_data = om.MFnMatrixData(bind_matrix_data_handle.data())
                transforms[i] = transforms[i] * bind_matrix_data.matrix()
                self.joint_matrix_data.append(bind_matrix_data.matrix())

            # 获取权重列表
            weight_list_handle = data_block.inputArrayValue(self.weightList)
            if weight_list_handle.elementCount() == 0:
                cmds.warning('没有权重列表')
                return
            new_positions = []
            j = 0
            # print('开始循环')
            while not geom_iter.isDone():
                # self.point_index.append([])
                self.weights_cache.append([])
                # 获取当前顶点位置
                pt = geom_iter.position()
                skinned = om.MPoint(0, 0, 0, 1.0)  # 初始化为零向量，w分量为1

                # 获取当前顶点的权重
                weight_list_handle.jumpToElement(j)
                pointWeightsHandle = weight_list_handle.inputValue()
                weightsHandle = pointWeightsHandle.child(self.weights)
                weightsArrayHandle = om.MArrayDataHandle(weightsHandle)

                # 应用皮肤变形
                total_weight = False
                for i in range(num_transforms):
                    try:
                        weightsArrayHandle.jumpToElement(i)
                        weight_value = weightsArrayHandle.inputValue().asDouble()
                        # self.point_index[j].append(i)
                        # self.weights_cache[j].append(weight_value)
                    except:
                        weight_value = 0
                    self.weights_cache[j].append(weight_value)
                    if weight_value > 0.0001:  # 只处理有影响的权重
                        transformed_point = pt * transforms[i]
                        skinned += om.MVector(transformed_point) * weight_value
                        skinned = om.MPoint(skinned)
                        if weight_value > 0:
                            total_weight = True
                j += 1

                # 归一化处理
                if total_weight == False:
                    skinned = pt  # 如果没有权重影响，保持原位置
                # 设置最终位置
                # geom_iter.setPosition(skinned)
                new_positions.append(skinned)
                geom_iter.next()

            # 一次性设置所有顶点位置
            for i, pos in enumerate(new_positions):
                points.append(pos)

            mesh_fn.setPoints(points)

        else:
            # print('使用烘焙数据')
            # 优化1：将属性访问转为局部变量，减少属性查找开销
            # joint_matrix_data = self.joint_matrix_data
            # weights_cache = self.weights_cache

            # 优化2：预计算变换矩阵，避免循环内重复乘法
            for i in range(num_transforms):
                transforms[i] = transforms[i] * self.joint_matrix_data[i]

            new_positions = om.MPointArray()

            # start_time = time.time()
            # geom_iter.reset()
            # # new_positions = om.MPointArray()
            # while not geom_iter.isDone():
            #     # new_positions.append(om.MPoint())
            #     # geom_iter.setPosition(om.MPoint())
            #     geom_iter.next()
            # end_time = time.time()
            # print('计算耗时1：', end_time - start_time, '秒')
            #
            # start_time = time.time()
            # geom_iter.reset()
            # # new_positions = om.MPointArray()
            # while not geom_iter.isDone():
            #     # new_positions.append(om.MPoint())
            #     geom_iter.setPosition(om.MPoint())
            #     geom_iter.next()
            # end_time = time.time()
            # print('计算耗时2：', end_time - start_time, '秒')
            #
            # start_time = time.time()
            # geom_iter.reset()
            # new_positions = om.MPointArray()
            # while not geom_iter.isDone():
            #     new_positions.append(om.MPoint())
            #     # geom_iter.setPosition(om.MPoint())
            #     geom_iter.next()
            # mesh_fn.setPoints(new_positions)
            # end_time = time.time()
            # print('计算耗时3：', end_time - start_time, '秒')
            #
            # start_time = time.time()
            # geom_iter.reset()
            # new_positions = om.MPointArray()
            # num = geom_iter.count()
            # for i in range(num):
            #     new_positions.append(om.MPoint())
            #     pass
            # mesh_fn.setPoints(new_positions)
            # end_time = time.time()
            # print('计算耗时4：', end_time - start_time, '秒')
            # 优化4：使用for循环代替while，更符合Python习惯且稍快

            j = 0
            while not geom_iter.isDone():
                pt = geom_iter.position()

                skinned = om.MVector(0, 0, 0)  # 优化5：使用MVector避免MPoint的w分量计算
                weights = self.weights_cache[j]

                # 只处理权重大于0的顶点
                for i, weight in enumerate(weights):
                    if weight > 0:
                        # 优化8：减少临时对象创建
                        temp_vec = om.MVector(pt * transforms[i]) * weight
                        skinned += temp_vec

                new_positions.append(om.MPoint(skinned))
                geom_iter.next()
                j += 1

            '''
            # 优化1：将属性访问转为局部变量
            joint_matrix_data = self.joint_matrix_data
            weights_cache = self.weights_cache
            weights_array = np.array(weights_cache, dtype=np.float64)  # 形状应为 (num_vertices, num_transforms)
            # print('设置模型', self.n)

            for i in range(num_transforms):
                transforms[i] = transforms[i] * joint_matrix_data[i]

            # # 优化2：预计算变换矩阵
            transforms_list = []
            for trans in transforms:  # 遍历每个Maya矩阵对象 (如 om.MMatrix)
                # 创建一个空的4x4列表来存储这个矩阵的数值元素
                matrix_elements = []
                for row in range(4):
                    for col in range(4):
                        # 关键步骤：使用索引操作符 (row, col) 提取MMatrix中每个元素的值

                        element_value = trans(row, col)
                        # 确保转换为Python浮点数
                        matrix_elements.append(float(element_value))
                # 将提取的16个数值重塑为4x4的NumPy数组
                matrix_array = np.array(matrix_elements, dtype=np.float64).reshape(4, 4)
                transforms_list.append(matrix_array)
            transforms_array = np.array(transforms_list)

            # 将MPointArray转换为NumPy数组（需要提前获取所有顶点位置）
            points_list = []
            geom_iter.reset()
            while not geom_iter.isDone():
                pt = geom_iter.position()
                points_list.append([pt.x, pt.y, pt.z])
                geom_iter.next()
            points_array = np.array(points_list)  # 形状为 (num_vertices, 3)
            # 将列表转换为 NumPy 数组，此时数组行数即为顶点数量

            # 向量化蒙皮计算
            skinned_positions = np.zeros((geom_iter.count(), 3))
            for i in range(num_transforms):
                # 扩展顶点坐标以进行矩阵乘法（添加齐次坐标w=1）
                points_homogeneous = np.hstack((points_array, np.ones((geom_iter.count(), 1))))  # 形状 (num_vertices, 4)
                # 应用变换矩阵 (num_vertices, 4) x (4,4).T -> (num_vertices, 4)
                transformed = np.dot(points_homogeneous, transforms_array[i].T)
                # 只取xyz坐标，并乘以对应权重
                weights_i = weights_array[:, i:i + 1]  # 形状 (num_vertices, 1)
                skinned_positions += transformed[:, :3] * weights_i

            # 将结果转换回MPointArray
            new_positions = om.MPointArray()
            for pos in skinned_positions:
                new_positions.append(om.MPoint(pos[0], pos[1], pos[2]))
            # i=0
            # while not geom_iter.isDone():
            #     geom_iter.setPoint(new_positions[i])
            #     i+=1
            #     geom_iter.next()
            '''

            mesh_fn.setPoints(new_positions)

    # 节点创建函数
    @classmethod
    def creator(self):
        return ompx.asMPxPtr(basicSkinCluster())

    # 节点初始化函数 - 必须正确定义属性
    @classmethod
    def initialize(cls):
        # 创建烘焙属性
        nAttr = om.MFnNumericAttribute()
        cls.isBreak = nAttr.create("isBreak", "ib", om.MFnNumericData.kInt, 0)
        nAttr.setMin(0)
        nAttr.setMax(1)
        nAttr.setStorable(True)  # 关键：允许属性被存储
        nAttr.setConnectable(True)  # 允许连接，但断开后依靠默认值或内部状态
        nAttr.setKeyable(True)
        cls.addAttribute(cls.isBreak)

        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.isBreak, outputGeom)

# 插件初始化函数
def initializePlugin(obj):
    plugin = ompx.MFnPlugin(obj, "KangmingZhan", "1.0", "Any")

    try:
        print("正在尝试注册basicSkinCluster节点")

        result = plugin.registerNode(
            basicSkinCluster.node_name,
            basicSkinCluster.kPluginNodeId,
            basicSkinCluster.creator,
            basicSkinCluster.initialize,
            ompx.MPxNode.kSkinCluster
        )

        print("basicSkinCluster节点注册成功！")
        return result

    except Exception as e:
        error_msg = f"注册basicSkinCluster节点失败: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        om.MGlobal.displayError(error_msg)


# 插件卸载函数
def uninitializePlugin(obj):
    plugin = ompx.MFnPlugin(obj)

    try:
        plugin.deregisterNode(basicSkinCluster.kPluginNodeId)
        print("basicSkinCluster节点注销成功！")
    except Exception as e:
        error_msg = f"注销basicSkinCluster节点失败: {str(e)}"
        print(error_msg)
        om.MGlobal.displayError(error_msg)

'''
proc connectJointCluster( string $j, int $i )
{
    if ( !objExists( $j+".lockInfluenceWeights" ) )
    {
        select -r $j;
        addAttr -sn "liw" -ln "lockInfluenceWeights" -at "bool";
    }
    connectAttr ($j+".liw") ("basicSkinCluster1.lockWeights["+$i+"]");
    connectAttr ($j+".worldMatrix[0]") ("basicSkinCluster1.matrix["+$i+"]");
    connectAttr ($j+".objectColorRGB") ("basicSkinCluster1.influenceColor["+$i+"]");
    float $m[] = `getAttr ($j+".wim")`;
    setAttr ("basicSkinCluster1.bindPreMatrix["+$i+"]") -type "matrix" $m[0] $m[1] $m[2] $m[3] $m[4] $m[5] $m[6] $m[7] $m[8] $m[9] $m[10] $m[11] $m[12] $m[13] $m[14] $m[15];
}
joint -p 1 0 0 ;
joint -p 0 1 0 ;
//joint -e -zso -oj xyz -sao yup joint1;
joint -p 0 0 1 ;
//joint -e -zso -oj xyz -sao yup joint2;
polyTorus -r 1 -sr 0.5 -tw 0 -sx 500 -sy 500 -ax 0 1 0 -cuv 1 -ch 0;
deformer -type "basicSkinCluster";
setAttr basicSkinCluster1.useComponentsMatrix 1;
connectJointCluster( "joint1", 0 );
connectJointCluster( "joint2", 1 );
connectJointCluster( "joint3", 2 );
skinCluster -e -maximumInfluences 3 basicSkinCluster1;  // forces computation of default weights
'''