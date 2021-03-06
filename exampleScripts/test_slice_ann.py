from yt import load
from science import makeMaterial, setMaterial
import numpy as np

# need for testing
#import matplotlib as plt
#plt.use('TkAgg')
#plt.use('Agg')

ds = load('~/data/TipsyGalaxy/galaxy.00300')

axis = 'x'
variable = 'density'
center = [0., 0., 0.]
width = 200.0
units = 'kpc'
color_map = 'algae'
show_annotations = True

image_name = 'testslice44'


#my_sphere = ds.sphere(center, (width, units))

from yt import SlicePlot
#p = SlicePlot(my_sphere, axis, variable, center = center, width = (width, units))
p = SlicePlot(ds, axis, variable, center = center, width = (width, units))
p.hide_axes()
p.hide_colorbar()
plot = p.plots[variable]
p.set_cmap(variable, "hot")
p.save('~/Desktop/testslc.png')
#fig = plot.figure
#f = BytesIO()
#vv = yt.write_image(np.log10(p.frb[variable][:,:-1].d),f, cmap_name = color_map)
plot.canvas.draw()
buff = plot.canvas.tostring_argb()
ncols, nrows = plot.canvas.get_width_height()
vv = np.fromstring(buff, dtype=np.uint8).reshape((nrows, ncols, 4), order="C")


if show_annotations:
    p = SlicePlot(ds, axis, variable, center = center, width = (width, units))
    plot = p.plots[variable]
    plot.canvas.draw()
    buff2 = plot.canvas.tostring_argb()
    ncols2, nrows2 = plot.canvas.get_width_height()
    vv2 = np.fromstring(buff2, dtype=np.uint8).reshape((nrows2, ncols2, 4), order="C")


ncols = vv.shape[1]
nrows = vv.shape[0]

# delete if already there
for im in bpy.data.images:
    if im.name == image_name:
        delete_unused_images(image_name)
        delete_unused_textures(image_name)
        delete_unused_materials(image_name)

# for annotations
for im in bpy.data.images:
    if im.name == image_name+'_ann':
        delete_unused_images(image_name+'_ann')
        delete_unused_textures(image_name+'_ann')
        delete_unused_materials(image_name+'_ann')


# switching a from back to front, and flipping image
# if also with annotation do a nice one in the domain
pixels_tmp = np.array(vv)
for i in range(0,nrows):
    #pixels_tmp[i,:,0] = vv[i,:,0]
    #pixels_tmp[i,:,1] = vv[i,:,1]
    #pixels_tmp[i,:,2] = vv[i,:,2]
    #pixels_tmp[i,:,3] = vv[i,:,3]
    pixels_tmp[i,:,3] = vv[nrows-1-i,:,0]
    pixels_tmp[i,:,0] = vv[nrows-1-i,:,1]
    pixels_tmp[i,:,1] = vv[nrows-1-i,:,2]
    pixels_tmp[i,:,2] = vv[nrows-1-i,:,3]


if show_annotations:
    pixels_tmp2 = np.array(vv2)
    
if show_annotations:
    for i in range(0,nrows2):
        pixels_tmp2[i,:,3] = vv2[nrows2-1-i,:,0]
        pixels_tmp2[i,:,0] = vv2[nrows2-1-i,:,1]
        pixels_tmp2[i,:,1] = vv2[nrows2-1-i,:,2]
        pixels_tmp2[i,:,2] = vv2[nrows2-1-i,:,3]


# blank image
image = bpy.data.images.new(image_name, width=ncols, height=nrows)
if show_annotations:
    image2 = bpy.data.images.new(image_name + '_ann', width=ncols2, height=nrows2)

pixels = pixels_tmp.ravel()/255.
#pixels = vv.ravel()/255.
if show_annotations:
    pixels2 = pixels_tmp2.ravel()/255.

image.pixels = pixels
if show_annotations:
    image2.pixels = pixels2


# activate the image in the uv editor
for area in bpy.context.screen.areas:
    if area.type == 'IMAGE_EDITOR':
        if show_annotations:
            area.spaces.active.image = image2
        else:
            area.spaces.active.image = image
    elif area.type == 'VIEW_3D': # make sure material/render view is on
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                if (space.viewport_shade != 'RENDERED') and (space.viewport_shade != 'MATERIAL'):
                    space.viewport_shade = 'RENDERED' # material is too slow

# also, attach to the projection in the blender 3d window
# now, set color
figmat = makeMaterial(image_name, (0,0,0), (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
setMaterial(bpy.data.objects[image_name], figmat)
# also, make shadeless
bpy.data.materials[image_name].use_shadeless = True

# Create image texture from image
cTex = bpy.data.textures.new(image_name, type = 'IMAGE')
cTex.image = image
# Add texture slot for color texture
mat = bpy.data.materials[image_name]
mtex = mat.texture_slots.add()
mtex.texture = cTex
#mtex.texture_coords = 'UV'
mtex.texture_coords = 'OBJECT' # this seems to work better for figures, but certainly needs to be tested
mtex.use_map_color_diffuse = True 
mtex.use_map_color_emission = True 
mtex.emission_color_factor = 0.5
mtex.use_map_density = True 
mtex.mapping = 'FLAT' 

# map to object
mtex.object = bpy.data.objects[image_name]

#So to rotate around the x axis for example, you could create a quaternion with createFromAxisAngle(1, 0, 0, M_PI/2) and multiply it by the current rotation quaternion of your model.
def create_from_axis_angle( xx, yy, zz, a):
    # Here we calculate the sin( theta / 2) once for optimization
    from math import sin, cos
    result = sin( a / 2.0 )
    # Calculate the x, y and z of the quaternion
    x = xx * result
    y = yy * result
    z = zz * result
    #Calcualte the w value by cos( theta / 2 )
    w = cos( a / 2.0 )
    f = (x*x+y*y+z*z+w*w)**0.5
    return (x/f, y/f, z/f, w/f)
