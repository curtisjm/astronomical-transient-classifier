import pickle

with open("../pickles/bat_data.pickle") as f:
    data = pickle.load(f)

print(data[0].name)
