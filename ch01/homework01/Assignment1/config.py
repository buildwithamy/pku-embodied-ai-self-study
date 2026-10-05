from dataclasses import dataclass
from typing import List
import numpy as np
from copy import deepcopy


@dataclass
class RobotConfig:
    urdf_path: str
    link_names: List[str]
    joint_names: List[str]
    init_qpos: np.ndarray


GALBOT_CONFIG = RobotConfig(
    urdf_path="galbot/galbot_left_arm_simple.urdf",
    link_names=[
        "base_link",
        "left_arm_base_link",
        "left_arm_link1",
        "left_arm_link2",
        "left_arm_link3",
        "left_arm_link4",
        "left_arm_link5",
        "left_arm_link6",
        "left_arm_link7",
        "left_arm_end_effector_mount_link",
        "left_gripper_base_link",
        "left_gripper_tcp_link",
    ],
    joint_names=[
        "left_arm_joint",
        "left_arm_joint1",
        "left_arm_joint2",
        "left_arm_joint3",
        "left_arm_joint4",
        "left_arm_joint5",
        "left_arm_joint6",
        "left_arm_joint7",
        "left_arm_end_effector_mount_joint",
        "left_gripper_joint",
        "left_gripper_tcp_joint",
    ],
    init_qpos=np.array([-0.65, 1.26, -0.1, -1.6357, 1.7, -0.111, 0.8996]),
)


def get_robot_config(name: str) -> RobotConfig:
    if name == "galbot":
        return deepcopy(GALBOT_CONFIG)
    else:
        raise ValueError(f"Unknown robot name: {name}")
