from tracktotrip import Track
import numpy as np
import matplotlib.pyplot as plt

temp_trk = [
    Track.from_gpx('/Users/ruipgil/Downloads/20160830.gpx')[0],
    # Track.from_gpx('/Users/ruipgil/Downloads/20160830.gpx')[0],
]

segs = []
for trke in temp_trk:
    segs.extend(trke.segments)
trk = Track("", segs)
trk.compute_metrics()
# trk.to_trip('', 0, 5.0, 0.15, 80, 0.3, '%Y-%m-%d')
plt.axis('equal')
plt.axis('off')
for segment in trk.segments:
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')

plt.savefig('compression_baseline.pdf')
plt.clf()
plt.axis('equal')
plt.axis('off')


n_points = sum([len(s.points) for s in trk.segments])
trk2 = trk.copy()
trk.simplify(0.000015, 2.0, 1.0)
for segment in trk.segments:
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
result = sum([len(s.points) for s in trk.segments])
print("From %d to %d points" % (n_points, result))
print("Compression: %f" % (n_points/float(result)))

plt.savefig('compression_spt.pdf')
plt.clf()
plt.axis('equal')
plt.axis('off')

trk = trk2
trk.simplify(0.000015, 2.0, 1.0, True)
for segment in trk.segments:
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
result = sum([len(s.points) for s in trk.segments])
print("From %d to %d points" % (n_points, result))
print("Compression: %f" % (n_points/float(result)))

plt.savefig('compression_drp.pdf')

plt.clf()
# plt.axis('off')
from tracktotrip.transportation_mode import build_histogram, normalize, extract_features_2
hist = normalize(build_histogram(trk.segments[0].points))
plt.hist(range(len(hist)), len(hist), weights=hist, cumulative=False, edgecolor='none')
plt.savefig('__hist.pdf')
plt.clf()
# plt.axis('off')
plt.hist(range(len(hist)), len(hist), weights=hist, cumulative=True, edgecolor='none')
plt.savefig('__hist_cum.pdf')


# plt.show()
