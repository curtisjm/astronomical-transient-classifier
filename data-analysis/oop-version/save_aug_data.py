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

aug_data = augment_all_data(new_data)
print(aug_data[10].rates)

rates_labels = [[aug_data[i].rates, aug_data[i].label] for i in range(len(aug_data))]

plot_rates_images([x[0] for x in rates_labels], "19")

[print(x[0].shape) for x in rates_labels]

# rates_labels = np.asanyarray(rates_labels)

np.save(
    "../npy-arrays/aug_rates_labels.npy",
    rates_labels,
    allow_pickle=True,
    fix_imports=False,
)

# with open("../pickles/aug_labels_rates.pickle", "wb") as f:
#     pickle.dump(rates_labels, f)
