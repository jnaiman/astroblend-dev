#typedef struct VoxelData {
#	int resol[3];
#	int interp_type;
#	short file_format;
#	short flag;
#	short extend;
#	short smoked_type;
#	short hair_type;
#	short data_type;
#	int _pad;
#	
#	struct Object *object; /* for rendering smoke sims */
#	float int_multiplier;
#	int still_frame;
#	char source_path[1024];  /* 1024 = FILE_MAX */
#
#	/* temporary data */
#	float *dataset;
#	int cachedframe;
#	int ok;
#	
#} VoxelData;

#import ctypes
from ctypes import *
import ctypes
import numpy as np
from science import setMaterial
import bpy


filevoxout = '/Users/jillnaiman1/Desktop/test1_ytl4_l1en27.bvox'

#Object = bpy.data.objects['Cube']

# done by hand:
# resol = 512, 512, 512
# interp_type = 1
# file_format = 0
# flag = 0
# extend = 2
# hair_type = 0
# data_type = 0
# _pad = 0
# Object = Nothing
# int_multiplier = 1.0
# still_frame = 0
# source_path = b'/Users/jillnaiman1/Desktop/test1_ytl4_l1en27.bvox'
# dataset = <__main__.LP_c_float object at 0x11dea31e0>
# cachedframe = 0
# ok = 1


# with code
# cachedframe = -1
# ok = 0
# source_path = b''


class VoxelData(Structure):
    _fields_ = [("resol", c_int*3), # NOTE this really is supposed to be 3 numbers
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
                ("source_path", c_char*1024), # this is probably wrong
                ("dataset", POINTER(c_float)),
                ("cachedframe", c_int),
                ("ok", c_int)]
    # NOTE!!! what to do about *dataset???



mat_name = 'CubeMat'
tex_name = 'CubeTex'

# first create but if it does exist
flagg = True
# do we have cube?
for ob in bpy.data.objects:
    if ob.name == 'Cube':
        flagg = False

if flagg:
    bpy.ops.mesh.primitive_cube_add(radius=1.0)


# put it in the center    
bpy.data.objects['Cube'].location = (0,0,0.)


# make a material
mat = bpy.data.materials.new(mat_name)
mat.type = 'VOLUME'
mat.volume.density = 0.0 # lower?
mat.volume.density_scale = 2.0 # upper in the slice plot
mat.volume.scattering = 1.4
mat.volume.emission = 0.0
mat.transparency_method = 'Z_TRANSPARENCY'

setMaterial(bpy.data.objects['Cube'], mat)

# Create texture from image sequence
mtex = mat.texture_slots.add()
mat.active_texture_index = 0

# this should work but it doesnt right now...
tex = bpy.data.textures.new(tex_name, type = 'VOXEL_DATA')
mat.active_texture = tex

tex.use_color_ramp = True

tex.voxel_data.file_format = 'BLENDER_VOXEL'
#tex.voxel_data.file_format = 'BLENDER_VOXEL'

tex.voxel_data.filepath = filevoxout

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
    tex.voxel_data.resolution[i] = 512




vdp = ctypes.cast(bpy.data.textures[tex_name].voxel_data.as_pointer(),ctypes.POINTER(VoxelData))

import yt
ds = yt.load("~/data/IsolatedGalaxy/galaxy0030/galaxy0030")
cg = ds.covering_grid(4, [0,0,0], (512,512,512))
rho = np.log10(cg["density"])
rho = (rho-rho.min())/(rho.max()-rho.min())
rho = rho.astype("float32").copy()
rho = np.ascontiguousarray(rho)
arr = (ctypes.c_float * rho.size)()
arr2 = np.ctypeslib.as_array(arr, rho.shape)
arr2[:] = rho.flat[:]

vdp.contents.dataset = ctypes.cast(arr, ctypes.POINTER(ctypes.c_float))
vdp.contents.ok = 1
vdp.contents.cachedframe = bpy.context.scene.frame_current

print (rho.strides)
