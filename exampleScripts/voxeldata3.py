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



# do this to start from clean slate
from science import delete_object
for ob in bpy.data.objects:
    if ob.name == 'Cube':
        delete_object('Cube')
    

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
mat.volume.density_scale = 1.0 # upper in the slice plot
mat.volume.scattering = 0.5 # look far in
mat.volume.emission = 5.0 # super bright
mat.transparency_method = 'Z_TRANSPARENCY'
# this makes things pretty
mat.use_full_oversampling = True
mat.use_mist = True
mat.volume.step_method = 'CONSTANT' # for pretty too

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



# this requires you have run the start up script
bpy.context.scene.HackTexture = True

level = 5


rez = 32*2**level



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


# do nice color stuff
nn = 6
for i in range(0,6):
    el = tex.color_ramp.elements.new((i)/(nn-1.))


tex.color_ramp.elements[1].color = (0,0,0, 0.1)
    
tex.color_ramp.elements[2].color = (0.008940682746469975, 0.025149978697299957, 0.2500000596046448, 0.25)

tex.color_ramp.elements[3].color = (0.3750000596046448, 0.016165535897016525, 0.3095288872718811, 0.3750000298023224)

tex.color_ramp.elements[4].color = (0.29114043712615967, 0.12912243604660034, 0.3539966344833374, 0.4041827619075775)

tex.color_ramp.elements[5].color = (0.015799466520547867, 0.5, 0.5, 0.5)    

tex.color_ramp.interpolation = 'EASE'


bpy.data.scenes['Scene'].render.filepath = '/Users/jillnaiman1/image.jpg'
bpy.ops.render.render( write_still=True )


# properties region
#a = bpy.context.window.screen.areas[1]


#a.regions[2]


#bpy.context.space_data.context = 'MATERIAL'
