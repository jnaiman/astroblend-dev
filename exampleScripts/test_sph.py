import science


ddir = '/Users/jillnaiman/data/sphdec/' # where data is stored
df = 'outputs_dec_' # base name of data files
dfiles = []
nf = 200
#nf = 5
ns = 1
science.nframe = ns # incase we want to render a subset, ns can be larger, nf can be smaller
# create list of files
for i in range(ns,nf):
    num = "%03d" % (i) # create strings from numbers, with 3 digits
    dfiles.append(ddir + df + num + '.txt')

halo_sizes = (0.0008,0.0008,0.0008,0.0008,0.0008,0.008) # larger for BH
colors = [(1,1,0), (0,0,1), (1,0,0), (1,0,0), (1,1,1), (0,1,0)]
# how many particle types?
# 0 = Gas
# 1 = Halo
# 2 = Disk (disk and bulge = old stars?)
# 3 = Bulge
# 4 = Stars (New stars?)
# 5 = BHs
particle_types = 6


cam = science.Camera()
cam.location = (1.0,0,0)
cam.pointing = (0,0,0)
# also, render to lower
cam.clip_begin = 0.0001

render_directory = '/Users/jillnaiman/blenderRenders/'
render_name = 'mymovie_sph_sta_'

light = science.Lighting('EMISSION') # light by surface emission

render = science.Render(render_directory, render_name)

#for i in range(0,nf-1):
#    myobject = science.Load(dfiles[i], scale = (0.1, 0.1, 0.1), 
#                            halo_sizes = halo_sizes, particle_num=particle_types, 
#                            particle_colors=colors)
#    science.hide_object(myobject.name[1])
#    render.render()
#    science.delete_object(myobject)



render_name = 'mymovie_sph_zoom_'

myobject = science.Load(dfiles[0], scale = (0.1, 0.1, 0.1), 
                        halo_sizes = halo_sizes, particle_num=particle_types, 
                        particle_colors=colors)

# hide the 1st particle
part_hide = (False, True, False, False, False, False)
myobject.particle_hide = part_hide

#movie = science.Movies(cam, render_directory, render_name, myobject, 
#                       render_type = 'Zoom', render_steps = nf-1, 
#                       zoom_factor = 0.5)

render_name = 'mymovie_sph_rot_'

#movie = science.Movies(cam, render_directory, render_name, myobject, 
#                       render_type = 'Rotation', render_steps = nf-1, 
#                       radius_end = 0.5, theta_end = 0.1, phi_end = 180., 
#                       use_current_start_angles=True, use_current_radius = True)



