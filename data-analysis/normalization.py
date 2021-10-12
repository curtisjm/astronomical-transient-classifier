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

# convert flux values to floats (a precaution that may not be necessary)
rates = [
    [[float(flux) for flux in e_band] for e_band in rate_matrix]
    for rate_matrix in rates
]

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

# use min-max normalization to convert each value to one between 0 and 1
normalized_rates = []
i = 0
for rate_matrix in rates:
    new_rate_matrix = []
    for e_band in rate_matrix:
        new_eband = []
        for flux in e_band:
            # new_eband.append((float(flux) - stats[i]["mean"]) / stats[i]["variance"])
            new_eband.append(
                (float(flux) - stats[i]["min"]) / (stats[i]["max"] - stats[i]["min"])
            )
        new_rate_matrix.append(new_eband)
    normalized_rates.append(new_rate_matrix)
    i += 1

# calculate new statistical values for each object after normalization
norm_stats = []
for rate_matrix in normalized_rates:
    norm_stats.append(
        {
            "min": np.amin(rate_matrix),
            "max": np.amax(rate_matrix),
            "mean": np.mean(rate_matrix),
            "median": np.median(rate_matrix),
            "variance": np.var(rate_matrix),
        }
    )

print(normalized_rates)

# rates_vs_norm_rates(rates, normalized_rates, class_num)
compare_histograms(rates, normalized_rates, class_num)
