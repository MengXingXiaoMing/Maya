import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# 使用您提供的精确数据
input_points = np.array([
    [50.0, 50.0, 50.0],
    [130.06, 53.06, 95.06],
    [35.06, 133.06, 45.06],
    [70.06, 133.06, 95.06],
    [38.06, 63.06, 91.06]
])

target_point = np.array([50, 50, 50])

# 计算每个点的欧几里得范数作为目标值
target_values = np.linalg.norm(input_points, axis=1)
target_norm = np.linalg.norm(target_point)


class UserDataRBFVisualizer:
    """基于用户数据的RBF可视化工具"""

    def __init__(self):
        self.output_dir = "user_data_rbf_fitting_results"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def print_reference_point_weights(self):
        """打印参考点对固定点的权重"""
        print("=" * 60)
        print("参考点对固定点的权重计算")
        print("=" * 60)

        # 使用输入点作为RBF中心
        centers = input_points
        sigma = 100.0  # RBF宽度参数

        # 计算目标点到每个参考点的距离
        distances = []
        for center in centers:
            dist = np.linalg.norm(target_point - center)
            distances.append(dist)

        # 计算RBF值（相似度）
        rbf_values = np.exp(-np.array(distances) ** 2 / (2 * sigma ** 2))

        # 归一化得到权重
        weights = rbf_values / np.sum(rbf_values)

        # 打印结果
        print("参考点（输入点）对固定点（目标点）的权重：")
        for i, (point, weight, dist, rbf_val) in enumerate(zip(input_points, weights, distances, rbf_values)):
            print(f"参考点{i + 1}: [{point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f}]")
            print(f"  到固定点的距离: {dist:.2f}")
            print(f"  RBF相似度值: {rbf_val:.6f}")
            print(f"  归一化权重: {weight:.6f}")
            print()

        # 可视化权重分布
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('参考点对固定点的权重分布', fontsize=16)

        # 1. 权重柱状图
        ax1 = fig.add_subplot(221)
        bars = ax1.bar(range(len(weights)), weights,
                       color=['red', 'blue', 'green', 'orange', 'purple'])
        ax1.set_xlabel('参考点编号')
        ax1.set_ylabel('权重值')
        ax1.set_title('各参考点对固定点的权重')
        ax1.set_xticks(range(len(weights)))
        ax1.set_xticklabels([f'点{i + 1}' for i in range(len(weights))])
        ax1.grid(True, alpha=0.3)

        # 添加权重数值
        for i, (bar, weight) in enumerate(zip(bars, weights)):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                     f'{weight:.4f}', ha='center', va='bottom', fontweight='bold')
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                     f'距离: {distances[i]:.1f}', ha='center', va='center', color='white')

        # 2. 距离与权重关系图
        ax2 = fig.add_subplot(222)
        ax2.scatter(distances, weights, s=100, c=range(len(weights)), cmap='viridis')
        ax2.set_xlabel('到固定点的距离')
        ax2.set_ylabel('权重值')
        ax2.set_title('距离与权重关系')
        ax2.grid(True, alpha=0.3)

        # 添加点标签
        for i, (dist, weight) in enumerate(zip(distances, weights)):
            ax2.annotate(f'点{i + 1}', (dist, weight), xytext=(5, 5),
                         textcoords='offset points', fontsize=8)

        # 3. RBF相似度值
        ax3 = fig.add_subplot(223)
        bars_rbf = ax3.bar(range(len(rbf_values)), rbf_values,
                           color=['red', 'blue', 'green', 'orange', 'purple'])
        ax3.set_xlabel('参考点编号')
        ax3.set_ylabel('RBF相似度值')
        ax3.set_title('RBF函数计算的相似度')
        ax3.set_xticks(range(len(rbf_values)))
        ax3.set_xticklabels([f'点{i + 1}' for i in range(len(rbf_values))])
        ax3.grid(True, alpha=0.3)

        for i, (bar, rbf_val) in enumerate(zip(bars_rbf, rbf_values)):
            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
                     f'{rbf_val:.4f}', ha='center', va='bottom', fontweight='bold')

        # 4. 权重贡献百分比
        ax4 = fig.add_subplot(224)
        wedges, texts, autotexts = ax4.pie(weights, labels=[f'点{i + 1}' for i in range(len(weights))],
                                           autopct='%1.1f%%', startangle=90)
        ax4.set_title('权重贡献百分比')

        plt.tight_layout()
        return fig, weights

    def visualize_data_points_with_labels(self):
        """可视化带标签的3D数据点"""
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('用户提供的3D数据点详细标记', fontsize=18)

        # 1. 3D散点图 - 详细标记
        ax1 = fig.add_subplot(221, projection='3d')
        colors = ['red', 'blue', 'green', 'orange', 'purple']

        # 绘制用户数据点并添加详细标签
        for i, (point, color) in enumerate(zip(input_points, colors)):
            ax1.scatter(point[0], point[1], point[2],
                        c=color, s=200, alpha=0.8)

            # 添加详细坐标标签
            label_text = f'点{i + 1}\nX:{point[0]:.2f}\nY:{point[1]:.2f}\nZ:{point[2]:.2f}\n范数:{target_values[i]:.2f}'
            ax1.text(point[0], point[1], point[2], label_text,
                     fontsize=8, ha='center', va='bottom',
                     bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7))

        # 绘制目标点
        ax1.scatter(target_point[0], target_point[1], target_point[2],
                    c='black', s=300, marker='*', alpha=1.0)

        # 添加目标点标签
        target_label = f'目标点\nX:{target_point[0]}\nY:{target_point[1]}\nZ:{target_point[2]}\n范数:{target_norm:.2f}'
        ax1.text(target_point[0], target_point[1], target_point[2], target_label,
                 fontsize=8, ha='center', va='bottom',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))

        ax1.set_xlabel('X轴')
        ax1.set_ylabel('Y轴')
        ax1.set_zlabel('Z轴')
        ax1.set_title('3D数据点分布（带详细坐标标记）')

        # 2. 数据点坐标表格
        ax2 = fig.add_subplot(222)
        ax2.axis('off')

        # 创建坐标表格
        table_data = []
        headers = ['点编号', 'X坐标', 'Y坐标', 'Z坐标', '范数值']

        for i, point in enumerate(input_points):
            table_data.append([f'点{i + 1}', f'{point[0]:.2f}', f'{point[1]:.2f}',
                               f'{point[2]:.2f}', f'{target_values[i]:.2f}'])

        table_data.append(['目标点', f'{target_point[0]}', f'{target_point[1]}',
                           f'{target_point[2]}', f'{target_norm:.2f}'])

        table = ax2.table(cellText=table_data, colLabels=headers,
                          loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)

        ax2.set_title('数据点坐标详细表格')

        # 3. 范数值对比柱状图
        ax3 = fig.add_subplot(223)
        point_labels = [f'点{i + 1}' for i in range(len(input_points))]
        point_labels.append('目标点')

        norms = list(target_values)
        norms.append(target_norm)

        bars = ax3.bar(range(len(norms)), norms,
                       color=['red', 'blue', 'green', 'orange', 'purple', 'black'])

        ax3.set_xlabel('数据点')
        ax3.set_ylabel('欧几里得范数')
        ax3.set_title('各点范数值对比')
        ax3.set_xticks(range(len(norms)))
        ax3.set_xticklabels(point_labels, rotation=45)
        ax3.grid(True, alpha=0.3)

        # 添加详细数值标签
        for i, (bar, norm) in enumerate(zip(bars, norms)):
            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                     f'{norm:.2f}', ha='center', va='bottom', fontweight='bold')

        # 4. 数据分布热力图
        ax4 = fig.add_subplot(224)

        # 计算各坐标轴的范围和分布
        coordinates = np.vstack([input_points, target_point])
        coordinate_ranges = []

        for dim in range(3):
            dim_values = coordinates[:, dim]
            coordinate_ranges.append([dim_values.min(), dim_values.max(),
                                      dim_values.mean(), dim_values.std()])

        # 创建热力图显示数据分布
        heatmap_data = np.array(coordinate_ranges)
        im = ax4.imshow(heatmap_data, cmap='viridis', aspect='auto')

        ax4.set_xticks(range(4))
        ax4.set_xticklabels(['最小值', '最大值', '平均值', '标准差'])
        ax4.set_yticks(range(3))
        ax4.set_yticklabels(['X轴', 'Y轴', 'Z轴'])
        ax4.set_title('各坐标轴数据分布统计')

        # 添加数值标注
        for i in range(3):
            for j in range(4):
                ax4.text(j, i, f'{heatmap_data[i, j]:.2f}',
                         ha='center', va='center', color='white', fontweight='bold')

        plt.colorbar(im, ax=ax4)

        plt.tight_layout()
        return fig

    def visualize_rbf_fitting_process(self):
        """可视化RBF拟合过程"""
        # 数据标准化
        scaler_X = StandardScaler()
        scaler_y = StandardScaler()

        X_scaled = scaler_X.fit_transform(input_points)
        y_scaled = scaler_y.fit_transform(target_values.reshape(-1, 1)).flatten()

        # 使用K-means确定RBF中心
        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(X_scaled)
        rbf_centers_scaled = kmeans.cluster_centers_

        # 反标准化得到原始尺度下的中心
        rbf_centers = scaler_X.inverse_transform(rbf_centers_scaled)

        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('RBF神经网络拟合过程详解', fontsize=18)

        # 1. RBF中心分布
        ax1 = fig.add_subplot(231, projection='3d')
        colors = ['red', 'blue', 'green', 'orange', 'purple']

        # 绘制原始数据点
        for i, (point, color) in enumerate(zip(input_points, colors)):
            ax1.scatter(point[0], point[1], point[2],
                        c=color, s=150, alpha=0.7, label=f'点{i + 1}')

        # 绘制RBF中心点
        center_colors = ['cyan', 'magenta', 'yellow']
        for i, (center, color) in enumerate(zip(rbf_centers, center_colors)):
            ax1.scatter(center[0], center[1], center[2],
                        c=color, s=300, marker='^', label=f'RBF中心{i + 1}')

            # 添加中心点标签
            center_label = f'中心{i + 1}\nX:{center[0]:.2f}\nY:{center[1]:.2f}\nZ:{center[2]:.2f}'
            ax1.text(center[0], center[1], center[2], center_label,
                     fontsize=8, ha='center', va='bottom')

        # 绘制目标点
        ax1.scatter(target_point[0], target_point[1], target_point[2],
                    c='black', s=300, marker='*', label='目标点')

        ax1.set_xlabel('X轴')
        ax1.set_ylabel('Y轴')
        ax1.set_zlabel('Z轴')
        ax1.set_title('RBF中心点分布')
        ax1.legend()

        # 2. 点到中心的距离计算
        ax2 = fig.add_subplot(232)

        # 计算每个点到各个RBF中心的距离
        distances = np.zeros((len(input_points), len(rbf_centers)))
        for i, point in enumerate(input_points):
            for j, center in enumerate(rbf_centers):
                distances[i, j] = np.linalg.norm(point - center)

        # 绘制距离热力图
        im = ax2.imshow(distances, cmap='YlOrRd', aspect='auto')

        ax2.set_xlabel('RBF中心')
        ax2.set_ylabel('数据点')
        ax2.set_title('数据点到RBF中心的距离')
        ax2.set_xticks(range(len(rbf_centers)))
        ax2.set_xticklabels([f'中心{i + 1}' for i in range(len(rbf_centers))])
        ax2.set_yticks(range(len(input_points)))
        ax2.set_yticklabels([f'点{i + 1}' for i in range(len(input_points))])

        # 添加距离数值
        for i in range(len(input_points)):
            for j in range(len(rbf_centers)):
                ax2.text(j, i, f'{distances[i, j]:.1f}',
                         ha='center', va='center', color='black', fontweight='bold')

        plt.colorbar(im, ax=ax2)

        # 3. RBF函数值计算
        ax3 = fig.add_subplot(233)

        sigma = 100.0  # RBF宽度参数
        rbf_values = np.exp(-distances ** 2 / (2 * sigma ** 2))

        im = ax3.imshow(rbf_values, cmap='viridis', aspect='auto')

        ax3.set_xlabel('RBF中心')
        ax3.set_ylabel('数据点')
        ax3.set_title('RBF函数激活值')
        ax3.set_xticks(range(len(rbf_centers)))
        ax3.set_xticklabels([f'中心{i + 1}' for i in range(len(rbf_centers))])
        ax3.set_yticks(range(len(input_points)))
        ax3.set_yticklabels([f'点{i + 1}' for i in range(len(input_points))])

        # 添加RBF值
        for i in range(len(input_points)):
            for j in range(len(rbf_centers)):
                ax3.text(j, i, f'{rbf_values[i, j]:.3f}',
                         ha='center', va='center', color='white', fontweight='bold')

        plt.colorbar(im, ax=ax3)

        # 4. 权重计算和预测
        ax4 = fig.add_subplot(234)

        # 简化的权重计算（实际应该用最小二乘法）
        # 这里用RBF值加权平均作为示意
        weights = rbf_values / np.sum(rbf_values, axis=1, keepdims=True)

        # 计算预测值
        predicted_values = np.sum(weights * target_values.reshape(-1, 1), axis=1)

        # 绘制真实值 vs 预测值
        points_range = range(len(input_points))
        ax4.bar([x - 0.2 for x in points_range], target_values,
                width=0.4, label='真实范数值', alpha=0.7)
        ax4.bar([x + 0.2 for x in points_range], predicted_values,
                width=0.4, label='预测范数值', alpha=0.7)

        ax4.set_xlabel('数据点')
        ax4.set_ylabel('范数值')
        ax4.set_title('RBF预测结果对比')
        ax4.set_xticks(points_range)
        ax4.set_xticklabels([f'点{i + 1}' for i in points_range])
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        # 5. 预测误差分析
        ax5 = fig.add_subplot(235)

        errors = np.abs(target_values - predicted_values)
        bars = ax5.bar(range(len(errors)), errors,
                       color=['red', 'blue', 'green', 'orange', 'purple'])

        ax5.set_xlabel('数据点')
        ax5.set_ylabel('绝对误差')
        ax5.set_title('预测误差分析')
        ax5.set_xticks(range(len(errors)))
        ax5.set_xticklabels([f'点{i + 1}' for i in range(len(errors))])
        ax5.grid(True, alpha=0.3)

        # 添加误差数值
        for i, (bar, error) in enumerate(zip(bars, errors)):
            ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     f'{error:.2f}', ha='center', va='bottom')

        # 6. 目标点预测
        ax6 = fig.add_subplot(236)

        # 计算目标点到RBF中心的距离
        target_distances = []
        for center in rbf_centers:
            target_distances.append(np.linalg.norm(target_point - center))

        target_distances = np.array(target_distances)
        target_rbf = np.exp(-target_distances ** 2 / (2 * sigma ** 2))

        # 计算目标点预测值
        target_weights = target_rbf / np.sum(target_rbf)
        target_predicted = np.sum(target_weights * target_values[:len(target_weights)])

        # 绘制目标点预测结果
        comparison_data = [target_norm, target_predicted]
        comparison_labels = ['实际范数', '预测范数']
        bars = ax6.bar(comparison_labels, comparison_data,
                       color=['darkblue', 'darkred'])

        ax6.set_ylabel('范数值')
        ax6.set_title('目标点[1,2,3]预测结果')
        ax6.grid(True, alpha=0.3)

        # 添加数值标签
        for bar, value in zip(bars, comparison_data):
            ax6.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

        plt.tight_layout()
        return fig

    def create_comprehensive_summary(self):
        """创建综合总结图表"""
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('RBF拟合综合分析总结', fontsize=16)

        # 1. 数据统计摘要
        ax1 = fig.add_subplot(221)
        ax1.axis('off')

        summary_text = "数据统计摘要:\n\n"
        summary_text += f"数据点数量: {len(input_points)}\n"
        summary_text += f"目标点坐标: [{target_point[0]}, {target_point[1]}, {target_point[2]}]\n\n"

        summary_text += "各坐标轴统计:\n"
        for dim, name in enumerate(['X', 'Y', 'Z']):
            values = input_points[:, dim]
            summary_text += f"{name}轴: 最小值={values.min():.2f}, 最大值={values.max():.2f}, "
            summary_text += f"平均值={values.mean():.2f}\n"

        summary_text += f"\n范数统计:\n"
        summary_text += f"最小范数: {target_values.min():.2f}\n"
        summary_text += f"最大范数: {target_values.max():.2f}\n"
        summary_text += f"平均范数: {target_values.mean():.2f}\n"
        summary_text += f"目标点范数: {target_norm:.2f}"

        ax1.text(0.1, 0.9, summary_text, transform=ax1.transAxes,
                 fontsize=10, va='top', linespacing=1.5,
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7))
        ax1.set_title('数据统计摘要')

        # 2. RBF参数设置
        ax2 = fig.add_subplot(222)
        ax2.axis('off')

        rbf_text = "RBF网络参数:\n\n"
        rbf_text += "网络结构:\n"
        rbf_text += f"- 输入维度: 3 (X,Y,Z坐标)\n"
        rbf_text += f"- 输出维度: 1 (范数值)\n"
        rbf_text += f"- RBF中心数量: 3\n"
        rbf_text += f"- RBF宽度参数(σ): 100.0\n\n"

        rbf_text += "训练数据:\n"
        rbf_text += f"- 训练样本数: {len(input_points)}\n"
        rbf_text += f"- 验证样本数: 1 (目标点)\n\n"

        rbf_text += "算法特点:\n"
        rbf_text += "- 使用K-means确定RBF中心\n"
        rbf_text += "- 高斯径向基函数\n"
        rbf_text += "- 加权平均预测"

        ax2.text(0.1, 0.9, rbf_text, transform=ax2.transAxes,
                 fontsize=10, va='top', linespacing=1.5,
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.7))
        ax2.set_title('RBF网络参数')

        # 3. 性能评估
        ax3 = fig.add_subplot(223)

        # 计算简单预测误差（示意）
        mean_prediction = target_values.mean()
        mean_error = abs(target_norm - mean_prediction)

        metrics = [mean_error, target_norm, mean_prediction]
        metric_labels = ['平均误差', '实际值', '基准预测']
        colors = ['red', 'blue', 'green']

        bars = ax3.bar(metric_labels, metrics, color=colors)
        ax3.set_ylabel('范数值')
        ax3.set_title('性能评估指标')
        ax3.grid(True, alpha=0.3)

        for bar, value in zip(bars, metrics):
            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     f'{value:.2f}', ha='center', va='bottom')

        # 4. 应用建议
        ax4 = fig.add_subplot(224)
        ax4.axis('off')

        advice_text = "应用建议:\n\n"
        advice_text += "✓ 数据预处理: 建议对坐标进行标准化\n"
        advice_text += "✓ 参数调优: 可调整RBF中心数量和σ参数\n"
        advice_text += "✓ 模型验证: 增加验证集评估泛化能力\n"
        advice_text += "✓ 特征工程: 可考虑添加其他几何特征\n"
        advice_text += "✓ 算法选择: 对于小数据集，RBF网络效果良好\n\n"

        advice_text += "扩展应用:\n"
        advice_text += "- 三维空间点分类\n"
        advice_text += "- 距离预测模型\n"
        advice_text += "- 空间插值计算"

        ax4.text(0.1, 0.9, advice_text, transform=ax4.transAxes,
                 fontsize=10, va='top', linespacing=1.5,
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.7))
        ax4.set_title('应用建议')

        plt.tight_layout()
        return fig


