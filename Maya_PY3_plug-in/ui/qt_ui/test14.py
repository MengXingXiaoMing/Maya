# -*- coding: utf-8 -*-
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
    [59.0, 59.0, 59.0],
    [130.06, 53.06, 95.06],
    [35.06, 133.06, 45.06],
    [70.06, 133.06, 95.06],
    [38.06, 63.06, 91.06]
])

target_point = np.array([50, 50, 50])

# 计算每个点的欧几里得范数作为目标值
target_values = np.linalg.norm(input_points, axis=1)
target_norm = np.linalg.norm(target_point)


class RBFWeightOptimizer:
    """RBF权重优化器"""

    def __init__(self, top_k=3, amplification_factor=2.0):
        self.top_k = top_k
        self.amplification_factor = amplification_factor

    def optimize_weights(self, weights):
        """
        优化权重：只保留最大的k个权重，权重和为1，大权重占比更大

        参数:
        weights: 原始权重数组

        返回:
        optimized_weights: 优化后的权重数组
        important_indices: 重要权重的索引
        """
        if len(weights) <= self.top_k:
            # 如果权重数量本来就少于或等于k，直接使用所有权重
            important_indices = np.arange(len(weights))
            selected_weights = weights.copy()
        else:
            # 获取最大的k个权重的索引
            important_indices = np.argpartition(weights, -self.top_k)[-self.top_k:]
            selected_weights = weights[important_indices]

        # 权重放大处理：越接近1的权重放大效果越明显
        amplified_weights = np.power(selected_weights, self.amplification_factor)

        # 归一化处理，确保权重和为1
        normalized_weights = amplified_weights / np.sum(amplified_weights)

        # 创建完整的权重数组（非重要权重设为0）
        final_weights = np.zeros_like(weights)
        final_weights[important_indices] = normalized_weights

        return final_weights, important_indices


