import pandas as pd

import urllib

import numpy as np

import matplotlib.pyplot as plt


BAT_table = pd.read_html(
    "https://swift.gsfc.nasa.gov/results/transients/", match="Source Name"
)[0]


Data1 = BAT_table[
    ["Source Name", "RA J2000 Degs", "Dec J2000 Degs", "Alternate Name", "Source Type"]
]


s = Data1["Source Name"]

Name = Data1["Alternate Name"]

Raobj = Data1["RA J2000 Degs"]

Decobj = Data1["Dec J2000 Degs"]

Sourcetype = Data1["Source Type"]

# orbital

# o = '.orbit.lc.txt'

# daily

o = ".lc.txt"


url = "https://swift.gsfc.nasa.gov/results/transients/weak/"


my_new_list = [url + x + o for x in s]

new_list = [a.replace("+", "p") for a in my_new_list]

a = [b.replace(" ", "") for b in new_list]


c = []

d = [[], [], []]


print("I got the list of files to parse")


def links(g):

    with urllib.request.urlopen(g) as p:

        s = p.read()

        # I'm guessing this would output the html source code ?

        table = s.decode("utf-8")

        content_list = table.splitlines()

        newlist = content_list[5:]

        time = np.array([b.split()[0] for b in newlist]).astype("float64")

        rate = np.array([b.split()[1] for b in newlist]).astype("float64")

        rate_err = np.array([b.split()[2] for b in newlist]).astype("float64")

    return np.array([time, rate, rate_err])


print("Building the big array")

for items in a:

    try:

        # print(items)

        c.append(links(items))

        # print(items)

    except:

        newurl = items.replace("weak/", "")

        c.append(links(newurl))

        print(items)


for i in range(len(c)):

    d[0].append(c[i])

    d[1].append(Name[i])

    d[2].append([Raobj[i], Decobj[i]])


print(len(d[0]))


# print(np.asarray(d))

np.save("BAT_trans_data.npy", np.asarray(d), allow_pickle=True, fix_imports=False)
