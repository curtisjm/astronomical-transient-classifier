import numpy as np
from sklearn.preprocessing import normalize

from plotting import *

data = np.load("bat_data1.npy", allow_pickle=True, fix_imports=False)

# supernova remnants
class_num = "19"

# put all rate matrices into their own array
rates = []
for i in range(len(data[3])):
    if data[3][i] == class_num:
        rates.append(data[0][i][1])

for rate_matrix in rates:
    rate_matrix = normalize(rate_matrix)

print(rates)

plot_rates_images(rates, class_num)
