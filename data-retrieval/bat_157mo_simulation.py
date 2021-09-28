# As first  example we  plan to  augment the BAT157
# month source catalog  thourgh simple iteration over the data
# bootstrapping an error fluctuation

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

data_dir = "./bat_157mo_eight_band_monthly_lightcurve"
# on cori
# data_dir='/global/homes/n/nino_lbl/Data/BAT/BAT_157m_eight_band_monthly_lightcurve'


file_list = glob.glob(data_dir + "/*.lc")
# print(file_list[0:5])

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
    Time = file1[1].data["TIME"]
    # we could use CENT_RATE (see Amy Lien emails) and then sum all bands
    #
    Rate = file1[1].data["RATE"]
    Rateerror = file1[1].data["RATE_ERR"]
    Name = file1[1].data["NAME"][0]
    Raobj = file1[1].data["RA_OBJ "][0]
    Decobj = file1[1].data["DEC_OBJ"][0]
    file1.close()

    ####  We keep all 9 bands:
    # 14-20,20-24,24-35,35-50,50-75,75-100,100-150,150-195, and total counts/s
    # keV
    # we store the transpose of the Rate/error so  that the last raw is the total count

    ##############   Let's cut the matrx from 1-8 raws and 1-155 columns
    rate_new = Rate.T[:-1]
    rate_err_new = Rateerror.T[:-1]
    if rate_new.shape[1] >= 155:
        # print(rat_new.shape)
        # print(rate_new[:,:155])
        data1[0].append([Time[:155], rate_new[:, :155], rate_err_new[:, :155]])
    else:
        print("Some object has less than 155 observations")

    data1[1].append(Name)
    data1[2].append([Raobj, Decobj])

print()
print(
    f"Time: {data1[0][0][0][0]}    Rate: {data1[0][0][0][1]}    Rate Error: {data1[0][0][0][2]}"
)
print(f"Name: {data1[1][0]}")
print(f"RaObj: {data1[2][0][0]}    DecObj: {data1[2][0][1]}")
print()

print("Checking the size of the arrays and their shapes\n")
print(len(data1[0]), len(file_list))
print(data1[0][0][1].shape)  ### >>>>>  8 raws, 155 columns

print("------>  Creating the simulated datasets   <------\n")
# step 1,  iterate over the 1628 object
# step 2, for each object extract one band lc
# step 3, bootstrap that lightcurve and place is in the new simulated object
#

# simulated data go here:
sim_data = []

# function creating the simulated data
def boot_sim(obj, nsamp, r, c):
    # print(obj)
    new_sample = np.empty([nsamp, r, c])
    # print(new_sample.shape)
    for j in range(r):
        raw = obj[j] * 1e5

        # operate bootstrap
        bts = BootstrappingWrapper(
            ConvolutionSmoother(window_len=4, window_type="ones"),
            bootstrap_type="mbb",
            block_length=5,
        )
        bts_samples = bts.sample(raw, n_samples=nsamp)
        for i in range(nsamp):
            # print(new_sample[i][j].shape)
            # print(bts_samples.T.shape)
            new_sample[i][j] = bts_samples[i] * 1e-5
    return new_sample


sim_sam = []
## Number of  object to simulate
nobj = 2

for i in range(len(data1[0])):
    s = boot_sim(data1[0][i][1], nobj, 8, 155)
    for j in range(nobj):
        sim_sam = np.append(sim_sam, np.array(s[j]).flatten())

###
print("Check the shape of the %i simulated data matrixes" % nobj)
print(sim_sam.shape)
print(8 * 155 * nobj * len(data1[0]))
q = np.reshape(sim_sam, (nobj * len(data1[0]), 8, 155))
print(q.shape)
# np.save('BAT150_sim10_wl4_bl_5.npy', q,allow_pickle=False, fix_imports=False)
###
print("Look at some examples")
for i in range(10):
    fig, ax = plt.subplots()
    # plt.imshow(q[i]*1e5,cmap='gray')
    plt.imshow(np.array(data1[0][i][1]) * 1e5, cmap="gray")
plt.show()
