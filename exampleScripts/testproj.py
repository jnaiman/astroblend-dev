import yt
ds = yt.load('~/data/TipsyGalaxy/galaxy.00300', n_ref=8)
yt.ProjectionPlot(ds, 'z', ('gas','density'), width=(40, 'kpc'), center='m').save('~/Desktop/proj2.py')

from science import objects
fname = '~/data/TipsyGalaxy/galaxy.00300'
name, ds, hused = objects.import_ytsph(fname, [0.0008], ('gas','temperature'), 'algae', color_log=False, n_ref=8)
