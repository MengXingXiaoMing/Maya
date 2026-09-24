# coding=gbk
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
# import numpy as np

# 指定要抓取的相机
camera_name = "side"
output_path = "D:/asdasd/asd.png"

# 获取活动 viewport
# view = omui.M3dView.active3dView()
view = omui.M3dView()
omui.M3dView.get3dView(1, view)
# 获取相机的 MDagPath（旧 API）
# sel = om.MSelectionList()
# sel.add(camera_name)
# cam_dag = om.MDagPath()
# sel.getDagPath(0, cam_dag)  # 获取 MDagPath

# 临时切换 viewport 相机到指定相机
# view.setCamera(cam_dag)  # 旧 API 下只需要一个参数
view.refresh(True, True)
# 读取颜色缓冲
image = om.MImage()
view.readColorBuffer(image, True)  # True = 包含 alpha

# 得到 RGB数据 如果写其他DG节点数据流可能会用上
rgb = image.pixels()

# 保存为 外部 PNG 文件，如果有必要 -- 不会执行新建，只能覆写，所以必须确保目标路径有文件
image.writeToFile(output_path, "png")
print("Saved capture to:", output_path)


