# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# As first  example we  plan to  augment the BAT157
# month source catalog  thourgh simple iteration over the data
#  bootstrapping an error fluctuation

# we refer to this blog: https://towardsdatascience.com/time-series-bootstrap-in-the-age-of-deep-learning-b98aa2aa32c4
# https://github.com/cerlymarco/MEDIUM_NoteBook/blob/master/TimeSeries_Bootstrap/TimeSeries_Bootstrap.ipynb
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
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

cosmo = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)


## label making
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


# step 1,  iterate over the 1526 objects that matched the 157 month catalog with the files names
# step 2, for each object extract one band lc and normalize them dividin by the max
# step 3, bootstrap that lightcurve and place is in the new simulated object with the correct label

# function creating the simulated data
def boot_sim(obj, nsamp, r, c):
    # print(obj)
    new_sample = np.empty([nsamp, r, c])
    # print(new_sample.shape)
    for j in range(r):
        raw = obj[j]
        # print(raw)
        # operate bootstrap
        bts = BootstrappingWrapper(
            ConvolutionSmoother(window_len=6, window_type="ones"),
            bootstrap_type="mbb",
            block_length=5,
        )
        bts_samples = bts.sample(raw, n_samples=nsamp)
        for i in range(nsamp):
            # print(new_sample[i][j].shape)
            # print(bts_samples.T.shape)

            new_sample[i][j] = bts_samples[i]
    return new_sample


####################################  DONE WITH IMPORT AND FUNCTIONS

## Create the labels
# Read the URL table:
from urllib import request

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


######################  CREATE THE FILE LIST

data_dir = "/Users/acucchiara/COM/proposal/SRP2021/work/BAT/BAT_157m_eight_band_monthly_lightcurve"
# on cori
# data_dir='/global/homes/n/nino_lbl/Data/BAT/BAT_157m_eight_band_monthly_lightcurve'


file_list = glob.glob(data_dir + "/*.lc")
# print(file_list[0:5])


##########################################    matching of the filelist and website table
newbnames = np.array([x[6:] for x in bnames])  # names in the website
newfin = np.array([x[-15:-3] for x in file_list])  # names in the list of files
# print(type(newbnames),type(newfin))
match = []
for i in range(len(newbnames)):
    s = np.where(newfin == newbnames[i])
    # print(s[0][0])
    try:
        match.append([s[0][0], tp[i]])
    except:
        # print('%s is not in the list' % str(i))
        pass
# print(len(match))
# print(match[0])
# print(file_list[match[0][0]])

##########################################   END  matching of the filelist and website table

#  data1=[[triplet],[name],[coord],[label]]
data1 = [[], [], [], []]
namobj = []
for i in range(len(match)):
    a = file_list[match[i][0]]
    namobj.append(newbnames[match[i][0]])
    rate150 = []
    rate150er = []

    file1 = fits.open(a, memmap=True)
    Time = file1[1].data["TIME"]
    # we could not use CENT_RATE (see Amy Lien emails) and then sum all bands
    #
    Rate = file1[1].data["RATE"]
    Rateerror = file1[1].data["RATE_ERR"]
    Name = file1[1].data["NAME"][0]
    Raobj = file1[1].data["RA_OBJ "][0]
    Decobj = file1[1].data["DEC_OBJ"][0]
    file1.close()
    #################

    # This is necessary because the rate is a 9 element array,
    # divide by energy blocks
    rate150 = [np.sum(x, axis=0) for x in Rate]
    rate150er = [np.sqrt(np.sum(np.square(x))) for x in Rateerror]
    # print(np.shape(rate150))
    # print(len(rate150))
    # data1[0].append([Time,rate150,rate150er])

    ####  We keep all 9 bands:
    # 14-20,20-24,24-35,35-50,50-75,75-100,100-150,150-195, and total counts/s
    # keV
    # we store the transpose of the Rate/error so  that the last raw is the total count

    ##############   Let's cut the matrx from 1-8 raws and 1-155 columns
    rate_new = Rate.T[:-1]
    rate_ErrNew = Rateerror.T[:-1]
    if rate_new.shape[1] >= 155:
        # print(rat_new.shape)
        # print(rate_new[:,:155])
        data1[0].append([Time[:155], rate_new[:, :155], rate_ErrNew[:, :155]])
    else:
        print("Some object has less than 155 observations")

    data1[1].append(Name)
    data1[2].append([Raobj, Decobj])
    data1[3].append(make_label(match[i][1]))

print("Checking the size of the arrays and their shapes\n")
print(len(data1[0]), len(file_list))
print(data1[0][0][1].shape)  ### >>>>>  8 raws, 155 columns

print("------>  Creating the simulated datasets   <------\n")
# step 1,  iterate over the 1628 object
# step 2, for each object extract one band lc
# step 3, bootstrap that lightcurve and place is in the new simulated object
#

# simulated data go here:
#######################   simulation of data
sim_sam = []
lab = []  ## >>> labels
nobj = 2

for i in range(len(data1[0])):
    mat = data1[0][i][1]
    # print(mat[0])
    s = boot_sim(mat * 1e4, nobj, 8, 155)
    label = int(data1[3][i])
    for j in range(nobj):
        # sim_sam.append([sim_sam,np.array(s[j]).flatten(),label])
        sim_sam = np.append(sim_sam, np.array(s[j]).flatten())
        lab.append(label)

# print(sim_sam.shape)
print(8 * 155 * nobj * len(data1[0]))


q = np.reshape(sim_sam * 1e-4, (nobj * len(data1[0]), 8, 155))
print(q[0].shape)
export_arr = []

# np.savez('BAT150_sim10_wl6_bl_5.npz', image=q,labels=lab)
###


# print('Look at some examples')
for i in range(10, 30):
    fig, ax = plt.subplots()
    plt.imshow(q[i] * 1e5, cmap="gray")
    plt.imshow(np.array(data1[0][i][1]) * 1e5, cmap="gray")
plt.show()
