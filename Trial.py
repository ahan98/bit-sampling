from BitSample import Sampler, Data
from Annoy import get_k_nns
from random import getrandbits

def do_one_trial(n, d, r, c, query_size):
    try:
        s = Sampler(n, d, r, c)
    except AssertionError:
        return None

    bits = Data.get_bit_arr_from_data("data.txt", d)
    queries = [getrandbits(d) for _ in range(query_size)]

    n_succ = 0
    total_t1 = total_t2 = 0
    avg_accuracy = 0

    for q in queries:
        nns, t1 = s.query(q)
        if not nns:
            continue
        annoy, t2 = get_k_nns(q, len(nns), bits, d, "hamming")

        avg_accuracy += (len(nns) - len(set(nns) - set(annoy))) / len(nns)
        n_succ += 1
        total_t1 += t1
        total_t2 += t2

    if not n_succ:
        return None

    avg_t1 = total_t1 / n_succ
    avg_t2 = total_t2 / n_succ
    avg_accuracy /= n_succ
    ratio_succ = n_succ / len(queries)

    return (avg_t1, avg_t2, avg_accuracy, ratio_succ)


def run_experiment(n_trials):

    trial_avgs = []

    for d in [8, 16, 32, 64]:
        cur_results = []
        r = 2
        while r < d:
            c = 1
            while c*r < d:
                for i in range(n_trials):
                    trial = do_one_trial(1000, d, r, c, 10)
                    if trial:
                        cur_results.append(trial)

                c += 1
            r <<= 1 # square r

        sum_results = [sum(metric) for metric in zip(*cur_results)]
        trial_avgs.append([val / len(cur_results) for val in sum_results])

    return trial_avgs


if __name__ == "__main__":
    print(run_experiment(1))

