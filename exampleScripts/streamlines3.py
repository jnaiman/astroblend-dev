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


ds = yt.load(fname)

c = np.array([0.5]*3)
N = 10  # number of stream lines
scale = 1.0
pos_dx = np.random.random((N,3))*scale-scale/2.
pos = c+pos_dx

streamlines = Streamlines(ds,pos,'velocity_x', 'velocity_y', 'velocity_z', length=1.0)
streamlines.integrate_through_volume()

# select out 1 stream... for now
stream = streamlines.streamlines[1]
stream = stream[np.all(stream != 0.0, axis=1)] # doen something fancy


# units
stream = stream*ds.length_unit # into cm 
# now, scale down to what we want
stream = stream/yt.units.cm
stream = stream/3.1e18 # pc

# for this case
stream = stream/1e5

x = stream[:,0]
y = stream[:,1]
z = stream[:,2]

# this will eventually be filled by an actual colormap
#  from data taken on the steamline
colors = np.zeros((len(stream),3))
for i in range(0,len(stream)):
    #colors.append([random.random() for ii in range(3)])
    colors[i,0] = random.random()
    colors[i,1] = random.random()
    colors[i,2] = random.random()

Nvals = max(100,floor(len(stream)/20.0)) 
#method='cubic' # or nearest, or linear
method='linear' # or nearest, or linear
xn = np.linspace(x.min(),x.max(),Nvals)

# y(x)
f = interpolate.interp1d(x,y,kind=method)
yn = f(xn)

# z(x)
f = interpolate.interp1d(x,z,kind=method)
zn = f(xn)

# also remap colors
f = interpolate.interp1d(x,colors[:,0],kind=method)
r = f(xn)
f = interpolate.interp1d(x,colors[:,1],kind=method)
g = f(xn)
f = interpolate.interp1d(x,colors[:,2],kind=method)
b = f(xn)

rgb = []
for i in range(0,Nvals):
    rgb.append([r[i],g[i],b[i]])



# put back in a smaller stream
streamn = np.zeros((Nvals,3))

streamn[:,0] = xn
streamn[:,1] = yn
streamn[:,2] = zn





# ok, lets assume streamlines works
 
# weight
w = 1
 

sname = ssname + "Object"
 

# create bevel object
science.deselect_all()
# add curve
bpy.ops.curve.primitive_bezier_circle_add(radius=0.1,  location=(0, 0, 0), rotation=(0, 0, 0))
bevob = bpy.data.objects['BezierCircle']

def MakePolyLine(objname, curvename, cList, bevel_obj):
    curvedata = bpy.data.curves.new(name=curvename, type='CURVE')
    curvedata.dimensions = '3D'
    curvedata.bevel_object = bevel_obj
    objectdata = bpy.data.objects.new(objname, curvedata)
    objectdata.location = (0,0,0) #object origin
    bpy.context.scene.objects.link(objectdata)
    polyline = curvedata.splines.new('NURBS')
    polyline.points.add(len(cList)-1)
    for num in range(len(cList)):
        polyline.points[num].co = (cList[num])+(w,)
    polyline.order_u = len(polyline.points)-1
    polyline.use_endpoint_u = True


MakePolyLine(sname, ssname, tuple(map(tuple,streamn)), bevob)
 


# now, we need to make this thing into a mesh & color it

# (1) select object
science.deselect_all()
bpy.data.objects[sname].select = True
bpy.context.scene.objects.active = bpy.data.objects[sname]



import copy


def color_nurbs_curve(nurbs_name, color_list):
    """Converts the NURBS curve which should already have a bevel object so it has some width.
    color_list should be a list of colors each of which is a 3 element list with [R,G,B]."""
    nurbs_obj = bpy.data.objects[nurbs_name + 'Object']
    print(nurbs_name)
    nurbs_curve_obj = bpy.data.curves[nurbs_name]
    print(nurbs_curve_obj)
    nurbs_coords = copy.deepcopy( [ nurbs_obj.data.splines[0].points[i].co for i in range(len(nurbs_obj.data.splines[0].points)) ] )
    #Error checking
    if len(nurbs_coords) != len(color_list):
        raise RuntimeError('The color list must have a number of colors equal to the number of control points of your bezier curve')
    if nurbs_curve_obj.data.bevel_object == None:
        raise RuntimeError('Your NURBS curve must have a bevel object')
    scn = bpy.context.scene
    #Convert to mesh
    scn.objects.active = nurbs_obj
    nurbs_obj.select = True
    bpy.ops.object.convert( target='MESH' )
    #sometimes this conversion results in a bunch of doubles, so I remove the doubles
    remove_doubles(nurbs_obj)
    mesh = nurbs_obj.data 
    if len(mesh.vertex_colors) == 0:
        bpy.ops.mesh.vertex_color_add()
    nurbs_obj.active_material = bpy.data.materials.new('material')
    nurbs_obj.active_material.use_vertex_color_paint = True
    print("test",nurbs_coords[1])
    #loop through each vertex
    num_verts = len(mesh.vertices)
    for vert_i in range(num_verts):
        #record shortest separation. -99 signals unset.
        shortest_sep = -99
        #loop through all the original bezier points to see 
        #which one is closest and then color it with the corresponding color
        count=0
        for b_point in nurbs_coords:
            b_point.resize_3d()
            temp_sep = (mesh.vertices[vert_i].co -  b_point).length
            if temp_sep < shortest_sep or shortest_sep == -99:
                shortest_sep = temp_sep
                color = color_list[count]
            count += 1
        color_vertex( nurbs_obj, vert_i, color )
        print( "Finished vertex: " + str(vert_i) + "/" + str(num_verts) )





