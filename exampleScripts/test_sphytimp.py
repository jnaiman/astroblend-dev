import science

filename = '/Users/jillnaiman/data/TipsyGalaxy/galaxy.00300'

color_field = ('Gas', 'Temperature') 
color_log = True
color_map = 'Rainbow'

# these two things play off eachother!
halo_size = 0.108 # need to play with this
set_cam = (0,0,70)

scale = [(1.0, 1.0, 1.0)]

cam = science.Camera()
cam.location = set_cam
cam.clip_begin = 0.0001

lighting = science.Lighting('EMISSION')

# initialize render
render_directory = '/Users/jillnaiman/blenderRenders/'
render_name = 'myytsphrender_'
render = science.Render(render_directory, render_name)


myobject = science.Load(filename, scale=scale, halo_sizes = halo_size, 
                        color_field = color_field, color_map = color_map, 
                        color_log = color_log, n_ref=8)

#render.render()
