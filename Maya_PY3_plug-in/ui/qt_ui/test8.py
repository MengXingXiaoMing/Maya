# coding=gbk
"""
修复版内存映射文件生成器 - 与C++代码完全兼容
"""

import struct
import sys
import os
from PIL import Image


def create_compatible_mmap(image_path, mmap_path):
    """
    创建与C++代码兼容的内存映射文件
    """
    try:
        print(f"? 处理: {image_path} -> {mmap_path}")

        # 打开图像并转为RGBA
        img = Image.open(image_path).convert('RGBA')
        width, height = img.size

        # 计算数据大小（确保与C++代码匹配）
        data_size = width * height * 4  # RGBA = 4字节每像素

        # 修复：使用与C++完全匹配的文件头格式
        # struct.pack格式说明：
        # '<' : 小端字节序（与x86架构匹配）
        # 'I' : unsigned int (4字节)
        # 顺序: 宽度、高度、数据大小、版本号
        header = struct.pack('<IIII',
                             width,  # 图像宽度
                             height,  # 图像高度
                             data_size,  # 像素数据大小
                             1)  # 版本号

        # 获取像素数据
        pixel_data = img.tobytes()

        # 写入文件
        with open(mmap_path, 'wb') as f:
            f.write(header)  # 文件头
            f.write(pixel_data)  # 像素数据

        print(f"? 成功创建: {mmap_path}")
        print(f"   尺寸: {width}x{height}")
        print(f"   数据大小: {data_size} 字节")
        print(f"   文件头: {len(header)} 字节")

        # 验证文件格式
        verify_file_format(mmap_path, width, height, data_size)

        return True

    except Exception as e:
        print(f"? 错误: {e}")
        return False


def verify_file_format(mmap_path, expected_width, expected_height, expected_data_size):
    """验证生成的文件格式是否正确"""
    try:
        file_size = os.path.getsize(mmap_path)
        header_size = 16  # 4个uint32 = 16字节

        with open(mmap_path, 'rb') as f:
            # 读取文件头
            header = f.read(header_size)
            if len(header) != header_size:
                print("? 文件头大小不正确")
                return False

            # 解析文件头
            width, height, data_size, version = struct.unpack('<IIII', header)

            # 验证数据
            if width != expected_width or height != expected_height:
                print(f"? 尺寸不匹配: 预期{expected_width}x{expected_height}, 实际{width}x{height}")
                return False

            if data_size != expected_data_size:
                print(f"? 数据大小不匹配: 预期{expected_data_size}, 实际{data_size}")
                return False

            if file_size != header_size + data_size:
                print(f"? 文件总大小不匹配")
                return False

        print(f"? 文件格式验证通过")
        return True

    except Exception as e:
        print(f"? 验证错误: {e}")
        return False


if __name__ == "__main__":
    # 使用方法1: 命令行参数
    if len(sys.argv) == 3:
        create_compatible_mmap(sys.argv[1], sys.argv[2])

    # 使用方法2: 直接修改这里的路径运行
    else:
        # 在这里直接设置您的文件路径！
        input_image = "D:/Personal/zhankangming/Desktop/super_man2.png"  # 修改为您的图片路径
        output_bin = "D:/Personal/zhankangming/Desktop/asd.bin"  # 修改为您想要的输出路径

        success = create_compatible_mmap(input_image, output_bin)

        if success:
            print("\n? 文件创建成功！现在可以在C++代码中加载了。")

        # 等待用户按键退出（避免PyCharm窗口闪退）
        input("按回车键退出...")