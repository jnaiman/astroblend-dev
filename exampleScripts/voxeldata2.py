import bpy
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
#tex.voxel_data.file_format = 'SMOKE'
#tex.voxel_data.file_format = 'IMAGE_SEQUENCE'

#filevoxout = '/Users/jillnaiman1/Desktop/test1_ytl4_l1en27.bvox'
#tex.voxel_data.filepath = filevoxout

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


level = 4


rez = 32*2**level


# make an image... does not seem to work...
#bpy.ops.image.new(name="DummyImage4", width=rez, height=rez,
#                  color=(0, 0, 0, 1))
#img = bpy.data.images["DummyImage4"]
#img_array = [1 for pix in range(len(img.pixels))] # fill with zeros
#img.pixels = img_array
##tex.image = img

       

#for i in range(3):
#    tex.voxel_data.resolution[i] = -512
for i in range(3):
    tex.voxel_data.resolution[i] = rez

    
vdp = ctypes.cast(bpy.data.textures[tex_name].voxel_data.as_pointer(),ctypes.POINTER(VoxelData))

import yt
ds = yt.load("~/data/IsolatedGalaxy/galaxy0030/galaxy0030")
cg = ds.covering_grid(level, [0,0,0], (rez,rez,rez))
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

# NOTE for a pretty image you want this setup with "over sampling" checked in the materials panel: http://blender.stackexchange.com/questions/15010/rendering-a-3d-volume
