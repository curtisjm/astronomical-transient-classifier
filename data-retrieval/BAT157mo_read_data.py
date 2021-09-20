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

# not take the BAT157 month  catalog
import glob
from astropy.io import fits

data_dir = "./BAT_157m_eight_band_monthly_lightcurve"

file_list = glob.glob(data_dir + "/*.lc")

"""
[
    [[Time, ...], [Rate, ...], [RateError, ...]],
    [Name, ...],
    [[RaObj, DecObj], ...]
]
"""
data1 = [[], [], []]

for a in file_list:
    file1 = fits.open(a, memmap=True)
    time = file1[1].data["TIME"]
    rate = file1[1].data["RATE"]
    rate_error = file1[1].data["RATE_ERR"]
    name = file1[1].data["NAME"][0]
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

print()
print(
    f"Time: {data1[0][0][0][0]}    Rate: {data1[0][0][0][1]}    Rate Error: {data1[0][0][0][2]}"
)
print(f"Name: {data1[1][0]}")
print(f"RaObj: {data1[2][0][0]}    DecObj: {data1[2][0][1]}")
print()
