import os
import glob
import random
import numpy as np
import pandas as pd
import seaborn as sns
import astropy.units as u
import matplotlib.pyplot as plt
import pandas.util.testing as tm
from urllib import request
from tsmoothie.smoother import *
from tsmoothie.bootstrap import BootstrappingWrapper
from tsmoothie.utils_func import create_windows, sim_seasonal_data, sim_randomwalk
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM

cosmo = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)

labels = {
    "Sy1": "1",
    "Sy1.2": "1",
    "Sy1.5": "1",
    "Sy1.8": "1",
    "Sy1.9": "1",
    "Beamed AGN": "2",
    "Compact group of gal": "3",
    "Galactic Center": "4",
    "GC": "4",
    "Galaxy Cluster": "5",
    "Gamma-ray source": "6",
    "Open star cluster": "7",
    "Sy1;broad-line AGN": "8",
    "Unknown AGN": "9",
    "molecular cloud": "10",
    "Starburst galaxy": "11",
    "Sy2 candidate": "12",
    "Symbiotic star": "13",
    "Pulsar": "14",
    "Sy2": "15",
    "U1": "16",
    "U2": "17",
    "U3": "18",
    "SNR": "19",
    "HMXB": "20",
    "CV": "21",
    "LMXB": "22",
    "XRB": "23",
    "Nova": "24",
    "star": "25",
    "multiple": "26",
    "LINER": "27",
}


def get_class_name(class_num):
    keys = list(labels.keys())
    values = list(labels.values())
    pos = values.index(class_num)
    return keys[pos]


def make_label(val):
    return labels[val]


def plot_by_class(data, class_num):
    # rates = []
    # for i in range(len(data[3])):
    #     if int(data[3][i]) == class_num:
    #         rates.append(data[0][i][1])
    # print(rates)
    print(f"0: {len(data[0])}")
    print(f"3: {len(data[3])}")


table_157mo = pd.read_html("https://swift.gsfc.nasa.gov/results/bs157mon/", match=".+")
df = table_157mo[1]

sub_class = df[
    [
        "BAT Name (a)",
        "Counterpart Name",
        "Class (j)",
        "Type",
        "RA (b)",
        "Dec",
        "Redshift (g)",
    ]
]
tp = sub_class["Type"].values
names = sub_class["Counterpart Name"].values
rah, dech = sub_class["RA (b)"].values, sub_class["Dec"].values
bnames = sub_class["BAT Name (a)"].values
z = sub_class["Redshift (g)"].values
z[np.isnan(z)] = 0.0
ld = cosmo.luminosity_distance(z).value * 1e6

data_dir = "./bat_157mo_eight_band_monthly_lightcurve"

file_list = glob.glob(data_dir + "/*.lc")
# print(file_list[0:5])


# matching of the filelist and website table
# names in the website
new_bnames = np.array([x[6:] for x in bnames])
# names in the list of files
newfin = np.array([x[x.index("J") : -3] for x in file_list])
# print(type(new_bnames),type(newfin))
match = []
for i in range(len(new_bnames)):
    s = np.where(newfin == new_bnames[i])
    # print(s[0][0])
    try:
        match.append([s[0][0], tp[i]])
    except:
        # print("%s is not in the list" % str(i))
        pass
# print(len(match))
# print(match[0:3])
# print(match[0])
# print(file_list[match[0][0]])

"""
[
    [[Times1[], Rates1[][], RateErrors1[][]], ...],
    [Name1, ...],
    [[RaObj1, DecObj1], ...],
    [Label1, ...]
]
"""
data1 = [[], [], [], []]
namobj = []

for i in range(len(match)):
    a = file_list[match[i][0]]
    namobj.append(new_bnames[match[i][0]])
    rate150 = []
    rate150er = []

    file1 = fits.open(a, memmap=True)
    time = file1[1].data["TIME"]
    rate = file1[1].data["RATE"]
    rate_error = file1[1].data["RATE_ERR"]
    name = file1[1].data["NAME"][0]
    ra_obj = file1[1].data["RA_OBJ "][0]
    dec_obj = file1[1].data["DEC_OBJ"][0]
    file1.close()

    # this is necessary because the rate is a 9 element array,
    # divide by energy blocks
    rate150 = [np.sum(x, axis=0) for x in rate]
    rate150er = [np.sqrt(np.sum(np.square(x))) for x in rate_error]
    # print(np.shape(rate150))
    # print(len(rate150))
    # data1[0].append([time,rate150,rate150er])

    # we keep all 9 bands:
    # 14-20,20-24,24-35,35-50,50-75,75-100,100-150,150-195, and total counts/s
    # keV
    # we store the transpose of the rate/error so  that the last raw is the total count

    # cut the matrix from 1-8 raws and 1-155 columns
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
    data1[3].append(make_label(match[i][1]))

print("Checking the size of the arrays and their shapes\n")
print(len(data1[0]), len(data1[3]))
# 8 raws, 155 columns
print(data1[0][0][1].shape)

plot_by_class(data1, 1)
