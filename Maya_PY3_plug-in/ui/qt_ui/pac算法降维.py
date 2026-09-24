# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 创建学生成绩数据
student_data = {
    '学生': ['A', 'B', 'C', 'D'],
    '数学': [390.06, 333.06, 95.06, 126.56],
    '语文': [115.56, 126.56, 76.56, 68.06],
    '物理': [115.56, 105.06, 1.56, 0.56],
    '英语': [1.56, 52.56, 7.56, 33.06],
    '体育': [9.00, 4.00, 0.00, 1.00]
}

# 创建DataFrame
df = pd.DataFrame(student_data)
df.set_index('学生', inplace=True)

print("原始学生成绩数据:")
print(df)
print()

# 提取特征数据
X = df.values

# 1. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("标准化后的数据:")
scaled_df = pd.DataFrame(X_scaled, index=df.index, columns=df.columns)
print(scaled_df)
print()

# 2. 应用PCA降维到1维
pca_1d = PCA(n_components=1)
X_pca_1d = pca_1d.fit_transform(X_scaled)

print("PCA降维到1维的结果:")
pca_1d_df = pd.DataFrame(X_pca_1d, index=df.index, columns=['一维数据'])
print(pca_1d_df)
print()

# 3. 显示PCA相关信息
print("PCA分析信息:")
print(f"第一主成分解释的方差比例: {pca_1d.explained_variance_ratio_[0]:.4f} ({pca_1d.explained_variance_ratio_[0]*100:.2f}%)")
print()

# 4. 显示主成分的组成（各科目对主成分的贡献）
print("各科目对第一主成分的贡献（特征向量）:")
components_df = pd.DataFrame(
    pca_1d.components_.T,
    index=df.columns,
    columns=['第一主成分贡献']
)
print(components_df)
print()

# 5. 学生排名（基于一维数据）
print("学生综合能力排名（基于PCA一维数据）:")
ranking = pca_1d_df.sort_values('一维数据', ascending=False)
for i, (student, score) in enumerate(ranking.iterrows(), 1):
    print(f"第{i}名: 学生{student} (一维数据: {score['一维数据']:.4f})")