def main():
    """生成基于用户数据的RBF拟合图解"""
    visualizer = UserDataRBFVisualizer()

    # 显示数据信息
    print("=" * 60)
    print("基于用户数据的RBF拟合图解")
    print("=" * 60)
    print("用户提供的数据点:")
    for i, point in enumerate(input_points):
        norm = target_values[i]
        print(f"  点{i + 1}: [{point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f}] → 范数: {norm:.2f}")

    print(f"目标点: [{target_point[0]}, {target_point[1]}, {target_point[2]}] → 范数: {target_norm:.2f}")
    print()

    # 获取当前工作目录
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    print(f"图片将保存到: {os.path.join(current_dir, visualizer.output_dir)}")
    print()

    # 1. 打印参考点对固定点的权重
    weights_fig, weights = visualizer.print_reference_point_weights()
    filename_weights = os.path.join(visualizer.output_dir, "reference_point_weights.png")
    weights_fig.savefig(filename_weights, dpi=300, bbox_inches='tight')
    plt.close(weights_fig)
    print(f"参考点权重图已保存: {os.path.abspath(filename_weights)}")
    print()

    # 2. 数据点详细标记可视化
    fig1 = visualizer.visualize_data_points_with_labels()
    filename1 = os.path.join(visualizer.output_dir, "data_points_detailed.png")
    fig1.savefig(filename1, dpi=300, bbox_inches='tight')
    plt.close(fig1)
    print(f"数据点详细标记图已保存: {os.path.abspath(filename1)}")

    # 3. RBF拟合过程可视化
    fig2 = visualizer.visualize_rbf_fitting_process()
    filename2 = os.path.join(visualizer.output_dir, "rbf_fitting_process.png")
    fig2.savefig(filename2, dpi=300, bbox_inches='tight')
    plt.close(fig2)
    print(f"RBF拟合过程图已保存: {os.path.abspath(filename2)}")

    # 4. 综合分析总结
    fig3 = visualizer.create_comprehensive_summary()
    filename3 = os.path.join(visualizer.output_dir, "comprehensive_analysis.png")
    fig3.savefig(filename3, dpi=300, bbox_inches='tight')
    plt.close(fig3)
    print(f"综合分析总结图已保存: {os.path.abspath(filename3)}")

    print("\n所有图解已生成完成！")
    print("图片完整路径列表:")
    print(f"1. {os.path.abspath(filename_weights)}")
    print(f"2. {os.path.abspath(filename1)}")
    print(f"3. {os.path.abspath(filename2)}")
    print(f"4. {os.path.abspath(filename3)}")

    return [os.path.abspath(filename_weights), os.path.abspath(filename1),
            os.path.abspath(filename2), os.path.abspath(filename3)]


if __name__ == "__main__":
    # 运行主程序
    image_paths = main()

    # 显示最终总结
    print("\n" + "=" * 60)
    print("RBF拟合图解生成总结")
    print("=" * 60)
    print(f"所有图片已保存到以下完整路径:")
    for i, path in enumerate(image_paths, 1):
        print(f"{i}. {path}")

    print(f"\n您可以在文件资源管理器中打开以下文件夹查看图片:")
    print(f"{os.path.abspath('user_data_rbf_fitting_results')}")
