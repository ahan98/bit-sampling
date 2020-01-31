# TODO get Annoy working

from BitSample import BitSample as bs
from annoy import AnnoyIndex
import random

def read_first_lines(filename, limit):
    with open(filename) as input_file:
        content = input_file.read().splitlines()

    for i, line in enumerate(content):
        if i >= 10:
            break
        print(line)


def testAnnoy():
    f = 1
    t = AnnoyIndex(f, "euclidean")  # Length of item vector that will be indexed
    for i in range(10):
        v = [random.getrandbits(64) for _ in range(f)]
        print(v[0])
        t.add_item(i, v)
    t.build(10)
    print(t.get_nns_by_item(0, 10))
    #for i in range(10):
    #    for j in range(i+1,10):
    #        print(t.get_distance(i, j))


if __name__ == "__main__":
    sampler = bs(n=10, d=16, r=2, c=2)
    #sampler.dataToCSV()
    #read_first_lines("data.csv", 10)
    testAnnoy()
    #while True:
    #    q = int(input("Enter number to query dataset: "))
    #    print("Searching for number(s) approximately close to", q, "...")
    #    print(sampler.query(q))
