import matplotlib.pyplot as plt
import numpy as np

from utils import *

# plot images of all objects of a given class
def plot_images_by_class(data, class_num):
    rates = []
    # names = []
    # put all rate matrices into their own array
    for i in range(len(data[3])):
        if data[3][i] == class_num:
            rates.append(data[0][i][1])
            # names.append(data[1][i])
    # plot each element in the rates array
    for i in range(len(rates)):
        plt.subplot(len(rates), 1, i + 1)
        plt.imshow(np.array(rates[i]) * 1e5, cmap="gray")
        # plt.title(names[i])
        if i == 0:
            plt.title(
                label=get_class_name(class_num),
                fontdict={"fontsize": "30"},
                pad=35,
            )
    plt.show()


# display histograms for each object of a given class
def plot_histograms_by_class(data, class_num):
    rates = []
    # put all rate matrices into their own array
    for i in range(len(data[3])):
        if data[3][i] == class_num:
            rates.append(data[0][i][1])

    for i in range(len(rates)):
        plt.subplot(len(rates), 1, i + 1)
        plt.hist(rates[i])
        # plt.title(names[i])
        if i == 0:
            plt.title(
                label=get_class_name(class_num),
                fontdict={"fontsize": "30"},
                pad=35,
            )
    plt.show()


def plot_rates_histogram(rates):
    for i in range(len(rates)):
        plt.subplot(len(rates), 1, i + 1)
        plt.hist(rates[i])
    plt.show()


def plot_rates_images(rates, class_num):
    for i in range(len(rates)):
        plt.subplot(len(rates), 1, i + 1)
        plt.imshow(np.array(rates[i]) * 1e5, cmap="gray")
        # plt.title(names[i])
        if i == 0:
            plt.title(
                label=get_class_name(class_num),
                fontdict={"fontsize": "30"},
                pad=35,
            )
    plt.show()
