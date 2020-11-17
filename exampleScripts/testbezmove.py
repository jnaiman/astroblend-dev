import science

# make a list of data files
ddir = '/Users/jillnaiman/data/sphdec/' # where data is stored
df = 'outputs_dec_' # base name of data files
dfiles = []
nf = 200
ns = 1
# create list of files
for i in range(ns,nf):
    num = "%03d" % (i) # create strings from numbers, with 3 digits
    dfiles.append(ddir + df + num + '.txt')

halo_sizes = (0.008,0.008,0.008,0.008,0.008,0.008) # halos or particles
colors = [(1,1,0), (0,0,1), (1,0,0), (1,0,0), (1,1,1), (0,1,0)]
# how many particle types?
# 0 = Gas
# 1 = Halo
# 2 = Disk (disk and bulge = old stars?)
# 3 = Bulge
# 4 = Stars (New stars?)
# 5 = BHs
particle_types = 6

# load particle data
myobject = science.Load(dfiles, scale = (0.1, 0.1, 0.1), 
                        halo_sizes = halo_sizes, particle_num=particle_types, 
                        particle_colors=colors)

# hide the 1st particle
part_hide = (False, True, False, False, False, False)
myobject.particle_hide = part_hide

# init camera
cam = science.Camera()

# first set Blender directory & render name
render_directory = '/Users/jillnaiman/blenderRenders/'
render_name = 'testbezsph_'

locs = [[10,10,10], [10, -10, 10], [10, -10, -10]] # camera goes through these points
pts =  [[0,3,0], [0, -3, 0], [0, 3, 0]] # camera will point at these points along the way


movie = science.Movies(cam, render_directory, render_name, myobject, 
                       render_type = 'Bezier', render_steps = nf-1, 
                       bezier_locations=locs, bezier_pointings=pts, 
                       bezier_visualize=True)


movie = science.Movies(cam, render_directory, render_name, myobject, 
                       render_type = 'Bezier', render_steps = nf-1, 
                       bezier_locations=locs, bezier_pointings=pts, 
                       bezier_visualize=False)

