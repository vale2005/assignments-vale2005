# naive implementation of the count-min sketch algorithm

import numpy as np
import pandas as pd
import mmh3

characters = list("ABCDEFGHIJKLMNOP")
stream = np.random.choice(list("ABCDEFGHIJKLMNOP"), 10000)

num_hashfuns=20
num_buckets=11

# init seeds equal to the number of buckets
hash_seeds = np.random.randint(1, 1000, num_hashfuns)

# init sketch
sketch = pd.DataFrame(np.zeros((num_hashfuns, num_buckets)))

# process items
for ch in stream:
    for hash_fun in range(num_hashfuns):
        bucket = mmh3.hash(ch, seed=hash_seeds[hash_fun]) % num_buckets
        sketch.loc[hash_fun, bucket] += 1

print(sketch)

# return minimum counts for each item
counts = dict()
for ch in characters:
    for hash_fun in range(num_hashfuns):
        bucket = mmh3.hash(ch, seed=hash_seeds[hash_fun]) % num_buckets
        if ch in counts:
            hash_count = sketch.loc[hash_fun, bucket]
            if hash_count < counts[ch]:
                counts[ch] = hash_count
        else:
            counts[ch] = sketch.loc[hash_fun, bucket]

print(counts)
print(sum(counts.values()))
