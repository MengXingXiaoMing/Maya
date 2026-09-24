# -*- coding: utf-8 -*-
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import os

# 使用您提供的三维数据点
input_points = np.array([
    [390.06, 333.06, 95.06],
    [330.06, 53.06, 95.06],
    [35.06, 333.06, 945.06],
    [70.06, 733.06, 95.06],
    [38.06, 63.06, 91.06]
])

# 计算每个点的欧几里得范数作为目标值
target_values = np.linalg.norm(input_points, axis=1)

print("输入数据点:")
for i, point in enumerate(input_points):
    print(f"点{i + 1}: {point} → 范数: {target_values[i]:.2f}")


# RBF神经网络类
class RBFNetwork:
    def __init__(self, n_centers=5, sigma=1.0):
        self.n_centers = n_centers
        self.sigma = sigma
        self.centers = None
        self.weights = None

    def _rbf_function(self, x, center):
        """径向基函数（高斯函数）"""
        return np.exp(-np.sum((x - center) ** 2) / (2 * self.sigma ** 2))

    def fit(self, X, y):
        """训练RBF网络"""
        # 使用K-means聚类确定RBF中心
        kmeans = KMeans(n_clusters=self.n_centers, random_state=42)
        kmeans.fit(X)
        self.centers = kmeans.cluster_centers_

        # 计算RBF激活值
        n_samples = X.shape[0]
        phi = np.zeros((n_samples, self.n_centers))

        for i in range(n_samples):
            for j in range(self.n_centers):
                phi[i, j] = self._rbf_function(X[i], self.centers[j])

        # 添加偏置项
        phi = np.hstack([phi, np.ones((n_samples, 1))])

        # 使用最小二乘法求解权重
        self.weights = np.linalg.pinv(phi) @ y

        return self

    def predict(self, X):
        """使用RBF网络进行预测"""
        n_samples = X.shape[0]
        phi = np.zeros((n_samples, self.n_centers))

        for i in range(n_samples):
            for j in range(self.n_centers):
                phi[i, j] = self._rbf_function(X[i], self.centers[j])

        # 添加偏置项
        phi = np.hstack([phi, np.ones((n_samples, 1))])

        return phi @ self.weights


def save_plot(fig, filename):
    """保存图形到文件"""
    output_dir = "rbf_fitting_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filepath


# 主程序
def main():
    print("=" * 60)
    print("RBF神经网络拟合案例")
    print("=" * 60)

    X = input_points
    y = target_values

    print(f"输入数据形状: {X.shape}")
    print(f"目标值形状: {y.shape}")
    print()

    # 数据标准化
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

    # 创建并训练RBF模型
    rbf_model = RBFNetwork(n_centers=3, sigma=1.0)
    rbf_model.fit(X_scaled, y_scaled)

    # 预测训练数据
    y_pred_scaled = rbf_model.predict(X_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()

    # 计算误差
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)

    print("模型性能:")
    print(f"均方误差 (MSE): {mse:.6f}")
    print(f"均方根误差 (RMSE): {rmse:.6f}")
    print()

    # 输出预测结果
    print("预测结果对比:")
    for i in range(len(X)):
        print(f"点{i + 1}: 真实范数 = {y[i]:.2f}, 预测范数 = {y_pred[i]:.2f}, 误差 = {abs(y[i] - y_pred[i]):.2f}")

    # 预测新点 [1, 2, 3]
    new_point = np.array([[1, 2, 3]])
    new_point_scaled = scaler_X.transform(new_point)
    new_pred_scaled = rbf_model.predict(new_point_scaled)
    new_pred = scaler_y.inverse_transform(new_pred_scaled.reshape(-1, 1)).flatten()[0]

    print(f"\n对新点 [1, 2, 3] 的预测:")
    print(f"预测范数值: {new_pred:.2f}")
    print(f"实际范数值: {np.linalg.norm(new_point):.2f}")

    # 可视化结果
    visualize_results(X, y, y_pred, rbf_model, scaler_X)

    return rbf_model, X, y, y_pred


def visualize_results(X, y, y_pred, rbf_model, scaler_X):
    """可视化RBF拟合结果"""

    # 1. 3D散点图：真实值 vs 预测值
    fig1 = plt.figure(figsize=(15, 5))

    # 真实值
    ax1 = fig1.add_subplot(131, projection='3d')
    scatter1 = ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap='viridis', s=100)
    ax1.set_title('真实范数值')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    fig1.colorbar(scatter1, ax=ax1, shrink=0.5)

    # 预测值
    ax2 = fig1.add_subplot(132, projection='3d')
    scatter2 = ax2.scatter(X[:, 0], X[:, 1], X[:, 2], c=y_pred, cmap='plasma', s=100)
    ax2.set_title('预测范数值')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    fig1.colorbar(scatter2, ax=ax2, shrink=0.5)

    # 误差
    errors = np.abs(y - y_pred)
    ax3 = fig1.add_subplot(133, projection='3d')
    scatter3 = ax3.scatter(X[:, 0], X[:, 1], X[:, 2], c=errors, cmap='hot', s=100)
    ax3.set_title('绝对误差')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    fig1.colorbar(scatter3, ax=ax3, shrink=0.5)

    plt.tight_layout()
    save_plot(fig1, "3d_scatter_comparison.png")
    print("3D散点图已保存")

    # 2. 2D散点图：真实值 vs 预测值
    fig2 = plt.figure(figsize=(10, 4))

    plt.subplot(121)
    plt.scatter(range(len(y)), y, c='blue', s=100, label='真实值')
    plt.scatter(range(len(y_pred)), y_pred, c='red', s=100, label='预测值')
    plt.xlabel('数据点索引')
    plt.ylabel('范数值')
    plt.title('真实值 vs 预测值')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(122)
    plt.bar(range(len(errors)), errors, color='orange')
    plt.xlabel('数据点索引')
    plt.ylabel('绝对误差')
    plt.title('预测误差')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    save_plot(fig2, "2d_comparison.png")
    print("2D比较图已保存")

    # 3. RBF中心点可视化
    fig3 = plt.figure(figsize=(8, 6))
    ax = fig3.add_subplot(111, projection='3d')

    # 原始数据点
    scatter_orig = ax.scatter(X[:, 0], X[:, 1], X[:, 2], c='blue', s=100, label='原始数据点')

    # RBF中心点（反标准化）
    centers_original = scaler_X.inverse_transform(rbf_model.centers)
    scatter_centers = ax.scatter(centers_original[:, 0], centers_original[:, 1], centers_original[:, 2],
                                 c='red', s=200, marker='x', label='RBF中心点')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('RBF中心点分布')
    ax.legend()

    plt.tight_layout()
    save_plot(fig3, "rbf_centers.png")
    print("RBF中心点图已保存")


if __name__ == "__main__":
    # 运行主程序
    rbf_model, X, y, y_pred = main()

    print("\n" + "=" * 60)
    print("程序执行完成")
    print("=" * 60)
    print("所有图表已保存到 'rbf_fitting_results' 文件夹")
