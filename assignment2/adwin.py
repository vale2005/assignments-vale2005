"""

Purpose:
    Implementation of the ADWIN algorithm. The thresholding is not working
    properly. It is implemented according to the paper, but when the window
    size is large, the threshold is over 1, which makes no sense, since the
    range of values in the stream is expected to be between [0,1]

input:
    - stream: an iterable of numbers between [0,1]
    - confidence: a float between [0, 1]

output:
    the plot of the window size over time

dependency:
    numpy, pyplot from matplotlib and the math and statistics module

"""
import numpy as np
import statistics as st
import math
from matplotlib import pyplot as plt


def adwin(stream, confidence=0.9):
    win_sizes = []
    initial_window_size = 10
    window = stream[:initial_window_size].tolist()
    for item in stream[initial_window_size:]:
        window.append(item)
        keep_cutting = True
        while keep_cutting:
            split_idx = 1
            # the additional condition is to check if we have gone
            # through the whole window
            while keep_cutting & (split_idx < len(window)):
                w0 = window[:split_idx]
                w1 = window[split_idx:]
                m = 1./(1./len(w0) + 1./len(w1))
                delta = confidence / len(window)
                cut = math.sqrt((1./(2.*m)) * math.log(4./delta))

                keep_cutting = abs(st.mean(w0)-st.mean(w1)) >= cut
                split_idx += 1
                print(cut)
            if keep_cutting:
                window.pop(0)
        win_sizes.append(len(window))
    return win_sizes


# uniform random
s1 = np.random.random(100)
mini = np.min(s1)
maxi = np.max(s1)
# shrink values between 0.7 and 0.9
s1 = np.apply_along_axis(lambda x: (x-mini)/(maxi-mini)*0.2 + 0.7, 0, s1)
print(s1.mean())

# normal dist
s2 = np.random.randn(200)
mini = np.min(s2)
maxi = np.max(s2)
# shrink values between 0.1 and 0.4
s2 = np.apply_along_axis(lambda x: (x-mini)/(maxi-mini)*0.3 + 0.1, 0, s2)
print(s2.mean())

stream = np.concatenate((s1, s2))
w1 = adwin(stream, 0.9)

plt.title("Window size over time")
plt.xlabel("Timestamp")
plt.ylabel("Size of window")
plt.plot(np.arange(10, stream.size), w1)
plt.show()