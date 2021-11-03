from tsmoothie.smoother import *
from tsmoothie.bootstrap import BootstrappingWrapper
from tsmoothie.utils_func import create_windows, sim_seasonal_data, sim_randomwalk

from utils import *


def augment_all_data(data):
    full_aug_data = []

    for label in range(1, 28):
        # copy all the original data from the class
        # will overwrite rates later
        single_class_data = []
        for i in range(len(data)):
            if data[i].label == label:
                single_class_data.append(data[i])

        # augment the data from each class
        aug_data = augment_class(data, label)

        # add the augmented data to the full data
        for obj in aug_data:
            full_aug_data.append(obj)

    return full_aug_data


def augment_class(single_class_data, desired_obj=10):
    # how many total new objects we need
    aug_fact = int(desired_obj / len(single_class_data))

    # class already has enough objects
    if aug_fact < 1:
        return single_class_data

    # start with the original data from the class
    aug_data = single_class_data

    # iterate over objects of the given class
    for obj in single_class_data:
        # augment each object aug_fact times
        for _ in range(aug_fact):
            # iterate over the 8 energy bands
            new_sample = np.empty([8, 155])
            for row in range(8):
                new_sample[row] = aug_single_arr(obj.rates[row])
                temp = obj
                temp.rates = new_sample
                # add to the augmented data
                aug_data.append(temp)

    return single_class_data


def aug_single_arr(arr):
    bts = BootstrappingWrapper(
        ConvolutionSmoother(window_len=6, window_type="ones"),
        bootstrap_type="mbb",
        block_length=5,
    )
    bts_samples = bts.sample(arr)

    return bts_samples
