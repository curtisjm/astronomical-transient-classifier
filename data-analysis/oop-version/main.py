import pickle
import numpy as np
from plotting import *

# with open("../pickles/aug_labels_rates.pickle") as f:
#     rates_labels = pickle.load(f)

# print(data[0].name)

rates_labels = np.load(
    "../npy-arrays/aug_rates_labels.npy", allow_pickle=True, fix_imports=False
)

# rates = [x[0] for x in rates_labels]

plot_rates_images([x[0] for x in rates_labels], "19")

# print(rates_labels[0][1])
