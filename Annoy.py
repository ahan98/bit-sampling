from time import time
from annoy import AnnoyIndex
from Sampler import Sampler
import Data

def get_k_nns(q, k, bits, d, metric):
    start = time()
    t = AnnoyIndex(d, metric)
    for idx, bit_arr in enumerate(bits):
        t.add_item(idx, bit_arr)
    t.build(10)

    q_bits = Data.get_dbit_arr(q, d, False)
    nns_sorted_idx = t.get_nns_by_vector(q_bits, len(bits))[:k]

    nns = []
    for i in nns_sorted_idx:
        dist = Sampler.hamming(bits[i], q_bits)
        nns.append((Data.get_dint(bits[i]), dist))
    total_t = time() - start

    return nns, total_t

