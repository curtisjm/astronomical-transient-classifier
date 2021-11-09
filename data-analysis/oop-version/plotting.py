import matplotlib.pyplot as plt
import numpy as np

from utils import *


# plot images of all objects of a given class
def plot_images_by_class(data, class_num="0"):
    rates = []
    # put all rate matrices into their own array
    for i in range(len(data)):
        if data[i].label == class_num:
            rates.append(data[i].rates)

    len_plt = len(rates) if len(rates) <= 8 else 8
    # plot each element in the rates array
    for i in range(len_plt):
        plt.subplot(len_plt, 1, i + 1)
        plt.imshow(np.array(rates[i]) * 1e5, cmap="gray")
        if i == 0:
            plt.title(
                label=get_class_name(class_num),
                fontdict={"fontsize": "30"},
                pad=35,
            )
    plt.show()
