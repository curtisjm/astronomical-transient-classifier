import numpy as np

from plotting import *
from utils import *

data = np.load("bat_data1.npy", allow_pickle=True, fix_imports=False)

# display histograms of Supernova Remnants
plot_histograms_by_class(data, "19")
