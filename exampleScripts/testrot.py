

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
render_name = 'testrot_'

# move camera out
cam.location = (10, 10, 10)
cam.pointing = sph2.location

#zoom_factor = 0.5

#zoom_factor = 2.0

#movie = science.Movies(cam, render_directory, render_name, sph1, sph2, sph3, 
#                       render_type = 'Zoom', render_steps = 60, 
#                       zoom_factor = zoom_factor)

#movie = science.Movies(cam, render_directory, render_name, sph1, sph2, sph3, 
#                       render_type = 'Bezier', render_steps = 60, 
#                       bezier_locations=(cam.location,(20,0,0)), 
#                       bezier_pointings=(sph2.location, sph2.location)

movie = science.Movies(cam, render_directory, render_name, sph1, sph2, sph3, 
                       render_type = 'Rotation', render_steps = 60, 
                       radius_end = 2.0, theta_end = 0.1, phi_end = 90., 
                       use_current_start_angles=True, use_current_radius = True)
