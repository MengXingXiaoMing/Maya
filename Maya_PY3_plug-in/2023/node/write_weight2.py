# coding=gbk
import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
class NewWrapUtils:
    """NewWrap 使用工具类 - 节点使用与定义分离"""

    @staticmethod
    def create_new_wrap(geometry_name, name="NewWrap1"):
        """
        创建NewWrap变形器并应用到指定几何体

        Args:
            geometry_name: 要变形的几何体名称
            name: 变形器名称

        Returns:
            tuple: (变形器名称, 几何体名称) 或 (None, None) 如果失败
        """
        try:
            # 选择几何体并创建变形器
            cmds.select(geometry_name)
            deformer = cmds.deformer(type="NewWrap", name=name)

            if deformer:
                print(f"成功创建NewWrap变形器: {deformer[0]}")
                return deformer[0], geometry_name
            else:
                print("创建变形器失败")
                return None, None

        except Exception as e:
            print(f"创建NewWrap变形器失败: {e}")
            return None, None

    @staticmethod
    def connect_surface_pair(deformer_name, wire_surface, base_surface, pair_index=0):
        """
        连接曲面对到NewWrap节点

        Args:
            deformer_name: 变形器名称
            wire_surface: Wire曲面名称
            base_surface: Base曲面名称
            pair_index: 曲面对索引

        Returns:
            bool: 是否成功
        """
        try:
            # 获取曲面形状节点
            wire_shapes = cmds.listRelatives(wire_surface, shapes=True) or []
            base_shapes = cmds.listRelatives(base_surface, shapes=True) or []

            if not wire_shapes or not base_shapes:
                print("无法获取曲面形状节点")
                return False

            wire_shape = wire_shapes[0]
            base_shape = base_shapes[0]

            # 构建属性路径
            wire_attr = f"{deformer_name}.surfacePairs[{pair_index}].wireSurface[0]"
            base_attr = f"{deformer_name}.surfacePairs[{pair_index}].baseSurface[0]"

            # 连接曲面
            cmds.connectAttr(f"{wire_shape}.worldSpace", wire_attr, force=True)
            cmds.connectAttr(f"{base_shape}.worldSpace", base_attr, force=True)

            print(f"成功连接曲面对[{pair_index}]:")
            print(f"  Wire曲面: {wire_surface} -> {wire_attr}")
            print(f"  Base曲面: {base_surface} -> {base_attr}")

            return True

        except Exception as e:
            print(f"连接曲面对失败: {e}")
            return False

    @staticmethod
    def set_radius(deformer_name, radius_value):
        """设置影响半径"""
        try:
            cmds.setAttr(f"{deformer_name}.radius", radius_value)
            print(f"设置 {deformer_name} 半径为 {radius_value}")
            return True
        except Exception as e:
            print(f"设置半径失败: {e}")
            return False

    @staticmethod
    def paint_weights_manual(deformer_name, pair_index=0):
        """
        手动设置权重绘制上下文
        """
        try:
            # 选择变形器
            cmds.select(deformer_name)

            # 设置当前工具为权重绘制工具
            cmds.ToolPropertyWindow()
            cmds.toolPropertySetCurrentContext("artAttrPaintContext")

            # 设置绘制属性
            weight_attr = f"{deformer_name}.weights[{pair_index}]"
            cmds.artSetToolAndSelectAttr("artAttrPaintContext", weight_attr)

            print(f"手动设置权重绘制上下文: {deformer_name}.weights[{pair_index}]")
            return True

        except Exception as e:
            print(f"手动设置权重绘制失败: {e}")
            return False

    @staticmethod
    def set_weight(deformer_name, pair_index, weight_value):
        """设置特定曲面对的权重值"""
        try:
            weight_attr = f"{deformer_name}.weights[{pair_index}]"
            cmds.setAttr(weight_attr, weight_value)
            print(f"设置 {deformer_name} 曲面对[{pair_index}]权重为: {weight_value}")
            return True
        except Exception as e:
            print(f"设置权重失败: {e}")
            return False

    @staticmethod
    def get_weight(deformer_name, pair_index):
        """获取特定曲面对的权重值"""
        try:
            weight_attr = f"{deformer_name}.weights[{pair_index}]"
            return cmds.getAttr(weight_attr)
        except:
            return 0.0

    @staticmethod
    def create_demo_scene():
        """创建演示场景"""
        # try:
        print("=== 创建NewWrap演示场景 ===")

        # 1. 创建测试平面
        plane = cmds.polyPlane(width=10, height=10, sx=20, sy=20, name="demoPlane")[0]
        print(f"创建测试平面: {plane}")

        # 2. 创建NewWrap变形器
        deformer, geometry = NewWrapUtils.create_new_wrap(plane, "NewWrap1")
        if not deformer:
            return False

        # 3. 设置半径
        NewWrapUtils.set_radius(deformer, 5.0)

        # 4. 创建测试曲面
        wire_surface = cmds.surface(du=3, dv=3, ku=(0, 0, 0, 1, 1, 1), kv=(0, 0, 0, 1, 1, 1), p=(
        (-0.5, 0, 0.5), (-0.5, 0, 0.16), (-0.5, 0, -0.16), (-0.5, 0, -0.5), (-0.16, 0, 0.5), (-0.16, 0, 0.16),
        (-0.16, 0, -0.16), (-0.16, 0, -0.5), (0.16, 0, 0.5), (0.16, 0, 0.16), (0.16, 0, -0.16), (0.16, 0, -0.5),
        (0.5, 0, 0.5), (0.5, 0, 0.16), (0.5, 0, -0.16), (0.5, 0, -0.5)), name="wireSurface")

        base_surface = cmds.surface(du=3, dv=3, ku=(0, 0, 0, 1, 1, 1), kv=(0, 0, 0, 1, 1, 1), p=(
            (-0.5, 0, 0.5), (-0.5, 0, 0.16), (-0.5, 0, -0.16), (-0.5, 0, -0.5), (-0.16, 0, 0.5), (-0.16, 0, 0.16),
            (-0.16, 0, -0.16), (-0.16, 0, -0.5), (0.16, 0, 0.5), (0.16, 0, 0.16), (0.16, 0, -0.16), (0.16, 0, -0.5),
            (0.5, 0, 0.5), (0.5, 0, 0.16), (0.5, 0, -0.16), (0.5, 0, -0.5)), name="baseSurface")
        # wire_surface = cmds.surface(name="wireSurface")[0]
        # base_surface = cmds.surface(name="baseSurface")[0]
        print(f"创建测试曲面: {wire_surface}, {base_surface}")

        # 5. 连接曲面对
        NewWrapUtils.connect_surface_pair(deformer, wire_surface, base_surface, 0)

        # 6. 设置初始权重
        NewWrapUtils.set_weight(deformer, 0, 1.0)
        NewWrapUtils.set_weight(deformer, 1, 0.5)  # 为第二个pair预留

        print("=== 演示场景创建完成 ===")
        print("使用方法:")
        print("1. 选择 NewWrap1 变形器")
        print("2. 运行: NewWrapUtils.paint_weights('NewWrap1', 0) 绘制权重")
        print("3. 在权重绘制工具中操作")

        return True

        # except Exception as e:
        #     print(f"创建演示场景失败: {e}")
        #     return False


