# TODO make experiment params cmd line args

from random import getrandbits
from pathlib import Path
from shutil import rmtree
from Sampler import Sampler
from Annoy import get_k_nns
import Data

def do_one_trial(n, d, r, c, query_size, is_write):
    try:
        s = Sampler(n, d, r, c, is_write)
    except AssertionError:
        return None

    queries = [getrandbits(d) for _ in range(query_size)]

    n_succ = 0  # number of queries for which c-approx found at least 1 neighbor
    total_t1 = total_t2 = 0  # total time for c-approx and annoy, respectively
    avg_accuracy = 0  # % of approximate neighbors that are also exact neighbors

    for q in queries:
        nns, t1 = s.query(q)
        if not nns:
            continue
        annoy, t2 = get_k_nns(q, len(nns), s.S, d, "hamming")

        avg_accuracy += (len(nns) - len(set(nns) - set(annoy))) / len(nns)
        n_succ += 1
        total_t1 += t1
        total_t2 += t2

    if not n_succ:  # c-approx failed for all queries
        return None

    # average each metric based on number of successful queries
    avg_t1 = total_t1 / n_succ
    avg_t2 = total_t2 / n_succ
    avg_accuracy /= n_succ

    return (avg_t1, avg_t2, avg_accuracy, n_succ)


# num_trials is the # of trials to run for VALID configurations of d,r,c
def run_experiment(data_size, num_trials, query_size, is_print=True, is_write=False):

    # clear old data files first
    if is_write:
        dirpath = Path("data")
        if dirpath.exists() and dirpath.is_dir():
            print("\nDeleting old data files in ./data/")
            print("New data files will OVERWRITE all files in ./data/")
            if input("Continue? (Y/N): ") == "N":
                return
            rmtree(dirpath)

    trial_avgs = []
    total_trials_per_d = [0] * 4

    for d_exp in range(3, 7):  # d = [8,16,32,64]
        d = 1 << d_exp
        cur_results = []
        n_failed = 0
        for r_exp in range(d_exp):  # r = [1,2,...,2^(d_exp-1)]
            r = 1 << r_exp
            for c in range(1, 1 << (d_exp - r_exp)):  # c = [1,2,3,...,d/r - 1]
                for _ in range(num_trials):
                    trial = do_one_trial(data_size, d, r, c, query_size, is_write)
                    if trial:
                        cur_results.append(trial)
                        total_trials_per_d[d_exp - 3] += 1

        sum_results = [sum(metric) for metric in zip(*cur_results)]
        trial_avgs.append([val / len(cur_results) for val in sum_results])

    if is_print:
        pretty_print(trial_avgs, total_trials_per_d, data_size, num_trials, query_size)

    return trial_avgs, total_trials_per_d


def pretty_print(trial_avgs, total_trials_per_d, data_size, num_trials, query_size):

    print(num_trials, "trials simulated for each valid configuration of d, r, and c")
    print("Each trial attempted to query", query_size, "elements from a data set of size", data_size)

    for i, vals in enumerate(trial_avgs):

        print('\n' + ("-" * 100))

        print("\nResults for d =", str(1 << (i + 3)), '(', total_trials_per_d[i], " total trials )\n")

        print("Average execution time PER QUERY:")
        print("c-approximate:", round(vals[0] * 1000, 2), 'ms')
        print("Annoy:", round(vals[1] * 1000, 2), "ms\n")

        print("Average accuracy of c-approximate:", round(vals[2] * 100, 2), '%')
        print("Percent of c-approximate queries which returned at least one neighbor:", round(100 * vals[3] / query_size, 2) , '%')


if __name__ == "__main__":
    # make these cmd line args
    data_size = 1000
    num_trials = 1
    query_size = 10

    exp_results = run_experiment(data_size, num_trials, query_size, is_write=True)

