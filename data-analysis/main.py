import numpy as np

data1 = np.load("bat_data1.npy", allow_pickle=True, fix_imports=False)

print(data1[1][0])
