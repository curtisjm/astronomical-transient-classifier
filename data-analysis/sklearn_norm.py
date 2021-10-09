import numpy as np
from sklearn.preprocessing import normalize

from plotting import *

data = np.load("bat_data1.npy", allow_pickle=True, fix_imports=False)

# supernova remnants
class_num = "19"

# put all rate matrices into their own array
rates = []
for i in range(len(data[3])):
    if data[3][i] == class_num:
        rates.append(data[0][i][1])

# convert flux values to floats (a precaution that may not be necessary)
rates = [
    [[float(flux) for flux in e_band] for e_band in rate_matrix]
    for rate_matrix in rates
]

normalized_rates = [normalize(rate_matrix) for rate_matrix in rates]

print(normalized_rates)

rates_vs_norm_rates(rates, normalized_rates, class_num)
