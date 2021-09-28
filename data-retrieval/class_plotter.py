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

import glob
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

cosmo = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)

# label making
def make_label(val):
    if (
        val == "Sy1.9"
        or val == "Sy1.2"
        or val == "Sy1.5"
        or val == "Sy1.8"
        or val == "Sy1"
    ):
        val = "1"
    elif val == "Beamed AGN":
        val = "2"
    elif val == "Compact group of gal":
        val = "3"
    elif val == "Galactic Center" or val == "GC":
        val = "4"
    elif val == "Galaxy Cluster":
        val = "5"
    elif val == "Gamma-ray source":
        val = "6"
    elif val == "Open star cluster":
        val = "7"
    elif val == "Sy1;broad-line AGN":
        val = "8"
    elif val == "Unknown AGN":
        val = "9"
    elif val == "molecular cloud":
        val = "10"
    elif val == "Starburst galaxy":
        val = "11"
    elif val == "Sy2 candidate":
        val = "12"
    elif val == "Symbiotic star":
        val = "13"
    elif val == "Pulsar":
        val = "14"
    elif val == "Sy2":
        val = "15"
    elif val == "U1":
        val = "16"
    elif val == "U2":
        val = "17"
    elif val == "U3":
        val = "18"
    elif val == "SNR":
        val = "19"
    elif val == "HMXB":
        val = "20"
    elif val == "CV":
        val = "21"
    elif val == "LMXB":
        val = "22"
    elif val == "XRB":
        val = "23"
    elif val == "Nova":
        val = "24"
    elif val == "star":
        val = "25"
    elif val == "multiple":
        val = "26"
    elif val == "LINER":
        val = "27"
    return val


data_dir = "./bat_157mo_eight_band_monthly_lightcurve"

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

    # cut the matrix from 1-8 raws and 1-155 columns
    rate_new = rate.T[:-1]
    rate_err_new = rate_error.T[:-1]
    if rate_new.shape[1] >= 155:
        data1[0].append([time[:155], rate_new[:, :155], rate_err_new[:, :155]])
    else:
        print("Some object has less than 155 observations")

    data1[1].append(name)
    data1[2].append([ra_obj, dec_obj])
