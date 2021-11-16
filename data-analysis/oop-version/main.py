import pickle
import numpy as np
from plotting import *

# with open("../pickles/bat_data.pickle") as f:
#     data = pickle.load(f)

# print(data[0].name)

rates_labels = np.load(
    "../npy-arrays/bat_data1_normalized.npy", allow_pickle=True, fix_imports=False
)

# plot_rates_images([r_l[0] for r_l in rates_labels], "19")

print(rates_labels[0][1])
