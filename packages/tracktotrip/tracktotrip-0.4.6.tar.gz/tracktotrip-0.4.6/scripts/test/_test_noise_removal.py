from tracktotrip import Track
import tracktotrip.transportation_mode as tm
from changepy import pelt
from changepy.costs import normal_mean

import numpy as np
import matplotlib.pyplot as plt

temp_trk = [
    Track.from_gpx('/Users/ruipgil/tracks/input/2016-06-11_1.gpx')[0],
    # Track.from_gpx('/Users/ruipgil/tracks/backup/2015-07-23_2.gpx')[0],
    # Track.from_gpx('/Users/ruipgil/tracks/backup/2015-07-23_3.gpx')[0]
]

segs = []
for trke in temp_trk:
    segs.extend(trke.segments)
trk = Track("", segs)
trk.compute_metrics()
# trk.to_trip('', 0, 5.0, 0.15, 80, 0.3, '%Y-%m-%d')

def two_mean_filter(accs, thr=0.1):
    nz_accs = [acc for acc in accs if acc > thr]

    mean = np.mean(nz_accs)
    mean = np.mean([acc for acc in accs if acc >= mean])

    std = np.std(nz_accs)
    std = np.std([acc for acc in accs if acc >= std])

    return mean, std

cm = 'grbcmykw'
def plot(ax, data):
    index = 0
    for i, seg_data in enumerate(data):
        ax.plot(range(index, len(seg_data) + index), seg_data, '-' + cm[i])
        mean, std = two_mean_filter(seg_data)
        # nz_seg_data = [d for d in seg_data if d > 0.2]
        # mean = np.mean(nz_seg_data)
        # # print('mean1', mean)
        # mean = np.mean([d for d in seg_data if d > mean])
        # # print('mean2', mean)
        # std = np.std(nz_seg_data)
        # # print('std1', std)
        # std = np.std([d for d in seg_data if d > std])
        # # print('std2', std)

        ax.axhline(mean + std, color=cm[i], linestyle='--')

        # for changepoint in changepoints[i]:
        #     ax.axvline(changepoint + index, color='k', linestyle='--')
        index = index + len(seg_data)

plot_n = 1
plot_cols = 2
plot_rows = 2
#
def show(data, title):
    global plot_n

    ax = fig.add_subplot(plot_rows, plot_cols, plot_n)

    ax.set_title(title)
    plot(ax, data)
    plot_n = plot_n + 1
#
fig = plt.figure()
# changepoint_for(raw_vel)
# changepoint_for(abs_vel)
# changepoint_for(square_vel)
# changepoint_for(diff_vel)
# changepoint_for(square_diff_vel)
# changepoint_for(raw_acc)

print([p.vel for p in trk.segments[0].points[390:400]])
print([p.acc for p in trk.segments[0].points[390:400]])
print([p.dt for p in trk.segments[0].points[390:400]])
show([[p.acc for p in segment.points] for segment in trk.segments], "Raw accelerations")
show([[abs(p.acc) for p in segment.points] for segment in trk.segments], "Abs accelerations")
show([[p.acc**2 for p in segment.points] for segment in trk.segments], "Abs accelerations")


plt.show()
