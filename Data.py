from random import getrandbits
from pathlib import Path
from os import listdir
from numpy import savetxt

# convert file of d-bit ints to list of bits
def get_bit_arr_from_data(filename, d):
    lines = []
    with open(filename) as input_file:
        lines = input_file.read().splitlines()
    return [get_dbit_arr(int_str, d, True) for int_str in lines]


# convert int string to length-d list of bits
def get_dbit_arr(n, d, is_string):
    if is_string:
        n = int(n)
    b = [n >> i & 1 for i in range(n.bit_length() - 1,-1,-1)]
    return [0] * (d - len(b)) + b


# randomly generate n d-bit ints and save to nums_i.dat if desired
def get_rand_data(n, d, is_write):
    bits = []
    for _ in range(n):
        bits.append([getrandbits(1) for _ in range(d)])
    if is_write:
        _write_bits_to_file(bits, d)
    return bits


# write bit arrays to file
def _write_bits_to_file(bits, d):
    rel_dir = "./data/d_" + str(d)
    Path(rel_dir).mkdir(parents=True, exist_ok=True)  # create dir if not exists

    # name data files systematically
    datfiles = [f for f in listdir(rel_dir) if f.endswith(".dat")]
    file_idx = len(datfiles) + 1
    dat_filename = "nums_" + str(file_idx) + ".dat"

    savetxt(rel_dir + '/' + dat_filename, [get_dint(arr) for arr in bits], fmt="%d")


def get_dint(bitlist):
    val = 0
    for bit in bitlist:
        val = (val << 1) | bit
    return val
