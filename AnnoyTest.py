from annoy import AnnoyIndex
from BitSample import BitSample as bs
import random

def get_bit_arr_from_data(filename):
    with open(filename) as input_file:
        lines = input_file.read().splitlines()

    bits = []
    for line in lines:
        cur = []
        for bit in line:
            cur.append(int(bit))
        bits.append(cur)

    return bits


def get_nns_annoy(q, bits, d, metric):
    t = AnnoyIndex(d, metric)
    for idx, bit_arr in enumerate(bits):
        t.add_item(idx, bit_arr)
    t.build(10)
    t.save("test.ann")
    u = AnnoyIndex(d, metric)
    u.load("test.ann")
    print(u.get_nns_by_item(q, len(bits)))


sampler = bs(n=10, d=16, r=2, c=2)
print(sampler.get_rand_data())
get_nns_annoy(0, sampler.get_rand_data(), sampler.d, "hamming")
