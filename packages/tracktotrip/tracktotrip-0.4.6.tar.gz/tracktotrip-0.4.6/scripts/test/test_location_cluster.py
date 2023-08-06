from tracktotrip import Track, Point
from sklearn.cluster import DBSCAN
from tracktotrip.location import compute_centroid
import numpy as np
import matplotlib.pyplot as plt

track = Track.from_gpx('/Users/ruipgil/Dropbox/20160911.gpx')[0]

plt.clf()
plt.axis('equal')
plt.axis('off')

track.compute_metrics()
# track.to_trip('inverse', 10, 0.01, 10, 1.0, 1.0)
points = []
dts = []
for segment in track.segments:
    for point in segment.points:
        dts.append(point.dt)
        points.append(point.gen2arr())
    # plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
print len(points)

average_dts = np.median(dts)
print average_dts
X = np.array(points[290:])

min_samples = 20.0/average_dts
print min_samples
db = DBSCAN(eps=0.00001, min_samples=min_samples)
db.fit(X)

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    # print k
    xy = X[class_member_mask & core_samples_mask]
    # print compute_centroid()
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)




plt.show()
