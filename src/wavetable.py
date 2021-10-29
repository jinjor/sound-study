import numpy as np
import math

NUM_SAMPLES = 4096
NUM_VARIATION = 128
BASE_FREQ = 440
MAX_FREQ = 22000

def make_lookup_table():
    array = [None] * MAX_FREQ
    freq_index = 0
    for note_num in range(NUM_VARIATION):
        freq = BASE_FREQ * math.pow(2, (note_num - 69) / 12)
        while (freq_index < freq):
            array[freq_index] = note_num
            freq_index += 1
    last_freq_index = freq_index - 1
    while (freq_index < MAX_FREQ):
        array[freq_index] = array[last_freq_index]
        freq_index += 1
    return array
lookup_table = make_lookup_table()

def sum_saw_partials(num_partials, angle):
    n = np.arange(1, num_partials + 1)
    k = (np.pi / 2) / num_partials
    gibbs_fix = np.power(np.cos((n - 1) * k), 2)
    return np.sum(np.sin(n * angle) / n * gibbs_fix)
np_sum_saw_partials = np.frompyfunc(sum_saw_partials, 2, 1)

def make_saw_table():
    print("creating saw table")
    variations = np.arange(NUM_VARIATION)
    freqs = BASE_FREQ * np.power(2, (variations - 69) / 12)
    num_partials = np.int_(MAX_FREQ / freqs)
    angles = 2 * math.pi / (NUM_SAMPLES - 1) * np.arange(NUM_SAMPLES)
    ret = np_sum_saw_partials(num_partials.reshape(-1, 1), angles)
    max = np.max(np.abs(ret[0]))
    ret = ret / max
    print(ret.shape)
    print("done")
    return ret
saw_table = make_saw_table()

def get_saw_value_from_array(array, normalized_angle):
    index_float = normalized_angle * 4095
    index = int(index_float)
    fragment = index_float - index
    return array[index] * (1 - fragment) + array[index + 1] * fragment

def get_saw_value_from_array_reverse(array, normalized_angle):
    index_float = normalized_angle * 4095
    index = int(index_float)
    fragment = index_float - index
    return array[4095 - index] * (1 - fragment) + array[4095 - index - 1] * fragment

def get_saw_value(freq, normalized_angle):
    note_index = lookup_table[int(freq)]
    array = saw_table[note_index]
    return get_saw_value_from_array(array, normalized_angle)

np_get_saw_value = np.frompyfunc(get_saw_value, 2, 1)

def get_pulse_value(edge, freq, normalized_angle):
    angle_shift = (1.0 - edge * 0.99) * 0.5 # ?
    pos1 = normalized_angle
    pos2 = np.remainder(pos1 + angle_shift, 1)
    note_index = lookup_table[int(freq)]
    array = saw_table[note_index]
    return get_saw_value_from_array(array, pos1) + get_saw_value_from_array_reverse(array, pos2) + (1.0 - 2 * angle_shift)

get_square_value = lambda freq, normalized_angle: get_pulse_value(0, freq, normalized_angle)

np_get_square_value = np.frompyfunc(get_square_value, 2, 1)