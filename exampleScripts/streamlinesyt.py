import yt
import numpy as np
import matplotlib.pylab as pl

from yt.visualization.api import Streamlines
from mpl_toolkits.mplot3d import Axes3D

ds = yt.load('/Users/jillnaiman/data/IsolatedGalaxy/galaxy0030/galaxy0030') # Load ds
c = np.array([0.5]*3)
N = 100
scale = 1.0
pos_dx = np.random.random((N,3))*scale-scale/2.
pos = c+pos_dx

streamlines = Streamlines(ds,pos,'velocity_x', 'velocity_y', 'velocity_z', length=1.0)
streamlines.integrate_through_volume()

fig=pl.figure()
ax = Axes3D(fig)
for stream in streamlines.streamlines:
    stream = stream[np.all(stream != 0.0, axis=1)]
    ax.plot3D(stream[:,0], stream[:,1], stream[:,2], alpha=0.1)
pl.savefig('streamlines.png')
