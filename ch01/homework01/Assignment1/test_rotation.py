import numpy as np
from rotation import (
    quat_normalize,
    quat_conjugate,
    quat_multiply,
    quat_rotate,
    quat_relative_angle,
    interpolate_quat,
    quat_to_axis_angle,
    quat_to_mat,
    mat_to_axis_angle,
    mat_to_quat,
    axis_angle_to_mat,
    axis_angle_to_quat,
    uniform_random_quat,
)


def test_quat_normalize():
    data = np.load("data/quat_normalize.npz")
    q = data["q"]
    ans = data["ans"]
    for qq, aa in zip(q, ans):
        assert np.allclose(quat_normalize(qq), aa)


def test_quat_conjugate():
    data = np.load("data/quat_conjugate.npz")
    q = data["q"]
    ans = data["ans"]
    for qq, aa in zip(q, ans):
        assert np.allclose(quat_conjugate(qq), aa)


def test_quat_multiply():
    data = np.load("data/quat_multiply.npz")
    q1 = data["q1"]
    q2 = data["q2"]
    ans = data["ans"]
    for qq1, qq2, aa in zip(q1, q2, ans):
        assert np.allclose(quat_multiply(qq1, qq2), aa) or np.allclose(
            -quat_multiply(qq1, qq2), aa
        )


def test_quat_rotate():
    data = np.load("data/quat_rotate.npz")
    q = data["q"]
    v = data["v"]
    ans = data["ans"]
    for qq, vv, aa in zip(q, v, ans):
        assert np.allclose(quat_rotate(qq, vv), aa)


def test_quat_relative_angle():
    data = np.load("data/quat_relative_angle.npz")
    q1 = data["q1"]
    q2 = data["q2"]
    ans = data["ans"]
    for qq1, qq2, aa in zip(q1, q2, ans):
        assert np.allclose(quat_relative_angle(qq1, qq2), aa)


def test_interpolate_quat():
    data = np.load("data/interpolate_quat.npz")
    q1 = data["q1"]
    q2 = data["q2"]
    ratio = data["ratio"]
    ans = data["ans"]
    for qq1, qq2, rr, aa in zip(q1, q2, ratio, ans):
        assert np.allclose(interpolate_quat(qq1, qq2, rr), aa[0]) or np.allclose(
            interpolate_quat(qq1, qq2, rr), aa[1]
        ) or np.allclose(-interpolate_quat(qq1, qq2, rr), aa[0]) or np.allclose(
            -interpolate_quat(qq1, qq2, rr), aa[1]
        )


def test_quat_to_mat():
    data = np.load("data/transform.npz")
    q = data["q"]
    mat = data["mat"]
    for qq, mm in zip(q, mat):
        assert np.allclose(quat_to_mat(qq), mm)


def test_mat_to_quat():
    data = np.load("data/transform.npz")
    q = data["q"]
    mat = data["mat"]
    for qq, mm in zip(q, mat):
        assert np.allclose(mat_to_quat(mm), qq) or np.allclose(-mat_to_quat(mm), qq)


def test_quat_to_axis_angle():
    data = np.load("data/transform.npz")
    q = data["q"]
    aa = data["aa"]
    for qq, aaa in zip(q, aa):
        if np.linalg.norm(aaa) > np.pi - 1e-3:
            assert np.allclose(quat_to_axis_angle(qq), aaa) or np.allclose(
                -quat_to_axis_angle(qq), aaa
            )
        else:
            assert np.allclose(quat_to_axis_angle(qq), aaa)


def test_axis_angle_to_quat():
    data = np.load("data/transform.npz")
    q = data["q"]
    aa = data["aa"]
    for qq, aaa in zip(q, aa):
        assert np.allclose(axis_angle_to_quat(aaa), qq) or np.allclose(
            -axis_angle_to_quat(aaa), qq
        )


def test_uniform_random_quat():
    quats = np.stack([uniform_random_quat() for _ in range(10000)])
    for i in range(10):
        sample = uniform_random_quat()
        rel_angle = np.array([quat_relative_angle(sample, q) for q in quats])
        threshold = np.random.uniform(0, np.pi)
        ratio = np.mean((rel_angle < threshold).astype(float))
        oracle = (threshold - np.sin(threshold)) / np.pi
        assert np.abs(ratio-oracle) < 0.025
