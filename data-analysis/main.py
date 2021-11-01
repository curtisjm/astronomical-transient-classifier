from matplotlib.pyplot import hist
import numpy as np

from plotting import *
from utils import *
from normalization import *
from augmentation import *

data = np.load(
    "./npy-arrays/bat_data1_normalized.npy", allow_pickle=True, fix_imports=False
)

aug_data = augment_all_data(data)
# plot_images_by_class(aug_data, "19")
