import numpy as np

from plotting import *


# get stats about each rate matrix
def get_stats(rates):
    return [
        {
            "min": np.amin(rates_matrix),
            "max": np.amax(rates_matrix),
            "mean": np.mean(rates_matrix),
            "median": np.median(rates_matrix),
            "variance": np.var(rates_matrix),
        }
        for rates_matrix in rates
    ]


# normalize all of the rates in our original data object
def get_normalized_rates(data):
    rates = [data[0][i][1] for i in range(len(data[0]))]
    stats = get_stats(rates)

    normalized_rates = []
    i = 0
    for rate_matrix in rates:
        new_rate_matrix = []
        for e_band in rate_matrix:
            new_eband = []
            for flux in e_band:
                new_eband.append(
                    (float(flux) - stats[i]["min"])
                    / (stats[i]["max"] - stats[i]["min"])
                )
            new_rate_matrix.append(new_eband)
        normalized_rates.append(new_rate_matrix)
        i += 1
    return normalized_rates

    # for i in range(len(data[0])):
    #     stats = get_stats(data[0][i][1])
    #     for e_band in data[0][i][1]:
    #         for flux in e_band:
    #             flux = (float(flux) - stats["min"]) / (stats["max"] - stats["min"])


# put all rate matrices into their own array
# rates = []
# for i in range(len(data[3])):
#     if data[3][i] == class_num:
#         rates.append(data[0][i][1])

# convert flux values to floats (a precaution that may not be necessary)
# rates = [
#     [[float(flux) for flux in e_band] for e_band in rate_matrix]
#     for rate_matrix in rates
# ]

# calculate statistical values for each object

# use min-max normalization to convert each value to one between 0 and 1
# normalized_rates = []
# i = 0
# for rate_matrix in rates:
#     new_rate_matrix = []
#     for e_band in rate_matrix:
#         new_eband = []
#         for flux in e_band:
#             # new_eband.append((float(flux) - stats[i]["mean"]) / stats[i]["variance"])
#             new_eband.append(
#                 (float(flux) - stats[i]["min"]) / (stats[i]["max"] - stats[i]["min"])
#             )
#         new_rate_matrix.append(new_eband)
#     normalized_rates.append(new_rate_matrix)
#     i += 1

# rates_vs_norm_rates(rates, normalized_rates, class_num)
# compare_histograms(rates, normalized_rates, class_num)
