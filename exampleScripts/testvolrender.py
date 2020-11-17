mat_name = 'CubeMat'
tex_name = 'CubeTex'

# use yt to input an image? or link to an image sequence
use_yt = False

# if using an image sequence, we need the name of the first file
#image_seq_dir = '/Users/jillnaiman1/data/cthead/'
#image_seq = 'cthead-8bit001.tif' # this is from: http://graphics.stanford.edu/data/voldata/mrbrain-8bit.tar.gz


# not-a-this
if False:
    #---------------------------------
    # first step, use yt to generate a bunch of images
    # pre generated
    generate_slices = False
    if generate_slices:
        import yt
        datafile = '~/data/IsolatedGalaxy/galaxy0030/galaxy0030'
        ds = yt.load(datafile)
        # number of slices
        nslice_start = 33
        nslice_end = 67
        for i in range(nslice_start, nslice_end):
            z = (i*1.0)/(nslice_end-nslice_start-1.)
            p = yt.SlicePlot(ds, 'z', 'density', center=[0.5, 0.5, z],width = (200,'kpc'))
            p.hide_axes()
            p.hide_colorbar()
            p.save('/Users/jillnaiman1/data/isolatedGalaxy_slices/slicefig-' + str(i+1-nslice_start).zfill(3) + '.png')
#
#    
#
    image_seq_dir = '/Users/jillnaiman1/data/isolatedGalaxy_slices/'
    image_seq = 'slicefig-001.png'
#
    #---------------------------------
    import numpy as np
#
    #specify dimensions header
    nx, ny, nz, nframes = 100,100,100,1
    header = np.array([nx,ny,nz,nframes])
#
    #create simple distance to origin texture
    x = np.linspace(-1,1,nx)
    y = np.linspace(-1,1,ny)
    z = np.linspace(-1,1,nz)
    zz,yy,xx = np.meshgrid(z,y,x,indexing='ij')
    pointdata = yy.flatten()**2+zz.flatten()**2+xx.flatten()**2
#
    #open and write to file
    binfile = open('/Users/jillnaiman1/Desktop/test1.bvox','wb')
    header.astype('<i4').tofile(binfile)
    pointdata.astype('<f4').tofile(binfile)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)    

generate_box = True    
#if generate_box:
import yt
import numpy as np
datafile = '~/data/IsolatedGalaxy/galaxy0030/galaxy0030'
ds = yt.load(datafile)
dd = ds.all_data()
level = 4
all_data = ds.covering_grid(level=level, left_edge=[0,0.0,0.0],dims=ds.domain_dimensions*2**level)
#pointdata = dd['density']/dd['density'].max()
pointdata = np.log10(all_data['density']).flatten()

pointdata_save = np.array(pointdata)


# rescale from 0->1
minp = pointdata.min()
maxp = pointdata.max()
for i in range(0,len(pointdata)):
    pointdata[i] = translate(pointdata[i], minp, maxp, 0, 1.)


# set low bounds = 0
pointdata[pointdata_save < -27] = 0.0

    
#pointdata /= pointdata.max()
nx, ny, nz, nframes = all_data['density'].shape[0], all_data['density'].shape[1], all_data['density'].shape[2],1
header = np.array([nx,ny,nz,nframes])
binfile = open('/Users/jillnaiman1/Desktop/test1_ytl4_l1en27.bvox','wb')
header.astype('<i4').tofile(binfile)
pointdata.astype('<f4').tofile(binfile)

#---------------------------------

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)




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
# more scattering = less the light penatrates into volume
mat.volume.scattering = 1.4
# make particles emissive?  I assume?... looks like it... we might have to
#  make different materials with different emissivities for different
#  emissivity of the gas
mat.volume.emission = 0.0
mat.transparency_method = 'Z_TRANSPARENCY'

setMaterial(bpy.data.objects['Cube'], mat)

# Create texture from image sequence
mtex = mat.texture_slots.add()
mat.active_texture_index = 0

# this should work but it doesnt right now...
tex = bpy.data.textures.new(tex_name, type = 'VOXEL_DATA')
#bpy.ops.texture.new()
#tex = bpy.data.textures['Texture']
#tex.name = tex_name
mat.active_texture = tex

tex.use_color_ramp = True

tex.voxel_data.file_format = 'IMAGE_SEQUENCE'

#if not use_yt: # generate from image seq
#bpy.ops.image.open(filepath=image_seq_dir+image_seq)
bpy.ops.image.open(filepath=image_seq_dir+image_seq, directory = image_seq_dir, files = [{"name":image_seq, "name":image_seq}], relative_path=True)

img = bpy.data.images[image_seq]
tex.voxel_data.filepath = image_seq_dir + image_seq
tex.image = img

img.source = 'SEQUENCE'

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



       
