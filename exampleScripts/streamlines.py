import science
import yt
import numpy as np
from yt.visualization.api import Streamlines

fname = '/Users/jillnaiman/data/IsolatedGalaxy/galaxy0030/galaxy0030'

ds = yt.load(fname)

c = np.array([0.5]*3)
N = 100
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

# ok, lets assume streamlines works
from mathutils import Vector
 
# weight
w = 1
 
# we don't have to use the Vector() notation.
#listOfVectors = [(0,0,0),(1,0,0),(2,0,0),(2,3,0),(0,2,1)]  ### points from streamlines
# rgb color at each point
#                white   red     yellow  green   blue
colorpoints =   [(1,1,1),(1,0,0),(1,1,0),(0,1,0),(0,0,1)]
ssname = "NameOfMyCurve2"
sname = ssname + "Object"


def MakePolyLine(objname, curvename, cList):
    curvedata = bpy.data.curves.new(name=curvename, type='CURVE')
    curvedata.dimensions = '3D'
    objectdata = bpy.data.objects.new(objname, curvedata)
    objectdata.location = (0,0,0) #object origin
    bpy.context.scene.objects.link(objectdata)
    polyline = curvedata.splines.new('NURBS')
    polyline.points.add(len(cList)-1)
    for num in range(len(cList)):
        polyline.points[num].co = (cList[num])+(w,)
    polyline.order_u = len(polyline.points)-1
    polyline.use_endpoint_u = True


MakePolyLine(sname, ssname, tuple(map(tuple,stream)))
 
obj = bpy.data.objects[sname]
obj.data.fill_mode = 'FULL'
obj.data.bevel_depth = 0.1
obj.data.bevel_resolution = 15 

# don't think we want this part
#solidify = obj.modifiers.new(type='SOLIDIFY', name="make_solid")
#solidify.thickness = -0.02 


# now, we need to make this thing into a mesh

# (1) select object
science.deselect_all()
bpy.data.objects[sname].select = True
bpy.context.scene.objects.active = bpy.data.objects[sname]


# (2) make sure you are in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# (3) alt-c -> then convert to mesh : bpy.ops.object.convert(target='MESH')
#      -> note - you can't see the faces unless you are in edit mode
bpy.ops.object.convert(target='MESH')


def duplicateObject(scene, name, copyobj):
    # Create new mesh
    mesh = bpy.data.meshes.new(name) 
    # Create new object associated with the mesh
    ob_new = bpy.data.objects.new(name, mesh) 
    # Copy data block from the old object into the new object
    ob_new.data = copyobj.data.copy()
    ob_new.scale = copyobj.scale
    ob_new.location = copyobj.location
    ob_new.rotation_euler = copyobj.rotation_euler 
    # Link new object to the given scene and select it
    scene.objects.link(ob_new)
    ob_new.select = True 
    return ob_new



# now, deciment the mesh... I think
fname = sname

lowResname=None 
RemeshMode='SMOOTH'
RemeshScale = 0.7
scene_name = None
if scene_name is None:
    scene_name = 'Scene'

scene = bpy.data.scenes[scene_name]
###highRes = bpy.data.objects[fname]
###if lowResname is None:
###    lowResname = 'LowRes'

# (I) duplicate highres
##duplicateObject(scene,lowResname,highRes)
###lowRes = bpy.data.objects[lowResname]
lowRes = bpy.data.objects[fname]
# need this to select only the one object
bpy.context.scene.objects.active = bpy.data.objects[fname]
# (II) remesh high res to low res grid
# Add a modifier = remesh
bpy.ops.object.modifier_add(type='REMESH')
# select the smooth remesh
bpy.data.objects[fname].modifiers['Remesh'].mode = RemeshMode
# scale the amount of blocks, seems like ~0.7 is ok?
bpy.data.objects[fname].modifiers['Remesh'].scale = RemeshScale
# apply the modifier
bpy.ops.object.modifier_apply(apply_as='DATA',modifier='Remesh')

# delete high rez object
###science.delete_object(fname)
###lowRes.name = fname


# now, figure out how to color this thing...oy
import random
tube = bpy.data.objects[sname]
tubemesh = bpy.data.objects[sname].data

if not tubemesh.vertex_colors:
    tubemesh.vertex_colors.new()

color_layer = tubemesh.vertex_colors["Col"]


i=0
for poly in tubemesh.polygons:
    #rgb = [random.random() for ii in range(3)]
    xyz = tubemesh.vertices[0].co
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
