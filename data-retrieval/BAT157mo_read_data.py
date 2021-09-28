# As first  example we  plan to  augment the BAT157
# month source catalog  though simple iteration over the data
# bootstrapping an error fluctuation

# we refer to this blog: https://towardsdatascience.com/time-series-bootstrap-in-the-age-of-deep-learning-b98aa2aa32c4
# https://github.com/cerlymarco/MEDIUM_NoteBook/blob/master/timeSeries_Bootstrap/timeSeries_Bootstrap.ipynb

import os
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas.util.testing as tm

from tsmoothie.smoother import *
from tsmoothie.bootstrap import BootstrappingWrapper
from tsmoothie.utils_func import create_windows, sim_seasonal_data, sim_randomwalk

# we need to increase the number of files that can be opened
# https://github.com/spacetelescope/drizzlepac/issues/39

# import resource
# resource.setrlimit(resource.RLIMIT_NOFILE, (1000,-1))

import glob

# https://docs.astropy.org/en/stable/io/fits/index.html
from astropy.io import fits

data_dir = "./BAT_157m_eight_band_monthly_lightcurve"

file_list = glob.glob(data_dir + "/*.lc")

"""
Rate, Rate Error:
8 energy bands are measured at the same time each month
[
    e1:[Mo1, Mo2, Mo3, ...],
    e2:[Mo1, Mo2, Mo3, ...],
    e3:[Mo1, Mo2, Mo3, ...],
    ...
]
"""

"""
[
    [[Times1[], Rates1[][], RateErrors1[][]], ...],
    [Name1, ...],
    [[RaObj1, DecObj1], ...]
]
"""
data1 = [[], [], []]

for a in file_list:
    file1 = fits.open(a, memmap=True)
    time = file1[1].data["TIME"]
    rate = file1[1].data["RATE"]
    rate_error = file1[1].data["RATE_ERR"]
    name = file1[1].data["NAME"][0]
    # coordinates
    ra_obj = file1[1].data["RA_OBJ "][0]
    dec_obj = file1[1].data["DEC_OBJ"][0]
    file1.close()

    ####  We keep all 9 bands:
    # 14-20,20-24,24-35,35-50,50-75,75-100,100-150,150-195, and total counts/s
    # keV
    # we store the transpose of the rate/error so  that the last raw is the total count

    # let's cut the matrix from 1-8 raws and 1-155 columns
    rate_new = rate.T[:-1]
    rate_err_new = rate_error.T[:-1]
    if rate_new.shape[1] >= 155:
        # print(rat_new.shape)
        # print(rate_new[:,:155])
        data1[0].append([time[:155], rate_new[:, :155], rate_err_new[:, :155]])
    else:
        print("Some object has less than 155 observations")

    data1[1].append(name)
    data1[2].append([ra_obj, dec_obj])


def graph_first_value():
    # time (MJD)
    x = np.array(data1[0][0][0])
    # rate (Crab)
    rates = np.array(data1[0][0][1])
    rate_errors = np.array(data1[0][0][2])

    for i in range(8):
        y = rates[i]
        y_err = rate_errors[i]

        plt.subplot(8, 1, i + 1)
        plt.scatter(x, y)
        plt.errorbar(x, y, yerr=y_err, fmt="o")
        plt.xlabel("Time (MJD)")
        plt.ylabel("Rate (Crab)")
    plt.show()


def find_min_time():
    min_t = 99999
    for i in range(len(data1[0])):
        if float(data1[0][0][i][0]) < min_t:
            min_t = float(data1[0][0][i][0][0])
    print(f"Min Time: {min_t}")


# graph_first_value()
find_min_time()
