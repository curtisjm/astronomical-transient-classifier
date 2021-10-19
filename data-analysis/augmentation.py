from tsmoothie.smoother import *
from tsmoothie.bootstrap import BootstrappingWrapper
from tsmoothie.utils_func import create_windows, sim_seasonal_data, sim_randomwalk


# min 6000 objects per class


# step 1,  iterate over the 1526 objects that matched the 157 month catalog with the files names
# step 2, for each object extract one band lc and normalize them dividin by the max
# step 3, bootstrap that lightcurve and place is in the new simulated object with the correct label

# function creating the simulated data
def boot_sim(obj, nsamp, r, c):
    # print(obj)
    new_sample = np.empty([nsamp, r, c])
    # print(new_sample.shape)
    for j in range(r):
        raw = obj[j]
        # print(raw)
        # operate bootstrap
        bts = BootstrappingWrapper(
            ConvolutionSmoother(window_len=6, window_type="ones"),
            bootstrap_type="mbb",
            block_length=5,
        )
        bts_samples = bts.sample(raw, n_samples=nsamp)
        for i in range(nsamp):
            # print(new_sample[i][j].shape)
            # print(bts_samples.T.shape)

            new_sample[i][j] = bts_samples[i]
    return new_sample


def augment_data(data):
    sim_sam = []
    lab = []
    nobj = 2

    for i in range(len(data[0])):
        mat = data[0][i][1]
        # print(mat[0])
        s = boot_sim(mat * 1e4, nobj, 8, 155)
        label = int(data[3][i])
        for j in range(nobj):
            # sim_sam.append([sim_sam,np.array(s[j]).flatten(),label])
            sim_sam = np.append(sim_sam, np.array(s[j]).flatten())
            lab.append(label)

    # print(sim_sam.shape)
    print(8 * 155 * nobj * len(data[0]))

    q = np.reshape(sim_sam * 1e-4, (nobj * len(data[0]), 8, 155))
    print(q[0].shape)
    return q
