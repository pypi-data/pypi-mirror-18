import math
import unittest
from tracktotrip.similarity import segment_similarity
from tracktotrip.similarity import normalize, line_distance_similarity, line_similarity
from tracktotrip.similarity import line, angle_similarity, distance_to_line, distance_similarity, sort_segment_points
from tracktotrip import Segment, Point, Track
from tracktotrip.smooth import NO_STRATEGY

import matplotlib.pyplot as plt
plt.axis('equal')
plt.axis('off')

def plot_segment(segment):
    x = [point.lon for point in segment.points]
    y = [point.lat for point in segment.points]
    plt.plot(x, y, 'o-')

track = Track.from_gpx('/Users/ruipgil/Downloads/20160830 (4).gpx')[0]

# for segment in track.segments:
#     plot_segment(segment)

track.compute_metrics()
track = track.smooth(NO_STRATEGY, 1000)
track = track.simplify(None, 1.0, 1.0)
# track.to_trip('inverse', 10, 0.01, 10, 1.0, 1.0)

for segment in track.segments:
    plot_segment(segment)

[a_seg, b_seg] = track.segments


similarity, parts = segment_similarity(a_seg, b_seg, .001)
# pts = sort_segment_points(b_seg.points, a_seg.points)
# plot_segment(Segment(pts))

print similarity
print parts

plt.show()
