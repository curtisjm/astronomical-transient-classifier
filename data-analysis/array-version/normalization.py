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
# uses min max normalization
# only normalizes the rates, not any other part of the data
# will have to update the rates in the original data object after using this function. see example below
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


#   norm_rates = get_normalized_rates(data)
#   for i in range(len(data[0])):
#       data[0][i][1] = np.matrix(norm_rates[i])
