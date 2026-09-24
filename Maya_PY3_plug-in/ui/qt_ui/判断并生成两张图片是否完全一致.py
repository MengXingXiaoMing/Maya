# coding=gbk
from PIL import Image
import numpy as np


def compare_images_with_transparent_diff(image1_path, image2_path, output_path="diff_transparent.png", threshold=10):
    """
    比较两张图片的像素差异，生成半透明差异图

    参数:
        image1_path: 第一张图片路径
        image2_path: 第二张图片路径
        output_path: 输出差异图路径
        threshold: 差异阈值，小于此值的差异将被忽略
    """
    try:
        # 加载图片并转换为RGBA模式（包含透明度通道）[1,3](@ref)
        img1 = Image.open(image1_path).convert('RGBA')
        img2 = Image.open(image2_path).convert('RGBA')

        # 调整图片尺寸一致
        if img1.size != img2.size:
            print(f"调整图片尺寸: {img1.size} → {img2.size}")
            img2 = img2.resize(img1.size)

        # 转换为numpy数组
        img1_arr = np.array(img1)
        img2_arr = np.array(img2)

        # 计算RGB通道的绝对差异[4](@ref)
        diff_rgb = np.abs(img1_arr[:, :, :3].astype(np.int16) - img2_arr[:, :, :3].astype(np.int16))

        # 计算总体差异（RGB三通道差异之和）
        diff_total = np.sum(diff_rgb, axis=2)

        # 创建差异掩码（标记有显著差异的像素）
        diff_mask = diff_total > threshold

        # 创建半透明差异图像
        # 初始化为全透明图像（RGBA，A=0）[5,7](@ref)
        diff_img = np.zeros((img1_arr.shape[0], img1_arr.shape[1], 4), dtype=np.uint8)

        # 设置透明度通道：有差异的区域不透明，无差异的区域透明
        alpha_channel = np.where(diff_mask, 255, 0).astype(np.uint8)

        # 计算差异颜色（放大差异以便观察）
        diff_color = np.minimum(diff_rgb, 255).astype(np.uint8)

        # 组合RGBA图像
        diff_img[:, :, :3] = diff_color  # RGB通道
        diff_img[:, :, 3] = alpha_channel  # Alpha通道

        # 转换为PIL图像并保存
        result_img = Image.fromarray(diff_img, 'RGBA')
        result_img.save(output_path, 'PNG')

        # 统计信息
        diff_pixels = np.sum(diff_mask)
        total_pixels = img1_arr.shape[0] * img1_arr.shape[1]

        print("=" * 60)
        print("图片差异比较结果")
        print("=" * 60)
        print(f"图片1: {image1_path} ({img1.size[0]}x{img1.size[1]})")
        print(f"图片2: {image2_path} ({img2.size[0]}x{img2.size[1]})")
        print(f"总像素数: {total_pixels}")
        print(f"有差异像素数: {diff_pixels}")
        print(f"差异比例: {diff_pixels / total_pixels * 100:.2f}%")
        print(f"差异阈值: {threshold}")
        print(f"输出文件: {output_path}")

        # 打印部分差异像素信息
        diff_coords = np.where(diff_mask)
        if len(diff_coords[0]) > 0:
            print("\n差异像素示例 (前10个):")
            print("坐标 (x,y) | 图片1 RGB | 图片2 RGB | 差异 RGB")
            print("-" * 50)

            for i in range(min(10, len(diff_coords[0]))):
                y, x = diff_coords[0][i], diff_coords[1][i]
                rgb1 = tuple(img1_arr[y, x, :3])
                rgb2 = tuple(img2_arr[y, x, :3])
                diff_rgb_val = tuple(diff_color[y, x])
                print(f"({x:3d},{y:3d}) | {rgb1} | {rgb2} | {diff_rgb_val}")

        print(f"\n半透明差异图已生成:")
        print(f"- 相同区域: 完全透明 (Alpha=0)")
        print(f"- 不同区域: 显示颜色差异 (Alpha=255)")
        # print(f"- 差异颜色已放大2倍以便观察")

        return {
            'total_pixels': total_pixels,
            'diff_pixels': diff_pixels,
            'diff_ratio': diff_pixels / total_pixels,
            'diff_image': result_img
        }

    except Exception as e:
        print(f"错误: {e}")
        return None


def create_side_by_side_comparison(image1_path, image2_path, diff_path, output_path="comparison.png"):
    """
    创建并排对比图，显示原图和差异图
    """
    try:
        img1 = Image.open(image1_path).convert('RGB')
        img2 = Image.open(image2_path).convert('RGB')
        diff = Image.open(diff_path)

        # 调整尺寸一致
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)

        # 创建对比图（原图1 | 原图2 | 差异图）
        width, height = img1.size
        comparison = Image.new('RGB', (width * 3, height), (240, 240, 240))

        comparison.paste(img1, (0, 0))
        comparison.paste(img2, (width, 0))

        # 将差异图转换为RGB用于显示（白色背景）
        diff_rgb = Image.new('RGB', diff.size, (255, 255, 255))
        diff_rgb.paste(diff, (0, 0), diff)  # 使用alpha通道作为掩码
        comparison.paste(diff_rgb, (width * 2, 0))

        comparison.save(output_path)
        print(f"\n对比图已保存: {output_path}")

    except Exception as e:
        print(f"创建对比图时出错: {e}")


# 使用示例
if __name__ == "__main__":
    # 替换为您的图片路径
    # 替换为你的图片路径
    image2 = r"D:\Personal\zhankangming\Desktop\新建文件夹 (39)\sadf.png"  # 第一张图片路径
    image1 = r"D:\Personal\zhankangming\Desktop\新建文件夹 (39)\sadfasdf.png"  # 第二张图片路径
    output = r"D:\Personal\zhankangming\Desktop\新建文件夹 (39)\aaaa.png"  # 差异图输出路径

    # 比较图片并生成半透明差异图
    result = compare_images_with_transparent_diff(image1, image2, output, threshold=20)

    if result:
        # 创建并排对比图
        create_side_by_side_comparison(image1, image2, output, "comparison_result.png")

        print("\n操作完成！")
        print(f"差异检测完成，{result['diff_pixels']}个像素有差异")
        print(f"请查看 {output} 查看半透明差异效果")

