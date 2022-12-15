import random

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

secure_rand_gen = random.SystemRandom()
a = np.random.uniform(-0.01, 0.01, [10000, 10000])
plt.hist(a[0])
plt.show()