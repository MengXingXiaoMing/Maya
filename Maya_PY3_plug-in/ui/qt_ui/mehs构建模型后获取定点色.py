# coding=gbk
# coding=gbk
import maya.cmds as cmds
import maya.OpenMaya as om
import os


def create_image_simple_method(mesh_name, output_path="D:/vertex_colors.png", img_size1=960, img_size2=540):
    """
    使用更简单的方法创建图片
    """
    if not cmds.objExists(mesh_name):
        return f"错误: 找不到网格 '{mesh_name}'"

    # 获取面颜色
    face_count = cmds.polyEvaluate(mesh_name, face=True)
    colors = []

    for face_idx in range(min(face_count, img_size1 * img_size2)):
        color_data = cmds.polyColorPerVertex(f'{mesh_name}.f[{face_idx}]', query=True, colorRGB=True)
        if color_data and len(color_data) >= 3:
            colors.append(color_data[:3])
        else:
            colors.append([1.0, 1.0, 1.0])

    # 补全颜色
    if len(colors) < img_size1 * img_size2:
        needed = img_size1 * img_size2 - len(colors)
        colors += colors[:needed]

    # 创建MImage对象
    mimage = om.MImage()

    # 方法2: 使用createFromInt创建指定大小的缓冲区[1](@ref)
    buffer_size = img_size1 * img_size2
    util = om.MScriptUtil()

    # 创建足够大的缓冲区（每个像素4字节）
    pixel_count = img_size1 * img_size2
    buffer_values = [0] * (pixel_count * 4)  # RGBA × 像素数

    # 填充像素数据
    for i in range(pixel_count):
        if i < len(colors):
            r, g, b = colors[i]
        else:
            r, g, b = 1.0, 1.0, 1.0  # 默认白色

        buffer_values[i * 4] = int(r * 255)  # R
        buffer_values[i * 4 + 1] = int(g * 255)  # G
        buffer_values[i * 4 + 2] = int(b * 255)  # B
        buffer_values[i * 4 + 3] = 255  # A

    # 使用正确的方法创建缓冲区
    util.createFromList(buffer_values, len(buffer_values))
    ptr = util.asUcharPtr()

    # 设置像素并保存
    mimage.setPixels(ptr, img_size1, img_size2)

    # 确保目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mimage.writeToFile(output_path, "png")
    return f"图片已保存: {output_path}"


# 使用
result = create_image_simple_method("MASH1_ReproMesh1")
print(result)