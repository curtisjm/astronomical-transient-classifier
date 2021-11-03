import matplotlib.pyplot as plt
import numpy as np

from utils import *

# plot images of all objects of a given class
def plot_images_by_class(data, class_num="0"):
    rates = []
    # put all rate matrices into their own array
    for i in range(len(data)):
        if data[0].label == class_num:
            rates.append(data[0].rates)
    # plot each element in the rates array
    for i in range(len(rates)):
        plt.subplot(len(rates), 1, i + 1)
        plt.imshow(np.array(rates[i]) * 1e5, cmap="gray")
        if i == 0:
            plt.title(
                label=get_class_name(class_num),
                fontdict={"fontsize": "30"},
                pad=35,
            )
    plt.show()
