from random import getrandbits

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


# randomly generate n d-bit ints and save in data.txt
def get_rand_data(n, d):
    bits = []
    for _ in range(n):
        bits.append([getrandbits(1) for _ in range(d)])
    _write_bits_to_file(bits)
    return bits


# write bit arrays as ints to data.txt
def _write_bits_to_file(bits):
    with open('data.txt', 'w') as output_file:
        print("Generating random data\n")
        print("Writing to data.txt...")
        for bit_arr in bits:
            n = 0
            for b in bit_arr:
                n = (n << 1) | b
            output_file.write(str(n) + '\n')


def get_dint(bitlist):
    val = 0
    for bit in bitlist:
        val = (val << 1) | bit
    return val