def color_vertex(obj, vert, color=[1,0,0]):
    """
    Paints a single vertex

    """
    mesh = obj.data 
    scn = bpy.context.scene
    #check if our mesh already has Vertex Colors, and if not add some... (first we need to make sure it's the active object)
    scn.objects.active = obj
    obj.select = True
    if len(mesh.vertex_colors) == 0:
        bpy.ops.mesh.vertex_color_add()
    i=0
    for poly in mesh.polygons:
        for vert_side in poly.loop_indices:
            global_vert_num = poly.vertices[vert_side-min(poly.loop_indices)] 
            if vert == global_vert_num:
                mesh.vertex_colors[0].data[i].color = color
            i += 1



def remove_doubles(obj):
    """ Removes doubles using default settings"""
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='TOGGLE') #I believe objects are created with the vertices all not selected
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')



###obj = bpy.data.curves[ssname]
#color_nurbs_curve(ssname, rgb)



"""Converts the NURBS curve which should already have a bevel object so it has some width.
color_list should be a list of colors each of which is a 3 element list with [R,G,B]."""
nurbs_name = ssname
color_list = rgb

nurbs_obj = bpy.data.objects[nurbs_name + 'Object']
nurbs_curve_obj = bpy.data.curves[nurbs_name]
nurbs_coords = copy.deepcopy( [ nurbs_obj.data.splines[0].points[i].co for i in range(len(nurbs_obj.data.splines[0].points)) ] )

#Error checking
if len(nurbs_coords) != len(color_list):
    raise RuntimeError('The color list must have a number of colors equal to the number of control points of your bezier curve')

if nurbs_obj.data.bevel_object == None:
    raise RuntimeError('Your NURBS curve must have a bevel object')
    
scn = bpy.context.scene
#Convert to mesh
bpy.ops.object.mode_set(mode='OBJECT')
scn.objects.active = nurbs_obj
nurbs_obj.select = True
bpy.ops.object.convert( target='MESH' )
#sometimes this conversion results in a bunch of doubles, so I remove the doubles
remove_doubles(nurbs_obj)
mesh = nurbs_obj.data 



if len(mesh.vertex_colors) == 0:
    bpy.ops.mesh.vertex_color_add()


nurbs_obj.active_material = bpy.data.materials.new('material')
nurbs_obj.active_material.use_vertex_color_paint = True
print("test",nurbs_coords[1])
#loop through each vertex
num_verts = len(mesh.vertices)

for vert_i in range(num_verts):
    #record shortest separation. -99 signals unset.
    shortest_sep = -99
    #loop through all the original bezier points to see 
    #which one is closest and then color it with the corresponding color
    count=0
    for b_point in nurbs_coords:
        b_point.resize_3d()
        temp_sep = (mesh.vertices[vert_i].co -  b_point).length
        if temp_sep < shortest_sep or shortest_sep == -99:
            shortest_sep = temp_sep
            color = color_list[count]
        count += 1
    color_vertex( nurbs_obj, vert_i, color )
    print( "Finished vertex: " + str(vert_i) + "/" + str(num_verts) )





##### HRE



# (2) make sure you are in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# (3) alt-c -> then convert to mesh : bpy.ops.object.convert(target='MESH')
#      -> note - you can't see the faces unless you are in edit mode
bpy.ops.object.convert(target='MESH')




# now, figure out how to color this thing...oy
import random
tube = bpy.data.objects[sname]
tubemesh = bpy.data.objects[sname].data

if not tubemesh.vertex_colors:
    tubemesh.vertex_colors.new()

color_layer = tubemesh.vertex_colors["Col"]

rgb = []
for i in range(0,Nvals):
    rgb.append([random.random() for ii in range(3)])


i=0
ic = 0 # lets try this
p1 = (xn[0],yn[0],zn[0])
p2 = (xn[1],yn[1],zn[1])
for ip, poly in enumerate(tubemesh.polygons):
    #rgb = [random.random() for ii in range(3)]
    #xyz = tubemesh.vertices[0].co
    
    for idx in poly.loop_indices:
        color_layer.data[i].color = rgb
        i += 1

# set to vertex paint mode to see the result ... don't need to do this once we map vertex paint
#bpy.ops.object.mode_set(mode='VERTEX_PAINT')
# NOTE!!!! YOU WILL HAVE TO HAVE "render" OR "Material" view set!!!

# note, to render this, we have to do:
matName = tube.name + 'c'
color = (1,1,1)
mat = science.makeMaterial(matName, color, (1,1,1), 1.0, 1.0)
mat.use_vertex_color_paint = True
science.setMaterial(tube,mat) # sets everything to material 0 by default


# check out: http://blenderscripting.blogspot.com/2014/02/3d-tube-from-points.html
# for particles check out: http://yt-project.org/doc/analyzing/analysis_modules/particle_trajectories.html#particle-trajectories
# may or maynot be useful: http://blenderscripting.blogspot.com/2013/03/painting-vertex-color-map-using.html, http://blenderartists.org/forum/showthread.php?190693-Setting-Vertex-Color-via-Python, http://www.blender.org/api/blender_python_api_2_63_2/bpy.types.Mesh.html
