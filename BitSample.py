from random import sample
from math import log, floor
from collections import defaultdict
from time import time
import Data

class Sampler:

    # n - size of (randomly generated) data set
    # d - int bit size
    # r - range for close points
    # c - approximation factor
    def __init__(self, n, d, r, c, data_file=None):
        self.n = n
        self.d = d
        self.r = r
        assert(r < d)

        self.c = c
        assert(c*r < d)

        if data_file:
            self.S = Data.get_bit_arr_from_data(data_file, d)
        else:
            self.S = Data.get_rand_data(n, d)

        self.p1 = 1 - r/d        # lower bound prob. of choosing same bit from two close points
        self.p2 = 1 - c*r/d      # upper bound prob. of choosing same bit from two far points

        self.k = floor(log(n, 1/self.p2))   # number of bits sampled from each x in S
        assert(self.k <= d)

        # number of hash functions g_i (to compute buckets)
        self.L = floor(5/self.p1)   # smaller r = larger p1 = smaller L

        self.bitmasks = self.get_masks()    # corresponds to the indices of the randomly sampled bits
        self.inv_map = self.preprocess()    # stores all x in S that hash to g_i(x)


    # hash each x in S to buckets g_1(x),...,g_L(x)
    def preprocess(self):
        inv_map = defaultdict(list)
        for x in self.S:
            used_buckets = set()
            for i in range(self.L):
                g_ix = self._get_bucket(self.bitmasks[i], x)
                if g_ix in used_buckets:
                    continue
                used_buckets.add(g_ix)
                inv_map[g_ix].append(x)
        return inv_map


    def _get_bucket(self, bitmask, x):
        bucket = []
        for i, bit in enumerate(bitmask):
            if bit:
                bucket.append(str(x[i]))
        return ''.join(bucket)


    # q - the element to be queried
    # returns approx. (defined by c*r) nearest neighbors to q, sorted by distance
    def query(self, q):
        nns = set()
        q_bits = Data.get_dbit_arr(q, self.d, False)
        start = time()
        for i in range(self.L):
            bucket = self._get_bucket(self.bitmasks[i], q_bits)
            for x in self.inv_map[bucket]:
                dist = Sampler.hamming(x, q_bits)
                if dist > (self.c * self.r):
                    continue
                x = Data.get_dint(x)
                if (x, dist) not in nns:
                    nns.add((x, dist))
        nns = sorted(nns, key=lambda pair:pair[1])
        total_t = time() - start
        return nns, total_t


    # returns hamming distance between two length-d bit arrays
    @staticmethod
    def hamming(a, b):
        n_diff = 0
        for i in range(len(a)):
            n_diff += a[i] ^ b[i]
        return n_diff


    # returns a list of L randomly generated bitmasks
    def get_masks(self):
        bitmasks = []
        for _ in range(self.L):
            bitmasks.append(self.kOnes())
        return bitmasks


    # returns a random d-bit int with exactly k set bits
    def kOnes(self):
        mask = [0] * self.d
        for idx in sample(range(self.d), self.k):
            mask[idx] = 1
        return mask

