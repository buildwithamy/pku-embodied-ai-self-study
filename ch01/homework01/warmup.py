"""作业 1 前置小练习：只需 NumPy，不修改或填写原作业模板。"""

import numpy as np


def main():
    np.set_printoptions(precision=6, suppress=True)

    # 一维数组、点积、叉积、模长和矩阵乘法。
    a = np.array([3.0, 4.0, 0.0])
    b = np.array([0.0, 1.0, 0.0])
    assert a.shape == (3,)
    assert np.isclose(np.linalg.norm(a), 5.0)
    assert np.isclose(a @ b, 4.0)
    assert np.allclose(np.cross(a, b), [0.0, 0.0, 3.0])
    assert np.allclose(a * b, [0.0, 4.0, 0.0])
    print("1. 数组：norm=5，点积=4，叉积=[0, 0, 3]")

    # 三角函数使用弧度；这里手写一例绕 Z 轴旋转的矩阵。
    theta = np.deg2rad(90.0)
    R_z = np.array([
        [np.cos(theta), -np.sin(theta), 0.0],
        [np.sin(theta), np.cos(theta), 0.0],
        [0.0, 0.0, 1.0],
    ])
    p_local = np.array([1.0, 0.0, 0.0])
    assert np.allclose(R_z @ p_local, [0.0, 1.0, 0.0])
    assert np.allclose(R_z.T @ R_z, np.eye(3))
    assert np.isclose(np.linalg.det(R_z), 1.0)
    print("2. 旋转：局部 X 方向经绕 Z 轴 90 度变成 Y 方向")

    # 坐标从子坐标系变到父坐标系：先旋转、再加平移。
    t_parent = np.array([2.0, 0.0, 0.0])
    T_parent_child = np.eye(4)
    T_parent_child[:3, :3] = R_z
    T_parent_child[:3, 3] = t_parent
    p_homogeneous = np.append(p_local, 1.0)
    p_parent = T_parent_child @ p_homogeneous
    assert np.allclose(p_parent, [2.0, 1.0, 0.0, 1.0])
    # 齐次方向向量末尾为 0，平移不会影响方向。
    d_parent = T_parent_child @ np.array([1.0, 0.0, 0.0, 0.0])
    assert np.allclose(d_parent, [0.0, 1.0, 0.0, 0.0])
    print("3. 齐次变换：点变成 [2, 1, 0]，方向仍为 [0, 1, 0]")

    # 单位四元数只构造已知实例，不提供原作业函数的完整实现。
    q_identity = np.array([1.0, 0.0, 0.0, 0.0])
    q_z90 = np.array([np.cos(theta / 2), 0.0, 0.0, np.sin(theta / 2)])
    assert np.isclose(np.linalg.norm(q_z90), 1.0)
    assert np.isclose(abs(q_z90 @ (-q_z90)), 1.0)
    # q 与 -q 表示同一旋转，其相对旋转角为 0。
    dot_same_rotation = np.clip(abs(q_z90 @ (-q_z90)), 0.0, 1.0)
    assert np.isclose(2.0 * np.arccos(dot_same_rotation), 0.0)
    rotation_vector = np.array([0.0, 0.0, theta])
    assert np.isclose(np.linalg.norm(rotation_vector), np.pi / 2)
    assert np.allclose(q_identity, [1.0, 0.0, 0.0, 0.0])
    print("4. 四元数：wxyz=", q_z90, "；旋转向量=", rotation_vector)

    # 旋转复合顺序：使用两个已知矩阵观察非交换性。
    R_x90 = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]])
    first_x_then_z = R_z @ R_x90 @ p_local
    first_z_then_x = R_x90 @ R_z @ p_local
    assert np.allclose(first_x_then_z, [0.0, 1.0, 0.0])
    assert np.allclose(first_z_then_x, [0.0, 0.0, 1.0])
    print("5. 次序：先 X 后 Z 得到 Y；先 Z 后 X 得到 Z")

    # 人工小链：基座到旋转关节后，再接固定的工具平移。
    # 与原模板的机器人资产无关，只展示两个已知变换的累乘。
    T_base_link = np.eye(4)
    T_base_link[:3, :3] = R_z
    T_link_tool = np.eye(4)
    T_link_tool[:3, 3] = np.array([1.0, 0.0, 0.0])
    T_base_tool = T_base_link @ T_link_tool
    assert np.allclose(T_base_tool[:3, 3], [0.0, 1.0, 0.0])
    print("6. 固定工具：局部 X 平移 1 米，在基座坐标系落到 Y=1 米")

    # 接近 180 度时“只按迹求 w 再除以 w”的转换公式会遇到 0 分母。
    R_x180 = np.diag([1.0, -1.0, -1.0])
    assert np.isclose(1.0 + np.trace(R_x180), 0.0)
    print("7. 180 度检查：1+trace(R)=0，应选虚部分量稳定分支")

    # 浮点数比较：三角函数计算的 cos(pi/2) 通常不严格等于 0。
    assert np.isclose(np.cos(theta), 0.0, atol=1e-12)
    assert np.allclose(p_parent[:3], [2.0, 1.0, 0.0], atol=1e-12)
    print("8. 浮点比较：使用 isclose / allclose，不用数组直接 == 判正确")
    print("前置示例全部通过。下一步进入 Assignment1 目录，逐个实现原作业 TODO。")


if __name__ == "__main__":
    main()
