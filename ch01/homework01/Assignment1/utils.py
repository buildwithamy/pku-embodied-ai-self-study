import numpy as np


def str_to_np(string: str) -> np.ndarray:
    """
    Convert strings like "0.1 0.2" into np.ndarray
    """
    return np.array([float(v) for v in string.split(" ")])
