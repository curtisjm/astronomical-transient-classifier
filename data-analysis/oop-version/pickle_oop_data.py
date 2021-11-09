import numpy as np
import pickle

from Transient import Transient
from plotting import *
from augmentation import *

data = np.load(
    "../npy-arrays/bat_data1_normalized.npy", allow_pickle=True, fix_imports=False
)

new_data = [
    Transient(
        times=data[0][i][0],
        rates=data[0][i][1],
        rate_errors=data[0][i][2],
        name=data[1][i],
        ra_dec=data[2][i],
        label=data[3][i],
    )
    for i in range(len(data[0]))
]


# with open("../pickles/bat_data.pickle", "wb") as f:
#     pickle.dump(new_data, f)

# plot_images_by_class(new_data, "19")

aug_data = augment_snr(new_data)
print(aug_data[10].rates)

plot_images_by_class(aug_data, "19")
