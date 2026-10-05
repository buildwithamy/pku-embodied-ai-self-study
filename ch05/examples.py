"""对应本章 Procrustes 提示的可运行验证；不是作业2学生函数的答案。"""
import numpy as np

rng = np.random.default_rng(20261004)
N = rng.normal(size=(40, 3))  # 源点：每行一个点
angle = 0.4
R_true = np.array([[np.cos(angle), -np.sin(angle), 0],
                   [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
t_true = np.array([0.3, -0.2, 0.1])
M = (R_true @ N.T).T + t_true  # 对应目标点
Mc, Nc = M - M.mean(0), N - N.mean(0)
U, S, Vh = np.linalg.svd(Mc.T @ Nc)
R = U @ np.diag([1, 1, np.linalg.det(U @ Vh)]) @ Vh
t = M.mean(0) - R @ N.mean(0)
residual = np.max(np.abs(M - ((R @ N.T).T + t)))
assert np.allclose(R, R_true, atol=1e-9)
assert np.allclose(t, t_true, atol=1e-9)
assert np.isclose(np.linalg.det(R), 1)
print("✓ Procrustes 恢复旋转与平移；最大残差:", residual)
