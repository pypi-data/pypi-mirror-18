import matplotlib.pyplot as plt
from tracktotrip import Track
from tracktotrip.td_sp import td_sp, td_tr

def plot(seg):
    plt.plot(map(lambda p: p.lat, seg), map(lambda p: p.lon, seg), '-o')

t = Track.fromGPX("/Users/ruipgil/tracks/2016-01-03_2.gpx")[0]
seg = t.segments[0].points
print('Lengths')
print(len(seg))

# plt.axis('equal')
# plot(seg)
res1 = td_tr(seg, 30)
print(len(res1))

from scipy import stats
import numpy as np
def computeMetrics(arr):
    prev = None
    for elm in arr:
        if prev is None:
            prev = elm
        else:
            elm.computeMetrics(prev)

# print('Modes')
computeMetrics(seg)
computeMetrics(res1)
vels1 = map(lambda p: p.vel, seg)
vels2 = map(lambda p: p.vel, res1)

bins = np.linspace(0, 30, 30)
print(np.mean(vels1))
print(np.mean(vels2))
plt.plot(np.histogram(vels1, bins, density=True)[0])
plt.plot(np.histogram(vels2, bins, density=True)[0])

# print(vels1)
# print(vels2)
# print(stats.mode(vels1))
# print(stats.mode(vels2))

# plot(seg)
# plot(res1)
plt.show()
