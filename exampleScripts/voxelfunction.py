import bpy
from ctypes import *
import ctypes
import numpy as np
from science import setMaterial


class VoxelData(Structure):
    _fields_ = [("resol", c_int*3),
                ("interp_type", c_int),
                ("file_format", c_short),
                ("flag", c_short),
                ("extend", c_short),
                ("hair_type", c_short),
                ("data_type", c_short),
                ("_pad", c_int),
                ("Object", c_voidp),
                ("int_multiplier", c_float),
                ("still_frame", c_int),
                ("source_path", c_char*1024),
                ("dataset", POINTER(c_float)),
                ("cachedframe", c_int),
                ("ok", c_int)]


# this requires you have run the start up script
bpy.context.scene.HackTexture = True


def voxelcube(name='Cube000', left_edge = [0,0,0.], right_edge = [1,1,1], array = [0,0,0], res = (0,0,0)):
    # do this to start from clean slate
    from science import delete_object
    for ob in bpy.data.objects:
        if ob.name == 'Cube':
            delete_object('Cube')
    mat_name = name + 'Mat'
    tex_name = name + 'CubeTex'
    # first create but if it does exist
    flagg = True
    # do we have cube?
    for ob in bpy.data.objects:
        if ob.name == 'Cube':
            flagg = False
    if flagg:
        bpy.ops.mesh.primitive_cube_add(radius=1.0)
        bpy.data.objects['Cube'].name = name
    # put it in the center    
    bpy.data.objects[name].location = ((right_edge[0]+left_edge[0])*0.5,
                                       (right_edge[1]+left_edge[1])*0.5,
                                       (right_edge[2]+left_edge[2])*0.5)
    bpy.data.objects[name].scale = ((right_edge[0]-left_edge[0])*0.5,
                                    (right_edge[1]-left_edge[1])*0.5,
                                    (right_edge[2]-left_edge[2])*0.5)
    # make a material
    mat = bpy.data.materials.new(mat_name)
    mat.type = 'VOLUME'
    mat.volume.density = 0.0 # lower?
    mat.volume.density_scale = 1.0 # upper in the slice plot
    mat.volume.scattering = 0.5
    mat.volume.emission = 5.0
    mat.transparency_method = 'Z_TRANSPARENCY'
    mat.use_full_oversampling = True
    mat.use_mist = True
    mat.volume.step_method = 'CONSTANT'
    setMaterial(bpy.data.objects[name], mat)
    # Create texture from image sequence
    mtex = mat.texture_slots.add()
    mat.active_texture_index = 0
    tex = bpy.data.textures.new(tex_name, type = 'VOXEL_DATA')
    mat.active_texture = tex
    tex.use_color_ramp = True
    tex.voxel_data.file_format = 'BLENDER_VOXEL'
    # now, lets try to re-norm the min and max of the transfer function
    tex.color_ramp.elements[0].color = (0,0,0, array.min())
    tex.color_ramp.elements[1].color = (1,1,1, array.max())
    print(tex.color_ramp.elements[0].color[:])
    mat.texture_slots[0].texture_coords = 'ORCO' # generated coords
    mat.texture_slots[0].mapping = 'CUBE' # map to a cube
    # NO idea
    ts = mat.texture_slots[0]
    ts.use_map_density = True
    ts.density_factor = 1.0
    ts.use_map_emission = True
    ts.emission_factor = 1.0
    ts.use_map_color_emission = True
    ts.emission_color_factor = 1.0
    for i in range(3):
        tex.voxel_data.resolution[i] = res[i]
    vdp = ctypes.cast(bpy.data.textures[tex_name].voxel_data.as_pointer(),ctypes.POINTER(VoxelData))
    arr = (ctypes.c_float * array.size)()
    arr2 = np.ctypeslib.as_array(arr, array.shape)
    arr2[:] = array.flat[:]
    vdp.contents.dataset = ctypes.cast(arr, ctypes.POINTER(ctypes.c_float))
    vdp.contents.ok = 1
    vdp.contents.cachedframe = bpy.context.scene.frame_current


import yt
ds = yt.load("~/data/IsolatedGalaxy/galaxy0030/galaxy0030")

dd = ds.all_data()
mi, ma = np.log10(dd.quantities.extrema("density"))
for i, (g, node, (sl, dims, gi)) in enumerate(dd.tiles.slice_traverse()):
   LE = node.get_left_edge()
   RE = node.get_right_edge()
   #data = g["density"][sl]
   data = np.log10(g["density"][sl]).copy("C")
   #np.log10(data, data)
   data = (data - mi)/(ma - mi)
   #print(data.max())
   #print(data.min())
   voxelcube(name='Cube%05i' % i, left_edge = LE, right_edge = RE, array = data, res = data.shape)
   print(i)
   #print(LE, RE, data.shape)
   


