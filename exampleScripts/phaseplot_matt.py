import matplotlib.pyplot as plt
import yt.visualization._mpl_imports as mpl
from io import BytesIO
import yt
import time
import numpy as np

imname = 'Image6'

ds = yt.load("~/data/IsolatedGalaxy/galaxy0030/galaxy0030")
p = yt.ProjectionPlot(ds, "x", "density")
p.save("hi.png")
plot = p.plots["density"]
fig = plot.figure
f = BytesIO()
vv = yt.write_image(np.log10(p.frb["density"][:,:-1].d),f)
pixels = (vv/255.).ravel()

ncols = vv.shape[1]
nrows = vv.shape[0]
image = bpy.data.images.new(imname, width=ncols, height=nrows)
image.pixels = pixels

# activate the image in the uv editor
for area in bpy.context.screen.areas:
    if area.type == 'IMAGE_EDITOR':
        area.spaces.active.image = image
