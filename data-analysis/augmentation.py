from tsmoothie.smoother import *
from tsmoothie.bootstrap import BootstrappingWrapper
from tsmoothie.utils_func import create_windows, sim_seasonal_data, sim_randomwalk
import copy

from utils import *

# min 6000 objects per class


# # step 1,  iterate over the 1526 objects that matched the 157 month catalog with the files names
# # step 2, for each object extract one band lc and normalize them dividing by the max
# # step 3, bootstrap that lightcurve and place is in the new simulated object with the correct label

# # function creating the simulated data
# def boot_sim(obj, nsamp, r, c):
#     # print(obj)
#     new_sample = np.empty([nsamp, r, c])
#     # print(new_sample.shape)
#     for j in range(r):
#         raw = obj[j]
#         # print(raw)
#         # operate bootstrap
#         bts = BootstrappingWrapper(
#             ConvolutionSmoother(window_len=6, window_type="ones"),
#             bootstrap_type="mbb",
#             block_length=5,
#         )
#         bts_samples = bts.sample(raw, n_samples=nsamp)
#         for i in range(nsamp):
#             # print(new_sample[i][j].shape)
#             # print(bts_samples.T.shape)

#             new_sample[i][j] = bts_samples[i]
#     return new_sample


# def augment_data_old(data):
#     sim_sam = []
#     lab = []
#     nobj = 2

#     for i in range(len(data[0])):
#         mat = data[0][i][1]
#         # print(mat[0])
#         s = boot_sim(mat * 1e4, nobj, 8, 155)
#         label = int(data[3][i])
#         for j in range(nobj):
#             # sim_sam.append([sim_sam,np.array(s[j]).flatten(),label])
#             sim_sam = np.append(sim_sam, np.array(s[j]).flatten())
#             lab.append(label)

#     # print(sim_sam.shape)
#     print(8 * 155 * nobj * len(data[0]))

#     q = np.reshape(sim_sam * 1e-4, (nobj * len(data[0]), 8, 155))
#     print(q[0].shape)
#     return q


# def get_augmented_data(data):
#     pass


# # function creating the simulated data
# def new_boot_sim(obj, nsamp, r, c):
#     # print(obj)
#     new_sample = np.empty([nsamp, r, c])
#     # print(new_sample.shape)
#     for j in range(r):
#         raw = obj[j]
#         # print(raw)
#         # operate bootstrap
#         bts = BootstrappingWrapper(
#             ConvolutionSmoother(window_len=6, window_type="ones"),
#             bootstrap_type="mbb",
#             block_length=5,
#         )
#         bts_samples = bts.sample(raw, n_samples=nsamp)
#         for i in range(nsamp):
#             # print(new_sample[i][j].shape)
#             # print(bts_samples.T.shape)

#             new_sample[i][j] = bts_samples[i]
#     return new_sample


def new_augment_data_single_obj(data, class_num, desired_obj=1000):
    aug_fact = 8
    new_sample = np.empty([aug_fact, 8, 155])

    rates = []
    for i in range(len(data[3])):
        if data[3][i] == class_num:
            rates.append(data[0][i][1])

    # aug_fact = desired_obj / len(rates)

    for n_obj in range(len(rates)):  # iterate over SNR objs
        for s in range(len(new_sample)):  # iterate over output matrices
            for row in range(8):
                new_sample[s][row] = aug_single_arr(rates[n_obj][row])

    return new_sample

    """
        checking: compare image (8x155) between XX simulated SNR and the original one
        rates[0][0][1] ----> new_sample[0:7]
    """

    # aug_rates = rates
    # new_rates = []
    # for mat in rates:
    #     for i in range(aug_fact):
    #         new_mat = []
    #         for e_band in mat:
    #             bts = BootstrappingWrapper(
    #                 ConvolutionSmoother(window_len=6, window_type="ones"),
    #                 bootstrap_type="mbb",
    #                 block_length=5,
    #             )
    #             bts_samples = bts.sample(e_band)
    #             new_mat.append(bts_samples)
    #     new_rates.append(new_mat)
    # print(new_rates)
    # return new_rates


# def augment_data_by_class(data, class_num):
#     n_objs = get_num_objects_by_class(data, class_num)
#     aug_fact = 10

#     rates = []
#     for i in range(len(data[3])):
#         if data[3][i] == class_num:
#             rates.append(data[0][i][1])

#     aug_rates = rates
#     for mat in rates:
#         for i in range(aug_fact):
#             new_mat = []
#             for e_band in mat:
#                 new_mat.append(boot_sim(e_band, 1, 8, 155))
#     print(aug_rates)


#######################


def augment_all_data(data):
    pass


def augment_class(data, class_num, desired_obj=1000):
    # copy all the original data from the class
    # will overwrite rates later
    aug_data = []
    for i in range(len(data[3])):
        if data[3][i] == class_num:
            aug_data.append(data[0][i])

    # how many total new objects we need
    aug_fact = int(desired_obj / len(aug_data[0]))
    new_sample = np.empty([aug_fact, 8, 155])

    # iterate over SNR objs
    for n_obj in range(len(data[0])):
        # iterate over output matrices
        for s in range(len(new_sample)):
            # iterate over the 8 energy bands
            for row in range(8):
                # use augmentation function
                new_sample[s][row] = aug_single_arr(aug_data[0][n_obj][1][row])
                # copy the original object data
                temp = data[0][n_obj]
                # overwrite rates
                temp[1] = new_sample
                # add to the augmented data
                aug_data[0].append(temp)
                # copy over other data corresponding to original object (not affected by augmentation)
                aug_data[1].append(data[1][n_obj])
                aug_data[2].append(data[2][n_obj])
                aug_data[3].append(data[3][n_obj])

    return aug_data


def aug_single_arr(arr):
    bts = BootstrappingWrapper(
        ConvolutionSmoother(window_len=6, window_type="ones"),
        bootstrap_type="mbb",
        block_length=5,
    )
    bts_samples = bts.sample(arr)
    return bts_samples
