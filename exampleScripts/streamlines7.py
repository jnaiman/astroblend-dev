import yt
import numpy as np
from yt.visualization.api import Streamlines
import random


fname = '/Users/jillnaiman1/data/IsolatedGalaxy/galaxy0030/galaxy0030' # home


# now, get stream line
ds = yt.load(fname)

c = np.array([0.5]*3)
N = 10  # number of stream lines
scale = 1.0
pos_dx = np.random.random((N,3))*scale-scale/2.
pos = c+pos_dx

streamlines = Streamlines(ds,pos,'velocity_x', 'velocity_y', 'velocity_z', length=1.0)

