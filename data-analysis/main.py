from matplotlib.pyplot import hist
import numpy as np

from plotting import *
from utils import *

data = np.load("bat_data1.npy", allow_pickle=True, fix_imports=False)

# display histograms of Supernova Remnants
# plot_histograms_by_class(data, "19")

class_num = "19"

rates = []
for i in range(len(data[3])):
    if data[3][i] == class_num:
        rates.append(data[0][i][1])

plot_rates_histogram(rates)
