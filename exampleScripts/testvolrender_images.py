import bpy
#import dicom

mat_name = 'CubeMat'
tex_name = 'CubeTex'

# use yt to input an image? or link to an image sequence
use_yt = False


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)    

import yt
import numpy as np
datafile = '~/data/IsolatedGalaxy/galaxy0030/galaxy0030'
ds = yt.load(datafile)
dd = ds.all_data()
level = 4
all_data = ds.covering_grid(level=level, left_edge=[0,0.0,0.0],dims=ds.domain_dimensions*2**level)
pointdata = np.log10(all_data['density']).flatten()
pointdata_save = np.array(pointdata)
# rescale from 0->1
minp = pointdata.min()
maxp = pointdata.max()
for i in range(0,len(pointdata)):
    pointdata[i] = translate(pointdata[i], minp, maxp, 0, 1.)
# set low bounds = 0
pointdata[pointdata_save < -27] = 0.0



#print("loading dicom data")
#ds = dicom.read_file("C:/Dev/stack/238.dcm")
#dcm_pixel = ds.pixel_array.flat.copy()


#create an image with width/height same size as ds_image.
print("creating a new image")
img_size = data.pixel_array.shape
print(img_size)
bpy.ops.image.new(name="DICOM", width=img_size[0], height=img_size[0], color=(0, 0, 0, 1), alpha=True, uv_test_grid=False, float=False)
img = bpy.data.images["DICOM"]


#build an array to create iage pixel data
print("Building a blank array")
img_array = [0 for pix in range(len(img.pixels))]
print(len(img_array))
print(4*512*512)




#in the future, need to normalize across volume, not individual slices...too lazy
normal = max(dcm_pixel)
print(normal)




#populate the array with the pixel data
print("populate the array with our dicom data")
for i in range(0,len(dcm_pixel)):
img_array[4*i] = dcm_pixel[i]/normal
img_array[4*i + 1] = dcm_pixel[i]/normal
img_array[4*i + 2] = dcm_pixel[i]/normal


#http://blenderartists.org/forum/showthread.php?195230-im-getpixel()-or-equivalent-in-Blender-2-5
#http://code.google.com/p/pydicom/wiki/WorkingWithPixelData
#http://blenderscripting.blogspot.com/2012/08/adjusting-image-pixels-internally-in.html


img.pixels = img_array
