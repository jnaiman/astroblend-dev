## NOT GREAT! CHECK OUT: http://wiki.blender.org/index.php/Doc:2.6/Manual/Modeling/Curves/Editing/Advanced
# make cylinder with Nvals number of things and then deform along a curve


import science
import yt
import numpy as np
from yt.visualization.api import Streamlines
from mathutils import Vector
import random
from scipy import interpolate


fname = '/Users/jillnaiman/data/IsolatedGalaxy/galaxy0030/galaxy0030'

ssname = "NameOfMyCurve"
























#ds = yt.load(fname)
#
#c = np.array([0.5]*3)
#N = 10  # number of stream lines
#scale = 1.0
#pos_dx = np.random.random((N,3))*scale-scale/2.
#pos = c+pos_dx
#
#streamlines = Streamlines(ds,pos,'velocity_x', 'velocity_y', 'velocity_z', length=1.0)
#streamlines.integrate_through_volume()
#
## select out 1 stream... for now
#stream = streamlines.streamlines[1]
#stream = stream[np.all(stream != 0.0, axis=1)] # doen something fancy
#
#
## units
#stream = stream*ds.length_unit # into cm 
## now, scale down to what we want
#stream = stream/yt.units.cm
#stream = stream/3.1e18 # pc
#
## for this case
#stream = stream/1e5
#
#x = stream[:,0]
#y = stream[:,1]
#z = stream[:,2]

# for testing cylinder
stream = np.zeros(100)

# this will eventually be filled by an actual colormap
#  from data taken on the steamline
colors = np.zeros((len(stream),3))
for i in range(0,len(stream)):
    #colors.append([random.random() for ii in range(3)])
    colors[i,0] = random.random()
    colors[i,1] = random.random()
    colors[i,2] = random.random()

#x = floor(len(stream)/20.0)
#
#if ((x % 2) != 0):
#    x=x+1
#
#Nvals = max(100,x)) 
##method='cubic' # or nearest, or linear
#method='linear' # or nearest, or linear
#xn = np.linspace(x.min(),x.max(),Nvals)
#
## y(x)
#f = interpolate.interp1d(x,y,kind=method)
#yn = f(xn)
#
## z(x)
#f = interpolate.interp1d(x,z,kind=method)
#zn = f(xn)
#
## also remap colors
#f = interpolate.interp1d(x,colors[:,0],kind=method)
#r = f(xn)
#f = interpolate.interp1d(x,colors[:,1],kind=method)
#g = f(xn)
#f = interpolate.interp1d(x,colors[:,2],kind=method)
#b = f(xn)
#
#rgb = []
#for i in range(0,Nvals):
#    rgb.append([r[i],g[i],b[i]])
#
#
#
## put back in a smaller stream
#streamn = np.zeros((Nvals,3))
#
#streamn[:,0] = xn
#streamn[:,1] = yn
#streamn[:,2] = zn



# add in cylinder
cyl_verts = 16
bpy.ops.mesh.primitive_cylinder_add(vertices=cyl_verts, radius=1, depth=2, location=(0, 0, 0), rotation=(0, 0, 0))

# now, make it long
cyl = bpy.data.objects['Cylinder']
cyl.scale = (0.5, 0.5, 10)


mesh = cyl.data
if len(mesh.vertex_colors) == 0:
    bpy.ops.mesh.vertex_color_add()

# for now - testing
rgb = colors

# color by the first color
color_layer = mesh.vertex_colors["Col"]

i=0
# tag the ends
ipend1 = -1
ipend2 = -1
dip1 = 0
dip2 = 0
for ip, poly in enumerate(mesh.polygons):
    print('ip = ' + str(ip))
    idip = i
    for idx in poly.loop_indices:
        print('idx = ' + str(idx))
        color_layer.data[i].color = rgb[0]
        print('i = ' + str(i))
        i += 1
    idip = (i-1)-idip
    if (idip > dip1):
        dip1 = idip
        ipend1 = ip
    elif (idip > dip2):
        dip2 = idip
        ipend2 = ip
    print(' ')

ipstart = ip # for next cylinder

# sub divide
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.mode_set(mode='EDIT')

bpy.ops.mesh.subdivide(smoothness=0)

bpy.ops.object.mode_set(mode='OBJECT')

# add more colors.... nope -> crashes
i=0
#for ip in range(0,len(mesh.polygons)):
for ip in range(0,20):
    print('ip = ' + str(ip))
    for idx in mesh.polygons[ip].loop_indices:
        print('idx = ' + str(idx))

for ip, poly in enumerate(mesh.polygons):
    if ip >= ipstart:
        for idx in poly.loop_indices:
            color_layer.data[i].color = rgb[1]
            i += 1




# check out: http://blenderscripting.blogspot.com/2014/02/3d-tube-from-points.html
# for particles check out: http://yt-project.org/doc/analyzing/analysis_modules/particle_trajectories.html#particle-trajectories
# may or maynot be useful: http://blenderscripting.blogspot.com/2013/03/painting-vertex-color-map-using.html, http://blenderartists.org/forum/showthread.php?190693-Setting-Vertex-Color-via-Python, http://www.blender.org/api/blender_python_api_2_63_2/bpy.types.Mesh.html