class EnhancedRBFVisualizer:
    """增强的RBF可视化工具（包含权重优化）"""

    def __init__(self):
        self.output_dir = "enhanced_rbf_results"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.weight_optimizer = RBFWeightOptimizer(top_k=3, amplification_factor=2.0)

    def calculate_original_weights(self):
        """计算原始RBF权重"""
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

        # 归一化得到原始权重
        original_weights = rbf_values / np.sum(rbf_values)

        return original_weights, distances, rbf_values

    def optimize_and_analyze_weights(self):
        """优化并分析权重"""
        # 计算原始权重
        original_weights, distances, rbf_values = self.calculate_original_weights()

        # 优化权重
        optimized_weights, important_indices = self.weight_optimizer.optimize_weights(original_weights)

        # 打印分析结果
        print("=" * 60)
        print("RBF权重优化分析")
        print("=" * 60)
        print(f"优化参数: 保留最大的 {self.weight_optimizer.top_k} 个权重, 放大因子: {self.weight_optimizer.amplification_factor}")
        print()

        print("原始权重分析:")
        for i, (weight, dist, rbf_val) in enumerate(zip(original_weights, distances, rbf_values)):
            status = "重要" if i in important_indices else "非重要"
            print(f"权重{i + 1}: {weight:.6f} (距离: {dist:.2f}, RBF值: {rbf_val:.6f}) [{status}]")
        print(f"原始权重和: {np.sum(original_weights):.6f}")
        print()

        print("优化后权重分析:")
        for i, weight in enumerate(optimized_weights):
            status = "重要" if i in important_indices else "非重要"
            if weight > 0:
                change_ratio = weight / original_weights[i] if original_weights[i] > 0 else float('inf')
                print(f"权重{i + 1}: {weight:.6f} (变化比率: {change_ratio:.2f}) [{status}]")
            else:
                print(f"权重{i + 1}: {weight:.6f} [被置零]")
        print(f"优化后权重和: {np.sum(optimized_weights):.6f}")
        print()

        return original_weights, optimized_weights, important_indices, distances, rbf_values

    def visualize_weight_optimization(self):
        """可视化权重优化过程"""
        # 获取权重数据
        original_weights, optimized_weights, important_indices, distances, rbf_values = self.optimize_and_analyze_weights()

        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('RBF权重优化过程可视化', fontsize=16)

        # 1. 原始权重分布
        ax1 = plt.subplot(2, 3, 1)
        bars1 = ax1.bar(range(len(original_weights)), original_weights,
                        color=['lightblue'] * len(original_weights), alpha=0.7)
        # 标记重要权重
        for idx in important_indices:
            bars1[idx].set_color('red')

        ax1.set_xlabel('权重索引')
        ax1.set_ylabel('权重值')
        ax1.set_title('原始权重分布')
        ax1.set_xticks(range(len(original_weights)))
        ax1.set_xticklabels([f'W{i + 1}' for i in range(len(original_weights))])
        ax1.grid(True, alpha=0.3)

        # 添加数值标签
        for i, (bar, weight) in enumerate(zip(bars1, original_weights)):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                     f'{weight:.4f}', ha='center', va='bottom', fontsize=8)
            if i in important_indices:
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                         '重要', ha='center', va='center', color='white', fontweight='bold')

        # 2. 优化后权重分布
        ax2 = plt.subplot(2, 3, 2)
        bars2 = ax2.bar(range(len(optimized_weights)), optimized_weights,
                        color=['lightgray'] * len(optimized_weights), alpha=0.7)
        # 标记重要权重
        for idx in important_indices:
            bars2[idx].set_color('green')

        ax2.set_xlabel('权重索引')
        ax2.set_ylabel('权重值')
        ax2.set_title('优化后权重分布')
        ax2.set_xticks(range(len(optimized_weights)))
        ax2.set_xticklabels([f'W{i + 1}' for i in range(len(optimized_weights))])
        ax2.grid(True, alpha=0.3)

        # 添加数值标签
        for i, (bar, weight) in enumerate(zip(bars2, optimized_weights)):
            if weight > 0:
                ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                         f'{weight:.4f}', ha='center', va='bottom', fontsize=8)
                if i in important_indices:
                    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                             '保留', ha='center', va='center', color='white', fontweight='bold')

        # 3. 权重变化对比
        ax3 = plt.subplot(2, 3, 3)
        x_pos = np.arange(len(original_weights))
        width = 0.35

        bars3_orig = ax3.bar(x_pos - width / 2, original_weights, width,
                             label='原始权重', alpha=0.7, color='lightblue')
        bars3_opt = ax3.bar(x_pos + width / 2, optimized_weights, width,
                            label='优化权重', alpha=0.7, color='lightgreen')

        # 标记重要权重区域
        for idx in important_indices:
            ax3.axvspan(idx - width, idx + width, alpha=0.2, color='yellow')

        ax3.set_xlabel('权重索引')
        ax3.set_ylabel('权重值')
        ax3.set_title('权重优化前后对比')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels([f'W{i + 1}' for i in range(len(original_weights))])
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. 距离与权重关系
        ax4 = plt.subplot(2, 3, 4)

        # 创建颜色映射：红色表示重要权重，蓝色表示非重要权重
        colors = ['red' if i in important_indices else 'blue' for i in range(len(distances))]
        sizes = [100 if i in important_indices else 50 for i in range(len(distances))]

        scatter = ax4.scatter(distances, original_weights, c=colors, s=sizes, alpha=0.7)
        ax4.set_xlabel('到目标点的距离')
        ax4.set_ylabel('原始权重值')
        ax4.set_title('距离与权重关系（红色为重要权重）')
        ax4.grid(True, alpha=0.3)

        # 添加点标签
        for i, (dist, weight) in enumerate(zip(distances, original_weights)):
            ax4.annotate(f'W{i + 1}', (dist, weight), xytext=(5, 5),
                         textcoords='offset points', fontsize=8)

        # 5. 权重放大效果
        ax5 = plt.subplot(2, 3, 5)

        # 只显示重要权重的放大效果
        important_original = original_weights[important_indices]
        important_optimized = optimized_weights[important_indices]

        x_pos_important = np.arange(len(important_indices))
        bars5_orig = ax5.bar(x_pos_important - 0.2, important_original, 0.4,
                             label='原始权重', alpha=0.7, color='lightblue')
        bars5_opt = ax5.bar(x_pos_important + 0.2, important_optimized, 0.4,
                            label='优化权重', alpha=0.7, color='lightgreen')

        ax5.set_xlabel('重要权重索引')
        ax5.set_ylabel('权重值')
        ax5.set_title('重要权重放大效果')
        ax5.set_xticks(x_pos_important)
        ax5.set_xticklabels([f'W{i + 1}' for i in important_indices])
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        # 添加数值标签和变化比率
        for i, (orig, opt) in enumerate(zip(important_original, important_optimized)):
            change_ratio = opt / orig
            ax5.text(x_pos_important[i], max(orig, opt) + 0.05,
                     f'×{change_ratio:.2f}', ha='center', va='bottom', fontweight='bold')

        # 6. 权重稀疏性分析
        ax6 = plt.subplot(2, 3, 6)

        # 计算稀疏度指标
        sparsity_metrics = {
            '非零权重比例': np.sum(original_weights > 0) / len(original_weights),
            '优化后非零权重比例': np.sum(optimized_weights > 0) / len(optimized_weights),
            '权重集中度': np.sum(original_weights ** 2),  # Gini系数简化
            '优化后权重集中度': np.sum(optimized_weights ** 2)
        }

        metrics_names = list(sparsity_metrics.keys())
        metrics_values = list(sparsity_metrics.values())

        bars6 = ax6.bar(metrics_names, metrics_values,
                        color=['lightblue', 'lightgreen', 'lightcoral', 'lightyellow'])
        ax6.set_ylabel('指标值')
        ax6.set_title('权重稀疏性分析')
        ax6.tick_params(axis='x', rotation=45)
        ax6.grid(True, alpha=0.3)

        # 添加数值标签
        for bar, value in zip(bars6, metrics_values):
            ax6.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                     f'{value:.3f}', ha='center', va='bottom')

        plt.tight_layout()
        return fig

    def visualize_3d_weight_analysis(self):
        """3D权重分析可视化"""
        original_weights, optimized_weights, important_indices, distances, rbf_values = self.optimize_and_analyze_weights()

        fig = plt.figure(figsize=(18, 6))

        # 1. 3D权重分布
        ax1 = fig.add_subplot(131, projection='3d')

        # 绘制数据点和权重
        for i, point in enumerate(input_points):
            color = 'red' if i in important_indices else 'blue'
            size = 200 if i in important_indices else 100
            alpha = 1.0 if i in important_indices else 0.6

            # 原始权重大小
            ax1.scatter(point[0], point[1], point[2],
                        s=size * original_weights[i] * 10, c=color, alpha=alpha,
                        label=f'点{i + 1}' if i in important_indices else "")

            # 添加标签
            label = f'点{i + 1}\n原始权重:{original_weights[i]:.3f}'
            if i in important_indices:
                label += f'\n优化权重:{optimized_weights[i]:.3f}'
            ax1.text(point[0], point[1], point[2], label, fontsize=8)

        # 绘制目标点
        ax1.scatter(target_point[0], target_point[1], target_point[2],
                    s=300, c='black', marker='*', label='目标点')

        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('3D数据点与权重分布（球体大小表示权重）')
        ax1.legend()

        # 2. 优化后权重分布
        ax2 = fig.add_subplot(132, projection='3d')

        for i, point in enumerate(input_points):
            if i in important_indices:  # 只显示重要权重
                color = 'green'
                size = 200

                ax2.scatter(point[0], point[1], point[2],
                            s=size * optimized_weights[i] * 10, c=color, alpha=1.0,
                            label=f'点{i + 1}')

                # 添加标签
                label = f'点{i + 1}\n优化权重:{optimized_weights[i]:.3f}'
                ax2.text(point[0], point[1], point[2], label, fontsize=8)

        # 绘制目标点
        ax2.scatter(target_point[0], target_point[1], target_point[2],
                    s=300, c='black', marker='*', label='目标点')

        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title('优化后权重分布（仅显示重要权重）')
        ax2.legend()

        # 3. 权重变化轨迹
        ax3 = fig.add_subplot(133, projection='3d')

        for i, point in enumerate(input_points):
            if i in important_indices:
                # 绘制从原始权重到优化权重的轨迹
                ax3.plot([point[0], point[0]], [point[1], point[1]], [point[2], point[2]],
                         'gray', alpha=0.3)

                # 原始权重点
                ax3.scatter(point[0], point[1], point[2],
                            s=100 * original_weights[i] * 10, c='red', alpha=0.7,
                            marker='o', label=f'原始' if i == important_indices[0] else "")

                # 优化权重点
                ax3.scatter(point[0], point[1], point[2],
                            s=100 * optimized_weights[i] * 10, c='green', alpha=0.7,
                            marker='^', label=f'优化' if i == important_indices[0] else "")

        ax3.set_xlabel('X')
        ax3.set_ylabel('Y')
        ax3.set_zlabel('Z')
        ax3.set_title('权重优化轨迹（圆形→三角形）')
        ax3.legend()

        plt.tight_layout()
        return fig

    def create_summary_report(self):
        """创建权重优化总结报告"""
        original_weights, optimized_weights, important_indices, distances, rbf_values = self.optimize_and_analyze_weights()

        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('RBF权重优化总结报告', fontsize=16)

        # 关闭坐标轴
        ax = plt.subplot(111)
        ax.axis('off')

        # 创建报告文本
        report_text = "RBF权重优化总结报告\n\n"
        report_text += "=" * 50 + "\n\n"

        report_text += "优化参数设置:\n"
        report_text += f"- 保留权重数量: {self.weight_optimizer.top_k}\n"
        report_text += f"- 放大因子: {self.weight_optimizer.amplification_factor}\n\n"

        report_text += "重要权重统计:\n"
        for idx in important_indices:
            orig = original_weights[idx]
            opt = optimized_weights[idx]
            change = opt - orig
            change_pct = (change / orig) * 100 if orig > 0 else 0
            report_text += f"- 权重{idx + 1}: {orig:.4f} → {opt:.4f} (变化: {change:+.4f}, {change_pct:+.1f}%)\n"
        report_text += f"\n权重集中度提升: {np.sum(optimized_weights ** 2) - np.sum(original_weights ** 2):.4f}\n"
        report_text += f"稀疏度: {len(important_indices)}/{len(original_weights)} 个非零权重\n\n"

        report_text += "优化效果评估:\n"
        total_important_weight_orig = np.sum(original_weights[important_indices])
        total_important_weight_opt = np.sum(optimized_weights[important_indices])
        report_text += f"- 重要权重占比: {total_important_weight_orig:.1%} → {total_important_weight_opt:.1%}\n"
        report_text += f"- 权重方差: {np.var(original_weights):.6f} → {np.var(optimized_weights):.6f}\n"
        report_text += f"- 最大权重: {np.max(original_weights):.4f} → {np.max(optimized_weights):.4f}\n\n"

        report_text += "应用建议:\n"
        report_text += "✓ 模型复杂度降低，仅保留最重要的特征\n"
        report_text += "✓ 大权重获得更大影响力，提高模型表达能力\n"
        report_text += "✓ 权重和为1，保持概率解释性\n"
        report_text += "✓ 适合特征选择和模型简化场景"

        # 添加文本
        ax.text(0.05, 0.95, report_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', linespacing=1.5,
                bbox=dict(boxstyle="round,pad=1", facecolor="lightcyan", alpha=0.8))

        return fig


