from matplotlib.pyplot import hist
import numpy as np

from plotting import *
from utils import *
from normalization import *
from augmentation import *

data = np.load(
    "./npy-arrays/bat_data1_normalized.npy", allow_pickle=True, fix_imports=False
)

aug_data = augment_class(data, "19")
plot_rates_images([aug_data[0][i][1] for i in range(len(aug_data[0]))])
