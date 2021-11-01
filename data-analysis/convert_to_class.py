import numpy as np

from Transient import Transient
from augmentation import *

data = np.load(
    "./npy-arrays/bat_data1_normalized.npy", allow_pickle=True, fix_imports=False
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

# [print(obj.name) for obj in new_data]
x = augment_class(data, "19")
print(x)