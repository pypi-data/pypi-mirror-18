from tracktotrip import Track
from tracktotrip.smooth import EXTRAPOLATE_STRATEGY, INVERSE_STRATEGY, NO_STRATEGY
import numpy as np
import matplotlib.pyplot as plt

temp_trk = [
    Track.from_gpx('/Users/ruipgil/tracks/backup/2015-07-23_1.gpx')[0],
    # Track.from_gpx('/Users/ruipgil/Downloads/20160830.gpx')[0],
]

segs = []
for trke in temp_trk:
    segs.extend(trke.segments)

trk = Track("", segs)
trk.segments[0].points = trk.segments[0].points[:10]
trk.compute_metrics()
plt.axis('equal')
# plt.axis('off')

def plot_track(trk, legend=None, marker='o'):
    plt.axis('equal')
    plt.axis('off')
    for segment in trk.segments:
        plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], '%s-' % marker, label=legend)

plot_track(trk, 'Original')
KALMAN_NOISE = 1000
trk1 = trk.copy()
# trk1.segments[0].points = list(reversed(trk1.segments[0].points))
trk1.smooth(NO_STRATEGY, KALMAN_NOISE)
trk2 = trk.copy().smooth(EXTRAPOLATE_STRATEGY, KALMAN_NOISE)
trk3 = trk.copy().smooth(INVERSE_STRATEGY, KALMAN_NOISE)

# print(len(trk1.segments[0].points))
# print(len(trk3.segments[0].points))

plot_track(trk1, 'No strategy', 'v')
plot_track(trk2, 'With extrapolation', 'D')
plot_track(trk3, 'With backwards pass', 's')
plt.legend()
# plt.show()
plt.savefig('kalman_strategies_comparison.pdf', bbox_inches='tight')

