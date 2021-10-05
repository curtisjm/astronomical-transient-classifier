import numpy as np

from plotting import *

data = np.load("bat_data1.npy", allow_pickle=True, fix_imports=False)

# supernova remnants
class_num = "19"

# put all rate matrices into their own array
rates = []
for i in range(len(data[3])):
    if data[3][i] == class_num:
        rates.append(data[0][i][1])

# calculate statistical values for each object
stats = []
for rate_matrix in rates:
    stats.append(
        {
            "min": np.amin(rate_matrix),
            "max": np.amax(rate_matrix),
            "mean": np.mean(rate_matrix),
            "median": np.median(rate_matrix),
            "variance": np.var(rate_matrix),
        }
    )

# apply normalization calculations to each of the values in the rates array
# normalized_rates = [
#     [
#         [(float(flux) - stats[i]["mean"]) / stats[i]["variance"] for flux in e_band]
#         for e_band in rate_matrix
#     ]
#     for rate_matrix in rates
#     i += 1
# ]
normalized_rates = []
i = 0
for rate_matrix in rates:
    for e_band in rate_matrix:
        for flux in e_band:
            normalized_rates.append(
                (float(flux) - stats[i]["mean"]) / stats[i]["variance"]
            )
    i += 1

print(normalized_rates)

plot_rates_histogram(normalized_rates)
