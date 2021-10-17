import numpy as np

def phase_saw(theta):
    return np.remainder(theta, 2 * np.pi)

def hard_sync(theta, ratio):
    return np.sin(ratio * phase_saw(theta))

def sin(theta, ratio):
    return np.sin(theta)

def square(theta, ratio):
    return np.where(np.remainder(theta, 2 * np.pi) > np.pi, 1, -1)