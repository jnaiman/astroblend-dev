

import science

cam = science.Camera()

sph1 = science.simpleobjects.Sphere('Sphere1', color = (1,0,0), shadeless=False)
sph1.location = (0, 3, 0)
sph2 = science.simpleobjects.Sphere('Sphere2', color = (1,1,0), shadeless=False)
sph2.location = (3, 0, 0)
sph3 = science.simpleobjects.Sphere('Sphere3', color = (0,0,1), shadeless=False)
sph3.location = (0, -3, 0)

# first set Blender directory
render_directory = '/Users/jillnaiman/blenderRenders/'
render_name = 'testbez_'

locs = [[10,10,10], [10, -10, 10], [10, -10, -10]] # camera goes through these points
pts =  [[0,3,0], [0, -3, 0], [0, 3, 0]] # camera will point at these points along the way


movie = science.Movies(cam, render_directory, render_name, sph1, sph2, sph3, 
                       render_type = 'Bezier', render_steps = 60, 
                       bezier_locations=locs, bezier_pointings=pts, 
                       bezier_visualize=True)


movie = science.Movies(cam, render_directory, render_name, sph1, sph2, sph3, 
                       render_type = 'Bezier', render_steps = 60, 
                       bezier_locations=locs, bezier_pointings=pts, 
                       bezier_visualize=False)

