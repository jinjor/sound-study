import numpy as np
from wavetable import np_get_saw_value

def hard_sync(freq, t, opt):
    return np.sin(opt['ratio'] * (2 * np.pi) * np.remainder(freq * t, 1))

def wt_hard_sync(freq, t, opt):
    normalized_angle = np.remainder(freq * t, 1)
    angle = (np_get_saw_value(freq, normalized_angle) * np.pi + np.pi).astype('float32')
    return np.sin(opt['ratio'] * angle)

def _sin(normalized_angle):
    return np.sin(2 * np.pi * normalized_angle)

def sin(freq, t, opt):
    normalized_angle = np.remainder(freq * t, 1)
    return _sin(normalized_angle)

def _square(normalized_angle):
    return np.where(normalized_angle > 0.5, 1, -1)

def square(freq, t, opt):
    normalized_angle = np.remainder(freq * t, 1)
    return _square(normalized_angle)

def _saw(normalized_angle):
    return normalized_angle * 2 - 1

def saw(freq, t, opt):
    normalized_angle = np.remainder(freq * t, 1)
    return _saw(normalized_angle)

def wt_saw(freq, t, opt):
    normalized_angle = np.remainder(freq * t, 1)
    return np_get_saw_value(freq, normalized_angle)

def fm_help(career, modulator, opt, freq, t):
    normalized_angle1 = np.remainder(freq * t, 1)
    normalized_angle2 = np.remainder(opt['ratio'] * freq * t, 1)
    normalized_angle = np.remainder(normalized_angle1 + opt['amount'] * modulator(normalized_angle2), 1)
    return career(normalized_angle)

def fm(career, modulator):
    return lambda freq, t, opt: fm_help(career, modulator, opt, freq, t)

def modulator_hardsync(normalized_angle):
    return normalized_angle