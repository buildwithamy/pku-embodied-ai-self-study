from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class Joint:
    name: str
    trans: np.ndarray  # with shape (3,)
    rot: np.ndarray  # rotation matrix with shape (3, 3)


@dataclass
class FixedJoint(Joint):
    pass


@dataclass
class RevoluteJoint(Joint):
    axis: np.ndarray
    lower_limit: float
    upper_limit: float


@dataclass
class Link:
    name: str
    visual_meshes: List[str]