def main():
    """主函数：运行完整的RBF权重优化案例"""
    # 创建可视化器
    visualizer = EnhancedRBFVisualizer()

    print("=" * 60)
    print("RBF权重优化完整案例")
    print("=" * 60)

    # 1. 权重优化分析
    print("正在进行权重优化分析...")
    fig1 = visualizer.visualize_weight_optimization()
    filename1 = os.path.join(visualizer.output_dir, "weight_optimization_process.png")
    fig1.savefig(filename1, dpi=300, bbox_inches='tight')
    plt.close(fig1)
    print(f"权重优化过程图已保存: {os.path.abspath(filename1)}")

    # 2. 3D权重分析
    print("生成3D权重分析图...")
    fig2 = visualizer.visualize_3d_weight_analysis()
    filename2 = os.path.join(visualizer.output_dir, "3d_weight_analysis.png")
    fig2.savefig(filename2, dpi=300, bbox_inches='tight')
    plt.close(fig2)
    print(f"3D权重分析图已保存: {os.path.abspath(filename2)}")

    # 3. 总结报告
    print("生成优化总结报告...")
    fig3 = visualizer.create_summary_report()
    filename3 = os.path.join(visualizer.output_dir, "optimization_summary.png")
    fig3.savefig(filename3, dpi=300, bbox_inches='tight')
    plt.close(fig3)
    print(f"优化总结报告已保存: {os.path.abspath(filename3)}")

    print("\n" + "=" * 60)
    print("案例运行完成！")
    print("=" * 60)
    print("生成的文件:")
    print(f"1. {os.path.abspath(filename1)}")
    print(f"2. {os.path.abspath(filename2)}")
    print(f"3. {os.path.abspath(filename3)}")

    return [filename1, filename2, filename3]


if __name__ == "__main__":
    # 运行主程序
    result_files = main()

    # 显示最终信息
    print(f"\n所有图表已保存到: {os.path.abspath('enhanced_rbf_results')}")
    print("\n关键特性实现:")
    print("✓ 只保留最大的3个权重")
    print("✓ 权重和严格为1")
    print("✓ 大权重获得更大占比")
    print("✓ 权重为1时达到最大影响力")
    print("✓ 完整的可视化分析")
