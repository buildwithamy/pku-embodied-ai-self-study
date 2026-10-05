# 本章可运行演示，按页面顺序执行；不含学生TODO解答。

# HTML L1014
import numpy as np

def rodrigues(u: np.ndarray, theta: float) -> np.ndarray:
    """绕单位轴 u 旋转 theta，返回 3x3 旋转矩阵"""
    u = np.asarray(u, dtype=float)
    if u.shape != (3,) or not np.all(np.isfinite(u)):
        raise ValueError("旋转轴必须是包含三个有限数的向量")
    norm = np.linalg.norm(u)
    if norm == 0:
        raise ValueError("旋转轴不能为零向量")
    u = u / norm
    K = np.array([
        [0, -u[2], u[1]],
        [u[2], 0, -u[0]],
        [-u[1], u[0], 0],
    ])
    return np.cos(theta)*np.eye(3) + (1-np.cos(theta))*np.outer(u,u) + np.sin(theta)*K

# 验证：绕 z 轴转 90°，x 轴应该转到 y 轴
R = rodrigues(np.array([0.,0.,1.]), np.pi/2)
x_new = R @ np.array([1.,0.,0.])
print(x_new)      # 期望 ≈ [0, 1, 0]
assert np.allclose(x_new, [0, 1, 0], atol=1e-9)

# HTML L1038
# 取本章 2 DoF 例子的参数：theta1=30°, theta2=0.1, l1=0.5, l2=0.3, l3=0.2, l4=0.1
import numpy as np
t1 = np.deg2rad(30); t2 = 0.1
l1, l2, l3, l4 = 0.5, 0.3, 0.2, 0.1

T01 = np.array([[np.cos(t1),-np.sin(t1),0,-l2*np.sin(t1)],
                [np.sin(t1), np.cos(t1),0, l2*np.cos(t1)],
                [0,0,1,l1],[0,0,0,1]])
T12 = np.array([[1,0,0,0],[0,1,0,l3],[0,0,1,t2],[0,0,0,1]])
T23 = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,-l4],[0,0,0,1]])

T03 = T01 @ T12 @ T23
print(T03)   # 末端位置 = 最后一列的前三个数
# 对照 5.4 节的公式：t_x = -sin(t1)(l2+l3), t_y = cos(t1)(l2+l3), t_z = l1-l4+t2
expected_t = np.array([-np.sin(t1)*(l2+l3), np.cos(t1)*(l2+l3), l1-l4+t2])
assert np.allclose(T03[:3,3], expected_t, atol=1e-9)
print("✓ 与手推公式一致")

# HTML L1058
def rot_dist(R1: np.ndarray, R2: np.ndarray) -> float:
    """两个旋转之间的最小旋转角（弧度）"""
    return np.arccos(np.clip((np.trace(R2 @ R1.T) - 1)/2, -1, 1))

print(rot_dist(np.eye(3), rodrigues(np.array([1.,0,0]), np.pi/3)))  # ≈ 1.0472 (= π/3)
