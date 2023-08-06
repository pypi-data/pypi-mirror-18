import pickle
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

features = pickle.load(open('geolife.features', 'r'))
labels = pickle.load(open('geolife.labels', 'r'))
labels_set = list(set(labels))
# print(labels_set)

x = np.arange(len(labels_set))
ys = [i+x+(i*x)**2 for i in range(len(labels_set))]

colors = cm.rainbow(np.linspace(0, 1, len(ys)))

for i, feature in enumerate(features):
    label = labels[i]
    c_index = labels_set.index(label)
    # print(c_index)
    color = colors[c_index]
    plt.plot(np.log1p(feature[0]/300.0), np.log1p(feature[1]), 'o', color=color, label=label)#, ms=(feature[2]/300.0) * 5 + 5)

plt.show()
