from matplotlib.pyplot import hist
import numpy as np

from plotting import *
from utils import *
from normalization import *
from augmentation import *

data = np.load("./npy-arrays/bat_data1_normalized.npy", allow_pickle=True, fix_imports=False)

augment_data_by_class(data, "19")
