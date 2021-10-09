import numpy as np

labels = {
    "*No Label Available*": "0",
    "Sy1.x": "1",
    "Sy1": "1",
    "Sy1.2": "1",
    "Sy1.5": "1",
    "Sy1.8": "1",
    "Sy1.9": "1",
    "Beamed AGN": "2",
    "Compact group of gal": "3",
    "Galactic Center": "4",
    "GC": "4",
    "Galaxy Cluster": "5",
    "Gamma-ray source": "6",
    "Open star cluster": "7",
    "Sy1;broad-line AGN": "8",
    "Unknown AGN": "9",
    "molecular cloud": "10",
    "Starburst galaxy": "11",
    "Sy2 candidate": "12",
    "Symbiotic star": "13",
    "Pulsar": "14",
    "Sy2": "15",
    "U1": "16",
    "U2": "17",
    "U3": "18",
    "SNR": "19",
    "HMXB": "20",
    "CV": "21",
    "LMXB": "22",
    "XRB": "23",
    "Nova": "24",
    "star": "25",
    "multiple": "26",
    "LINER": "27",
}


# find label name from label number
def get_class_name(class_num):
    keys = list(labels.keys())
    values = list(labels.values())
    pos = values.index(class_num)
    return keys[pos]


# get label number from label string
def make_label(val):
    return labels[val]


def find_min_time(data):
    min_t = 1e14
    for i in range(len(data[0])):
        if float(data[0][i][0][0]) < min_t:
            min_t = float(data[0][i][0][0])
    # print(f"Min Time: {min_t}")
    return min_t