# 使用示例 - 在Maya中运行这些命令

def test_new_wrap():
    """测试NewWrap变形器"""

    # 1. 创建演示场景
    success = NewWrapUtils.create_demo_scene()
    if not success:
        print("演示场景创建失败")
        return

    # 2. 获取变形器名称
    deformer_name = "NewWrap1"

    # 3. 检查节点属性
    print("\n=== 检查节点属性 ===")
    attrs = cmds.listAttr(deformer_name)
    print("节点属性:", [attr for attr in attrs if not attr.startswith('__')])

    # 4. 检查曲面对连接
    print("\n=== 检查曲面对连接 ===")
    for i in range(3):  # 检查前3个pair
        wire_attr = f"{deformer_name}.surfacePairs[{i}].wireSurface[0]"
        base_attr = f"{deformer_name}.surfacePairs[{i}].baseSurface[0]"

        wire_conn = cmds.listConnections(wire_attr, source=True) or []
        base_conn = cmds.listConnections(base_attr, source=True) or []

        print(f"曲面对[{i}]: Wire连接={wire_conn}, Base连接={base_conn}")

    # 5. 检查权重
    print("\n=== 检查权重值 ===")
    for i in range(3):
        weight = NewWrapUtils.get_weight(deformer_name, i)
        print(f"权重[{i}]: {weight}")

    print("\n测试完成! 现在可以开始绘制权重。")


# 运行测试（取消注释来执行）
test_new_wrap()
NewWrapUtils().paint_weights_manual('NewWrap1', pair_index=0)