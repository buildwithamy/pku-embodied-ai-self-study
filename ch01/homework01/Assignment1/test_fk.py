import numpy as np
from robot_model import RobotModel, RevoluteJoint
from config import get_robot_config


def test_fk():
    data = np.load("data/fk.npz")
    q = data["q"]
    poses = data["poses"]
    rcfg = get_robot_config("galbot")
    rm = RobotModel(rcfg)
    for qq, pose in zip(q, poses):
        my_pose = rm.fk(qq)
        for l, p1, p2 in zip(rcfg.link_names, pose, my_pose):
            assert np.allclose(p1, p2), f"The first mismatch link is {l}: expected \n{p1}\n, got \n{p2}\n for qpos \n{qq}\n"
