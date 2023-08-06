from tracktotrip import Track
from tracktotrip.smooth import INVERSE_STRATEGY, NO_STRATEGY
import numpy as np
import matplotlib.pyplot as plt

temp_trk = [
    Track.from_gpx('/Users/ruipgil/Downloads/20160830 (3).gpx')[0],
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

KALMAN_NOISE = 1000
plt.savefig('kalman_baseline.pdf', bbox_inches='tight')
plt.clf()
plt.axis('equal')
plt.axis('off')

n_points = sum([len(s.points) for s in trk.segments])
trk = trk.copy()
trk.smooth(NO_STRATEGY, KALMAN_NOISE)
for segment in trk.segments:
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
result = sum([len(s.points) for s in trk.segments])
print("From %d to %d points" % (n_points, result))
print("Compression: %f" % (n_points/float(result)))

plt.savefig('kalman_no_s.pdf', bbox_inches='tight')
plt.clf()
plt.axis('equal')
plt.axis('off')


from pykalman import KalmanFilter
from scipy import stats
def smooth(points, n_iter=1):
    measurements = map(lambda p: [p.lon, p.lat], points)
    dts = map(lambda p: p.dt, points)
    print dts
    dt = sum(dts) / len(dts)
    print dt
    transition = [
            [1, dt, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, dt],
            [0, 0, 0, 1]]
    observation = [
            [1, 0, 0, 0],
            [0, 0, 1, 0]]
    initial = [measurements[0][0], 0, measurements[0][1], 0]
    kf = KalmanFilter(transition_matrices = transition, observation_matrices = observation, initial_state_mean=initial)
    kf = kf.em(measurements, n_iter=n_iter)
    print kf
    (smoothed_state_means, smoothed_state_covariances) = kf.smooth(measurements)

    for pi, point in enumerate(points):
        point.lon = smoothed_state_means[pi][0]
        point.lat = smoothed_state_means[pi][2]

    return points

# trk.smooth(INVERSE_STRATEGY, KALMAN_NOISE)
# for segment in trk.segments:
#     trk.compute_metrics()
#     points = segment.points
#     print 'kalman inverse average velocity %f' % (sum([p.vel for p in segment.points]) / float(len(segment.points)))
#     # points = smooth(points)
#     plt.plot([p.lon for p in points], [p.lat for p in points], 'o-')
# result = sum([len(s.points) for s in trk.segments])
# print("From %d to %d points" % (n_points, result))
# print("Compression: %f" % (n_points/float(result)))

# plt.show()
# exit()
plt.savefig('kalman_inverse.pdf', bbox_inches='tight')
plt.clf()
plt.axis('equal')
plt.axis('off')

n_points = sum([len(s.points) for s in trk.segments])
trk = trk.copy()
trk.simplify(0.000015, 2.0, 1.0)
trk.compute_metrics()
for segment in trk.segments:
    trk.compute_metrics()
    print 'simplify spt average velocity %f' % (sum([p.vel for p in segment.points]) / float(len(segment.points)))
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
result = sum([len(s.points) for s in trk.segments])
print("From %d to %d points" % (n_points, result))
print("Compression: %f" % (n_points/float(result)))

plt.savefig('compression_spt.pdf', bbox_inches='tight')
plt.clf()
plt.axis('equal')
plt.axis('off')

trk.simplify(0.00004, 2.0, 1.0, True)
for segment in trk.segments:
    trk.compute_metrics()
    print 'simplify drp average velocity %f' % (sum([p.vel for p in segment.points]) / float(len(segment.points)))
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
result = sum([len(s.points) for s in trk.segments])
print("From %d to %d points" % (n_points, result))
print("Compression: %f" % (n_points/float(result)))

plt.savefig('compression_drp.pdf', bbox_inches='tight')


plt.clf()
plt.axis('equal')
plt.axis('off')

trk2 = trk
trk = trk2
trk.simplify(0.000015, 2.0, 1.0, True)
for segment in trk.segments:
    trk.compute_metrics()
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
result = sum([len(s.points) for s in trk.segments])
plt.savefig('compression_drp_after.pdf', bbox_inches='tight')


# plt.show()
