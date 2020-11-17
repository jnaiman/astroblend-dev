#import science
import yt
import numpy as np
from yt.visualization.api import Streamlines
#from mathutils import Vector
import random
#from scipy import interpolate # need to activate correct yt version and do: pip3.4 install scipy


#fname = '/Users/jillnaiman/data/IsolatedGalaxy/galaxy0030/galaxy0030'
fname = '/Users/jillnaiman1/data/IsolatedGalaxy/galaxy0030/galaxy0030' # home

ssname = "MyStream"


# now, get stream line
ds = yt.load(fname)

c = np.array([0.5]*3)
N = 10  # number of stream lines
scale = 1.0
pos_dx = np.random.random((N,3))*scale-scale/2.
pos = c+pos_dx

streamlines = Streamlines(ds,pos,'velocity_x', 'velocity_y', 'velocity_z', length=1.0)



if False:
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
        colors[i,0] = random.random()
        colors[i,1] = random.random()
        colors[i,2] = random.random()


    # remap to a smaller number of points for simplicity
    Nvals = max(100,floor(len(stream)/20.0)) 
    #method='cubic' # or nearest, or linear - cubic takes awhile
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





    # make 2 meshes into one mesh
    def join_surfaces(name_list):
        science.deselect_all()
        # join objects
        bpy.context.scene.objects.active = bpy.data.objects[name_list[0]]
        for i in range(0,len(name_list)):
            bpy.data.objects[name_list[i]].select = True
        bpy.ops.object.join()


    # add in cylinders
    cyl_verts = 16
    ncylinders = Nvals # how many cylinders total?
    cyl_scale_xy = 0.01
    cyl_scale_z = 1.0/Nvals



    # for the first point




    # this will run through a trial of creating a mesh from python data..woo!
    # some parts taken from: http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Geometry
    import bpy

    # these are if you wanna change the colors or transparencies on the fly
    def makeMaterial(name, diffuse, specular, alpha, emiss):
        mat = bpy.data.materials.new(name)
        mat.emit = emiss # emissivity is up to 2.0!
        mat.diffuse_color = diffuse
        mat.diffuse_shader = 'LAMBERT' 
        mat.diffuse_intensity = 1.0 
        mat.specular_color = specular
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.5
        mat.alpha = alpha  # sets transparency (0.0 = invisable)
        mat.use_transparency = True # assumes Z-transparency
        return mat

    def setMaterial(ob, mat):
        me = ob.data
        me.materials.append(mat)


    # things for emissive lighting
    bpy.data.worlds['World'].light_settings.indirect_factor=20. 
    # have to use approximate, not ray tracing for emitting objects ...
    #   ... for now... 
    bpy.data.worlds['World'].light_settings.gather_method = 'APPROXIMATE' 
    bpy.data.worlds['World'].horizon_color = [0.0, 0.0, 0.0] # horizon = black
    bpy.data.worlds['World'].light_settings.use_indirect_light = True  # emitting things


    # CONE! 
    # Define the coordinates of the vertices. Each vertex is defined by 3 consecutive floats.
    coords=[(-1.0, -1.0, -1.0), (1.0, -1.0, -1.0), (1.0, 1.0 ,-1.0), \
    (-1.0, 1.0,-1.0), (0.0, 0.0, 1.0)]

    # Define the faces by index numbers. Each faces is defined by 4 consecutive integers.
    # For triangles you need to repeat the first vertex also in the fourth position.
    faces=[ (2,1,0,3), (0,1,4,0), (1,2,4,1), (2,3,4,2), (3,0,4,3)]

    me = bpy.data.meshes.new("PyramidMesh")   # create a new mesh  

    ob = bpy.data.objects.new("Pyramid", me)          # create an object with that mesh
    ob.location = bpy.context.scene.cursor_location   # position object at 3d-cursor
    bpy.context.scene.objects.link(ob)                # Link object to scene

    # Fill the mesh with verts, edges, faces 
    me.from_pydata(coords,[],faces)   # edges or faces should be [], or you ask for problems
    me.update(calc_edges=True)    # Update mesh with new data

    mat1 = makeMaterial('mat1', (0,0,1), (1,1,1), 0.75, 1.0) # blue, bright
    mat2 = makeMaterial('mat2', (0,1,0), (1,1,1), 0.75, 1.5) # green, brightest
    mat3 = makeMaterial('mat3', (1,0,0), (1,1,1), 0.75, 0.25) # red, dim

    # add on these materials
    obj = bpy.data.objects['Pyramid']
    setMaterial(obj,mat1) # sets everything to material 0 by default
    setMaterial(obj,mat2)
    setMaterial(obj,mat3)

    # set a few faces different colors
    me.polygons[4].material_index = 2
    me.polygons[0].material_index = 1
    me.polygons[1].material_index = 1
    me.polygons[2].material_index = 2
