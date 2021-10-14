import matplotlib.pyplot as plt
import numpy as np

from utils import *

# plot images of all objects of a given class
def plot_images_by_class(data, class_num="0"):
    rates = []
    # put all rate matrices into their own array
    for i in range(len(data[3])):
        if data[3][i] == class_num:
            rates.append(data[0][i][1])
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


# display histograms for each object of a given class
def plot_histograms_by_class(data, class_num="0"):
    rates = []
    # put all rate matrices into their own array
    for i in range(len(data[3])):
        if data[3][i] == class_num:
            rates.append(data[0][i][1])

    for i in range(len(rates)):
        plt.subplot(len(rates), 1, i + 1)
        plt.hist(rates[i])
        if i == 0:
            plt.title(
                label=get_class_name(class_num),
                fontdict={"fontsize": "30"},
                pad=35,
            )
    plt.show()


# flatten each rates matrix in an array of objects
def flatten_rates(rates):
    rates = np.array(rates)
    return [rate_matrix.flatten() for rate_matrix in rates]


# plot the histogram of a given array of rate matrices
def plot_rates_histogram(rates):
    rates = flatten_rates(rates)
    for i in range(len(rates)):
        plt.subplot(len(rates), 1, i + 1)
        plt.hist(rates[i])
    plt.show()


# compare the histograms of objects before and after normalization
def compare_histograms(rates, norm_rates, class_num="0"):
    if len(rates) != len(norm_rates):
        print(
            "Lengths of rates and normalized rates arrays are not equal. Aborting display of images."
        )
        return
    rates = flatten_rates(rates)
    norm_rates = flatten_rates(norm_rates)

    fig, axs = plt.subplots(len(rates), 2)
    for i in range(len(rates)):
        axs[i][0].hist(rates[i])
        axs[i][1].hist(norm_rates[i])

    axs[0][0].set_title(
        label="Original Rates",
        fontdict={"fontsize": "15"},
        pad=20,
    )
    axs[0][1].set_title(
        label="Normalized Rates",
        fontdict={"fontsize": "15"},
        pad=20,
    )
    fig.suptitle(
        get_class_name(class_num),
        fontsize=30,
    )
    plt.show()


# plot the image representations of the rates for a single object
def plot_rates_images(rates, class_num="0"):
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


# compare the images of the original rates measurements to the normalized values
def rates_vs_norm_rates(rates, norm_rates, class_num="0"):
    if len(rates) != len(norm_rates):
        print(
            "Lengths of rates and normalized rates arrays are not equal. Aborting display of images."
        )
        return

    length = 10 if len(rates) > 10 else len(rates)

    fig, axs = plt.subplots(length, 2)
    for i in range(length):
        axs[i][0].imshow(np.array(rates[i]) * 1e5, cmap="gray")
        axs[i][1].imshow(np.array(norm_rates[i]) * 1e5, cmap="gray")

    axs[0][0].set_title(
        label="Original Rates",
        fontdict={"fontsize": "15"},
        pad=20,
    )
    axs[0][1].set_title(
        label="Normalized Rates",
        fontdict={"fontsize": "15"},
        pad=20,
    )
    fig.suptitle(
        get_class_name(class_num),
        fontsize=30,
    )
    plt.show()
