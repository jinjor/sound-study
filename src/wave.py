import numpy as np
from wavetable import np_get_saw_value

def phase_saw(angle):
    return np.remainder(angle, 2 * np.pi)

def phase_wt_saw(freq, angle):
    return (np_get_saw_value(freq, angle) * np.pi + np.pi).astype('float32')

def hard_sync(freq, angle, ratio):
    return np.sin(ratio * phase_saw(angle))

def wt_hard_sync(freq, angle, ratio):
    return np.sin(ratio * phase_wt_saw(freq, angle))

def sin(freq, angle, ratio):
    return np.sin(angle)

def square(freq, angle, ratio):
    normalized_angle = np.remainder(angle, 2 * np.pi) / (2 * np.pi)
    return np.where(normalized_angle > 0.5, 1, -1)

def saw(freq, angle, ratio):
    normalized_angle = np.remainder(angle, 2 * np.pi) / (2 * np.pi)
    return normalized_angle * 2 - 1

def wt_saw(freq, angle, ratio):
    return np_get_saw_value(freq, angle)