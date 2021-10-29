import numpy as np
import wavetable

def hard_sync(freq, t, opt):
    return np.sin(opt['ratio'] * (2 * np.pi) * np.remainder(freq * t, 1))

def wt_hard_sync(freq, t, opt):
    normalized_angle = np.remainder(freq * t, 1)
    angle = (_wt_saw(freq, normalized_angle) * np.pi + np.pi).astype('float32')
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

def saw_with_num_partials(freq, t, num_partials):
    normalized_angle = np.remainder(freq * t, 1)
    array = wavetable.make_one_saw_array(num_partials)
    def help(normalized_angle):
        return wavetable.get_saw_value_from_array(array, normalized_angle)
    np_help = np.frompyfunc(help, 1, 1)
    return np_help(normalized_angle)

_wt_saw = wavetable.np_get_saw_value

def wt_saw(freq, t, opt):
    normalized_angle = np.remainder(freq * t, 1)
    return _wt_saw(freq, normalized_angle)

_wt_square = wavetable.np_get_square_value

def wt_square(freq, t, opt):
    normalized_angle = np.remainder(freq * t, 1)
    return _wt_square(freq, normalized_angle)

def fm_help(career, modulator, opt, freq, t):
    normalized_angle1 = np.remainder(freq * t, 1)
    normalized_angle2 = np.remainder(opt['ratio'] * freq * t, 1)
    normalized_angle = np.remainder(normalized_angle1 + opt['amount'] * modulator(freq, normalized_angle2), 1).astype('float32')
    return career(freq, normalized_angle)

def fm(career, modulator):
    return lambda freq, t, opt: fm_help(career, modulator, opt, freq, t)

def modulator_hardsync(normalized_angle):
    return normalized_angle