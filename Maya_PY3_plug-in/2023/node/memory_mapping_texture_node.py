# coding=gbk
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import os
import time
from PIL import Image

# 节点类型定义
kPluginNodeTypeName = "FileTextureNode"
FileTextureNodeId = om.MTypeId(0x001242)

# 定义状态常量
kSuccess = 0
kFailure = 1
kUnknownParameter = 2


class FileTextureNode(ompx.MPxNode):
    """文件纹理节点 - 基于官方C++实现"""

    # 输入属性
    aFileName = om.MObject()  # 文件路径
    aUVCoord = om.MObject()  # UV坐标

    # 输出属性
    aOutColor = om.MObject()  # 输出颜色
    aOutAlpha = om.MObject()  # 输出Alpha

    def __init__(self):
        """初始化节点"""
        ompx.MPxNode.__init__(self)

        # 内部状态
        self._image = None  # MImage等效对象
        self._width = 0  # 纹理宽度
        self._height = 0  # 纹理高度
        self._last_modified = 0  # 最后修改时间
        self._file_path = ""  # 当前文件路径
        self._pixel_data = None  # 像素数据

    def compute(self, plug, dataBlock):
        """计算节点输出 - 核心逻辑"""
        try:
            # 只处理输出属性的计算请求
            if (plug != self.aOutColor and
                    plug.parent() != self.aOutColor and
                    plug != self.aOutAlpha):
                return kUnknownParameter

            # 获取输入数据
            file_path_handle = dataBlock.inputValue(self.aFileName)
            file_path = file_path_handle.asString()

            uv_handle = dataBlock.inputValue(self.aUVCoord)
            uv = uv_handle.asFloat2()

            # 检查是否需要重新加载纹理
            if self._should_reload(file_path):
                self._load_texture(file_path)

            # 计算输出颜色和Alpha
            out_color = om.MFloatVector(0.0, 0.0, 0.0)
            out_alpha = 1.0

            if self._pixel_data and self._width > 0 and self._height > 0:
                # 处理UV坐标
                u = max(0.0, min(1.0, uv[0]))
                v = max(0.0, min(1.0, uv[1]))

                # 计算像素位置
                row = int(v * (self._height - 1))
                col = int(u * (self._width - 1))
                print('row:',row,'col:',col)
                # 获取像素数据
                pixel_index = (row * self._width + col) * 4
                if pixel_index + 3 < len(self._pixel_data):
                    r = self._pixel_data[pixel_index] / 255.0
                    g = self._pixel_data[pixel_index + 1] / 255.0
                    b = self._pixel_data[pixel_index + 2] / 255.0
                    a = self._pixel_data[pixel_index + 3] / 255.0

                    out_color = om.MFloatVector(r, g, b)
                    out_alpha = a

            # 设置输出颜色
            out_color_handle = dataBlock.outputValue(self.aOutColor)
            out_color_handle.setMFloatVector(out_color)
            out_color_handle.setClean()

            # 设置输出Alpha
            out_alpha_handle = dataBlock.outputValue(self.aOutAlpha)
            out_alpha_handle.setFloat(out_alpha)
            out_alpha_handle.setClean()

            return kSuccess

        except Exception as e:
            om.MGlobal.displayError(f"计算错误: {str(e)}")
            return kFailure

    def _should_reload(self, file_path):
        """检查是否需要重新加载纹理"""
        if not file_path or not os.path.exists(file_path):
            return False

        try:
            # 检查文件路径是否变化
            if file_path != self._file_path:
                return True

            # 检查文件修改时间
            current_modified = os.path.getmtime(file_path)
            if current_modified > self._last_modified:
                return True

            return False

        except:
            return True

    def _load_texture(self, file_path):
        """从文件加载纹理 - 等效于MImage.readFromFile"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")

            # 使用PIL加载图像
            img = Image.open(file_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 获取图像尺寸
            width, height = img.size

            # 获取像素数据
            img_data = img.tobytes()

            # 更新内部状态
            self._pixel_data = bytearray(img_data)
            self._width = width
            self._height = height
            self._last_modified = os.path.getmtime(file_path)
            self._file_path = file_path

            om.MGlobal.displayInfo(f"成功加载纹理: {file_path} ({width}x{height})")

        except Exception as e:
            om.MGlobal.displayError(f"加载纹理失败: {str(e)}")
            self._pixel_data = None
            self._width = 0
            self._height = 0

    @classmethod
    def nodeCreator(cls):
        """创建节点实例"""
        return ompx.asMPxPtr(FileTextureNode())

    @classmethod
    def nodeInitializer(cls):
        """初始化节点属性"""
        nAttr = om.MFnNumericAttribute()
        tAttr = om.MFnTypedAttribute()

        # 输入文件路径属性（字符串）
        cls.aFileName = tAttr.create("fileName", "f", om.MFnData.kString)
        tAttr.setStorable(True)
        tAttr.setWritable(True)
        tAttr.setReadable(False)
        tAttr.setUsedAsFilename(True)  # 标记为文件路径属性
        cls.addAttribute(cls.aFileName)

        # UV坐标属性（二维浮点数）
        uAttr = nAttr.create("uCoord", "u", om.MFnNumericData.kFloat, 0.0)
        vAttr = nAttr.create("vCoord", "v", om.MFnNumericData.kFloat, 0.0)
        cls.aUVCoord = nAttr.create("uvCoord", "uv", uAttr, vAttr)
        nAttr.setStorable(True)
        nAttr.setWritable(True)
        nAttr.setReadable(False)
        cls.addAttribute(cls.aUVCoord)

        # 输出颜色属性（RGB）
        cls.aOutColor = nAttr.createColor("outColor", "oc")
        nAttr.setStorable(False)
        nAttr.setWritable(False)
        nAttr.setReadable(True)
        cls.addAttribute(cls.aOutColor)

        # 输出Alpha属性
        cls.aOutAlpha = nAttr.create("outAlpha", "oa", om.MFnNumericData.kFloat, 1.0)
        nAttr.setStorable(False)
        nAttr.setWritable(False)
        nAttr.setReadable(True)
        cls.addAttribute(cls.aOutAlpha)

        # 设置属性关联
        cls.attributeAffects(cls.aFileName, cls.aOutColor)
        cls.attributeAffects(cls.aFileName, cls.aOutAlpha)
        cls.attributeAffects(cls.aUVCoord, cls.aOutColor)
        cls.attributeAffects(cls.aUVCoord, cls.aOutAlpha)


# 插件初始化函数
def initializePlugin(mobject):
    """初始化插件"""
    mplugin = ompx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    try:
        mplugin.registerNode(
            kPluginNodeTypeName,
            FileTextureNodeId,
            FileTextureNode.nodeCreator,
            FileTextureNode.nodeInitializer
        )
        om.MGlobal.displayInfo(f"? 成功注册节点: {kPluginNodeTypeName}")
    except Exception as e:
        om.MGlobal.displayError(f"? 注册节点失败: {kPluginNodeTypeName}, 错误: {e}")
        raise


def uninitializePlugin(mobject):
    """反初始化插件"""
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(FileTextureNodeId)
        om.MGlobal.displayInfo(f"? 成功注销节点: {kPluginNodeTypeName}")
    except Exception as e:
        om.MGlobal.displayError(f"? 注销节点失败: {kPluginNodeTypeName}, 错误: {e}")
        raise