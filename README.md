# bit-sampling
This repo contains an implementation of bit sampling for Hamming distance, a straightforward technique for [Locality-Sensitive Hashing](https://en.wikipedia.org/wiki/Locality-sensitive_hashing#Bit_sampling_for_Hamming_distance). Here, bit sampling is used to solve the c-approximate nearest neighbor problem.

The code for the bit sampler in  `Sampler.py` is based off of these Penn State [lecture notes](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.712.8703&rep=rep1&type=pdf).

By introducing some randomness, and accepting some loss of precision (hence, approximate search), bit sampling can query for nearest neighbors "quite fast." As speed is relative, I decided to compare my sampler with [Spotify's Annoy API](https://github.com/spotify/annoy) to more precisely gauge how well it performs.

## How to Run
`python3 Trial.py` will simulate one experiment (takes about 1 minute to execute).

### Sample Output
```
1 trials simulated for each valid configuration of d, r, and c
Each trial attempted to query 10 elements from a data set of size 1000
----------------------------------------------------------------------------------------------------
Results for d = 8 ( 4  total trials )
Average execution time PER QUERY:
c-approximate: 4.78 ms
Annoy: 13.31 ms
Average accuracy of c-approximate: 31.44 %
Percent of c-approximate queries which returned at least one neighbor: 100.0 %
----------------------------------------------------------------------------------------------------
Results for d = 16 ( 18  total trials )
Average execution time PER QUERY:
c-approximate: 6.48 ms
Annoy: 11.63 ms
Average accuracy of c-approximate: 54.04 %
Percent of c-approximate queries which returned at least one neighbor: 96.11 %
----------------------------------------------------------------------------------------------------
Results for d = 32 ( 38  total trials )
Average execution time PER QUERY:
c-approximate: 12.78 ms
Annoy: 13.75 ms
Average accuracy of c-approximate: 49.0 %
Percent of c-approximate queries which returned at least one neighbor: 93.42 %
----------------------------------------------------------------------------------------------------
Results for d = 64 ( 77  total trials )
Average execution time PER QUERY:
c-approximate: 26.57 ms
Annoy: 19.85 ms
Average accuracy of c-approximate: 50.98 %
Percent of c-approximate queries which returned at least one neighbor: 93.51 %
```

## Measuring Performance
Each simulation iterates through various configurations for `d` (the bitlength of integers), `r` (the distance of "close" points), and `c` (the approximation factor such that query `q` is approximately close to data point `x` if `hamming(q,x) <= c*r`.

**Note:** An invalid coniguration of `(d,r,c)` is one which results in a mathematical error when initializing the `Sampler` object, since other attributes are functions of these three parameters; see the `assert` statements in  `Sampler.py` for more detail.

For each vaild `(d,r,c)`, the simulation performs `num_trials=1` trial(s), attempting to query `query_size=10` item from a data set of `data_size=1000` randomly generated `d`-bit integers. Once all trials are completed (note that some may have exited prematurely if our randomized sampler failed to query for any neighbors), we average the total query time for our sampler, as well as Spotify's Annoy.

Annoy returns the exact (i.e. not approximate) `k` nearest neighbors. We therefore record the average "accuracy" of our sampler after the trials. I.e., how many of the `k` neighbors returned by our solver also appeared in the exact `k` nearest neighbors from Annoy? Simply, accuracy tells us what percent of the approximate neighbors were also exact solutions.

Lastly, we record the percent of queries which were successful. As noted above, it is possible for the sampler (due to randomness) to miss completely, and return no neighbors for some queries.

## Improvements
- Currently, `num_trials`, `query_size`, and `data_size` are hard-coded in `main` in `Trial.py`, for quick-and-dirty testing, but these should be command-line arg parameters
- Allow for users to use their own data files, instead of only randomly generated ones.

## Misc. Remarks
Interestingly, Annoy has a hard time handling 64-bit integers. As a workaround, I encoded each `d`-bit integer as a length-`d` array of bits.

## Conclusion
From the above sample output, we can see that, per query, our sampler performs comparably (usually even faster) than Annoy. Our sampler is also able to find at least one approximate neighbor >90% of the time. However, the low accuracy shows that typically only about 40% of solutions found are exact.

I've attempted to standardize the trials as much as possible to better understand the tradeoffs between approximate and exact solvers. Ultimately, it seems by allowing for some approximation factor, we can query for neighbors quite quickly, with a comfortably low fail rate (a query "fails" if no neighbor is found) of <10%.

Note that probabilistic failure can be further reduced by configuring the `numerator` variable in `Sampler.__init__()`, though this will of course impact runtime performance. Briefly explaining, increasing the numerator  increases the total number of buckets into which elements of the data sets are hashed. This means that data points are hashed less sparsely.

See `Section 5.2 - Analysis` of the above PSU paper, particularly the analysis of a missed query occurring with probability `1/e`, which can be reduced arbitrarily low.
