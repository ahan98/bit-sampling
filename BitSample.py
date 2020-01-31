from random import sample, getrandbits
from math import log, floor
from collections import defaultdict
from csv import writer

class BitSample:

    # n - size of (randomly generated) data set
    # d - int bit size
    # r - range for close points
    # c - approximation factor
    def __init__(self, n, d, r, c):
        self.n = n
        self.d = d
        self.r = r
        assert(r < d)

        self.c = c
        assert(c*r < d)

        self.S = self.get_rand_data()

        self.p1 = 1 - r/d        # lower bound prob. of choosing same bit from two close points
        self.p2 = 1 - c*r/d      # upper bound prob. of choosing same bit from two far points

        # NOTE floor or ceil?
        self.k = floor(log(n, 1/self.p2))    # number of bits sampled from each x in S
        self.L = floor(5/self.p1)            # number of hash functions g_i (to compute buckets)

        # NOTE not sure if these need to be attributes
        self.bitmasks = self.getMasks()     # corresponds to the indices of the randomly sampled bits
        self.inv_map = self.preprocess()    # stores all x in S that hash to g_i(x)


    # randomly generate n d-bit ints
    def get_rand_data(self):
        data = []
        for _ in range(self.n):
            data.append([getrandbits(1) for _ in range(self.d)])
        return data


    # hashes each x in S to buckets g_1(x),...,g_L(x)
    def preprocess(self):
        inv_map = defaultdict(list)
        for i in range(self.L):
            for x in self.S:
                bucket = self.get_bucket(self.bitmasks[i], x)
                inv_map[bucket].append(x)
        return inv_map


    # TODO make concatenation more efficient
    def get_bucket(self, bitmask, x):
        bucket = ""
        for i in range(len(bitmask)):
            bucket += str(bitmask[i] & x[i])
        return bucket


    # q - the element to be queried
    # returns an approx. close x in S, if such an x exists
    def query(self, q):
        for i in range(self.L):
            bucket = self.bitmasks[i] & q
            for x in self.inv_map[bucket]:
                if self.hamming(x,q) <= (self.c * self.r):
                    return x


    # returns hamming distance between two length-d bit arrays
    def hamming(self, a, b):
        n_diff = 0
        for i in range(self.d):
            n_diff += a[i] ^ b[i]
        return n_diff


    # returns a list of L randomly generated bitmasks
    def getMasks(self):
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


    def dataToCSV(self):
        print("saving data set to data.csv...")
        with open('data.csv', 'w') as f:
            my_writer = writer(f)
            for val in self.S:
                my_writer.writerow([val])


    def print(self):
        print("n =", self.n)
        print("r =", self.r)
        print("c =", self.c)
        print("d =", self.d)
        self.dataToCSV()
        print("p1 =", self.p1)
        print("p2 =", self.p2)
        print("L =", self.L)
        print("k =", self.k)
        print("bitmasks =", self.bitmasks)
        print("inv_map =", self.inv_map)


