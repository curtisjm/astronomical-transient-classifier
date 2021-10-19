from matplotlib.pyplot import hist
import numpy as np

from plotting import *
from utils import *
from normalization import *
from augmentation import *

data = np.load("bat_data1.npy", allow_pickle=True, fix_imports=False)
print(data[0][0][1])

norm_rates = get_normalized_rates(data)

for i in range(len(data[0])):
    data[0][i][1] = np.matrix(norm_rates[i])

# plot_images_by_class(data, "19")
print(data[0][0][1])

np.save("bat_data1_normalized.npy", data, allow_pickle=True, fix_imports=False)
