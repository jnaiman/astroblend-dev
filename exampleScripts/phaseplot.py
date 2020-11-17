import matplotlib.pyplot as plt
plt.use('TkAgg')
import science
import numpy as np
import yt


# Enzo data
filename = '~/data/IsolatedGalaxy/galaxy0030/galaxy0030'

ds = yt.load(filename)
#ad = ds.all_data()

sphere_rad = 200.0 # in kpc

my_sphere = ds.sphere("c", (sphere_rad, "kpc"))

# make a phase plot
plot = yt.PhasePlot(my_sphere, "density", "temperature", ["cell_mass"],weight_field=None)

plot.set_cmap("cell_mass", "hot")

imname = "MyImage777"


pp = plot.plots[('gas', 'cell_mass')]

ncols, nrows = pp.canvas.get_width_height()

# first, draw the canvas
pp.canvas.draw()

# then, fill the buffer
buff = pp.canvas.tostring_argb()
pixels_tmp = np.fromstring(buff, dtype=np.uint8).reshape((nrows, ncols, 4), order="C")

# switching a from back to front, and flipping image
pixels = np.array(pixels_tmp)
for i in range(0,nrows):
    pixels[i,:,3] = pixels_tmp[nrows-1-i,:,0]
    pixels[i,:,0] = pixels_tmp[nrows-1-i,:,1]
    pixels[i,:,1] = pixels_tmp[nrows-1-i,:,2]
    pixels[i,:,2] = pixels_tmp[nrows-1-i,:,3]


# blank image
image = bpy.data.images.new(imname, width=ncols, height=nrows)

image.pixels = pixels.ravel()/255.

# activate the image in the uv editor
for area in bpy.context.screen.areas:
    if area.type == 'IMAGE_EDITOR':
        area.spaces.active.image = image




## Also, hey, for fun, lets add in some iso surfaces
## Density will be the isosurface determinant - so pick 2 densities
#rho = [2e-27, 1e-27]
## transparencies of densities - inner is 100% opaque, outer is 50%
#transparencies = [1.0, 0.5]
#
## how is emissivity calculated?
#def _Emissivity(field, data):
#    return (data['gas','density']*data['density']*np.sqrt(data['gas','temperature']))
#
## isosurfaces at 2 and 1 x 10^-27
#myobject = science.Load(filename, scale = (50.0, 50.0, 50.0), isosurface_value = rho, 
#                        surf_type='sphere', radius = sphere_rad, 
#                        radius_units = "kpc", surface_field="density", 
#                        meshname = 'Allen', transparency = transparencies, 
#                        color_field='temperature', emit_field=_Emissivity) 

