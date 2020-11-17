import matplotlib.pyplot as plt
#import yt.visualization._mpl_imports as mpl
from io import BytesIO
import yt
import time
import numpy as np
import bpy
from scienceutils import makeMaterial, setMaterial, delete_unused_materials, delete_unused_textures, delete_unused_images

# test:
'''
filename = '/Users/jillnaiman1/data/IsolatedGalaxy/galaxy0030/galaxy0030'
from yt import load
ds = load(filename)
import science
image_name = 'SlicePlot'
science.plots.ytSlicePlot(ds, image_name = image_name, center=[0.5, 0.5, 0.5], width=20.0)
'''


class ytSlicePlot(object):
    def __init__(self, ds, image_name = "ytSliceImage", axis='z', variable='density',
                 center=[0.0, 0.0, 0.0], width = 10.0, units = 'kpc', color_map = 'hot',
                 show_annotations = True):
        from yt import SlicePlot
        p = SlicePlot(ds, axis, variable, center = center, width = (width, units))
        p.hide_axes()
        p.hide_colorbar()
        p.set_cmap(variable, color_map)
        p._setup_plots()
        plot = p.plots[variable]
        plot.canvas.draw()
        buff = plot.canvas.tostring_argb()
        ncols, nrows = plot.canvas.get_width_height()
        vv = np.fromstring(buff, dtype=np.uint8).reshape((nrows, ncols, 4), order="C")
        if show_annotations:
            p = SlicePlot(ds, axis, variable, center = center, width = (width, units))
            p.set_cmap(variable, color_map)
            p._setup_plots()
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




'''        
        ncols = vv.shape[1]
        nrows = vv.shape[0]
        flagg = True
        for image in bpy.data.images:
            if image.name == image_name:
                delete_unused_images(image_name)
                delete_unused_textures(image_name)
                delete_unused_materials(image_name)

        image = bpy.data.images.new(image_name, width=ncols, height=nrows)
        image.pixels = pixels
        
        # activate the image in the uv editor
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.spaces.active.image = image
            elif area.type == 'VIEW_3D': # make sure material/render view is on
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if (space.viewport_shade != 'RENDERED') and (space.viewport_shade != 'MATERIAL'):
                            space.viewport_shade = 'RENDERED'

        # also, attach to the slice in the blender 3d window
        # now, set color
        figmat = makeMaterial(image_name, (0,0,0), (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
        setMaterial(bpy.data.objects[image_name], figmat)
        # also, make shadeless
        bpy.data.materials[image_name].use_shadeless = True

        # Create image texture from image
        cTex = bpy.data.textures.new(image_name, type = 'IMAGE')
        # try this for desplay purposes
        #pixels2 = pixels[::-1]
        #print(pixels)
        #print(pixels2)
        #from copy import deepcopy
        #image2 = deepcopy(image)
        #image2.pixels = pixels2
        cTex.image = image
        # Add texture slot for color texture
        mat = bpy.data.materials[image_name]
        mtex = mat.texture_slots.add()
        mtex.texture = cTex
        mtex.texture_coords = 'OBJECT' # this seems to work better for figures, but certainly needs to be tested
        mtex.use_map_color_diffuse = True 
        mtex.use_map_color_emission = True 
        mtex.emission_color_factor = 0.5
        mtex.use_map_density = True 
        mtex.mapping = 'FLAT' 

        # map to object
        mtex.object = bpy.data.objects[image_name]

'''

class ytProjectionPlot(object):
    def __init__(self, ds, image_name = "ytProjectionImage", axis='z', variable=('gas','temperature'),
                 weight_variable = ('gas','density'), 
                 center=[0.0, 0.0, 0.0], width = 10.0, units = 'kpc', color_map = 'algae',
                 show_annotations = False):
        from yt import ProjectionPlot, OffAxisProjectionPlot
        if (axis != 'z') and (axis != 'y') and (axis != 'x'):
            p = OffAxisProjectionPlot(ds,axis,variable,width=(width, units), weight_field = weight_variable)
            #plot = p.plots[variable]
            #fig = plot.figure
            #f = BytesIO()
            #vv = yt.write_image(np.log10(p.frb[variable][:,:-1].d),f, cmap_name = color_map)
            p.hide_axes()
            p.hide_colorbar()
            p.set_cmap(variable, color_map)
            p._setup_plots()
            plot = p.plots[variable]
            plot.canvas.draw()
            buff = plot.canvas.tostring_argb()
            ncols, nrows = plot.canvas.get_width_height()
            vv = np.fromstring(buff, dtype=np.uint8).reshape((nrows, ncols, 4), order="C")
            if show_annotations:
                p = OffAxisProjectionPlot(ds,axis,variable,width=(width, units), weight_field = weight_variable)
                p.set_cmap(variable, color_map)
                p._setup_plots()
                plot = p.plots[variable]
                plot.canvas.draw()
                buff2 = plot.canvas.tostring_argb()
                ncols2, nrows2 = plot.canvas.get_width_height()
                vv2 = np.fromstring(buff2, dtype=np.uint8).reshape((nrows2, ncols2, 4), order="C")
                #plot.canvas.draw()
                #buff = plot.canvas.tostring_argb()
                #ncols2, nrows2 = plot.canvas.get_width_height()
                #vv2 = np.fromstring(buff, dtype=np.uint8).reshape((nrows2, ncols2, 4), order="C")
        else:
            p = ProjectionPlot(ds, axis, variable, center=center, width=(width,units), weight_field=weight_variable)
            #plot = p.plots[variable]
            #fig = plot.figure
            #f = BytesIO()
            #vv = yt.write_image(np.log10(p.frb[variable][:,:-1].d),f, cmap_name = color_map)
            p.hide_axes()
            p.hide_colorbar()
            p.set_cmap(variable, color_map)
            p._setup_plots()
            plot = p.plots[variable]
            plot.canvas.draw()
            buff = plot.canvas.tostring_argb()
            ncols, nrows = plot.canvas.get_width_height()
            vv = np.fromstring(buff, dtype=np.uint8).reshape((nrows, ncols, 4), order="C")
            
            if show_annotations:
                p = ProjectionPlot(ds, axis, variable, center=center, width=(width,units), weight_field=weight_variable)
                p.set_cmap(variable, color_map)
                p._setup_plots()
                plot = p.plots[variable]
                plot.canvas.draw()
                buff2 = plot.canvas.tostring_argb()
                ncols2, nrows2 = plot.canvas.get_width_height()
                vv2 = np.fromstring(buff2, dtype=np.uint8).reshape((nrows2, ncols2, 4), order="C")
                #plot.canvas.draw()
                #buff = plot.canvas.tostring_argb()
                #ncols2, nrows2 = plot.canvas.get_width_height()
                #vv2 = np.fromstring(buff, dtype=np.uint8).reshape((nrows2, ncols2, 4), order="C")



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







'''                
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
#        pixels_tmp = np.zeros([ncols, nrows, 4])
        pixels_tmp = np.array(vv)
        for i in range(0,nrows):
            #pixels_tmp[i,:,3] = vv[:,ncols-1-i,0]
            #pixels_tmp[i,:,0] = vv[:,ncols-1-i,1]
            #pixels_tmp[i,:,1] = vv[:,ncols-1-i,2]
            #pixels_tmp[i,:,2] = vv[:,ncols-1-i,3]
            #pixels_tmp[i,:,3] = vv[nrows-1-i,:,0]
            #pixels_tmp[i,:,0] = vv[nrows-1-i,:,1]
            #pixels_tmp[i,:,1] = vv[nrows-1-i,:,2]
            #pixels_tmp[i,:,2] = vv[nrows-1-i,:,3]
            pixels_tmp[i,:,0] = vv[i,:,0]
            pixels_tmp[i,:,1] = vv[i,:,1]
            pixels_tmp[i,:,2] = vv[i,:,2]
            pixels_tmp[i,:,3] = vv[i,:,3]

        # flip
        #nc = ncols
        #ncols = nrows
        #nrows = nc
        
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
'''


class ytPhasePlot(object):
    def __init__(self, ds, image_name = "ytPhasePlotImage", xvar = ('gas','density'), yvar = ('gas', 'temperature'),
                 color_field = ('gas','cell_mass'), weight_field = None, sphere_radius = 200.0, 
                 center="c",  sphere_units = 'kpc', color_map = 'algae'):
        from yt import PhasePlot
        # generate plot
        my_sphere = ds.sphere(center, (sphere_radius, sphere_units))
#        my_sphere = ds.sphere("c", (sphere_radius, sphere_units))
        print("HERE!!!!")
        print(center)
        print(sphere_radius)
        print(sphere_units)
        print(xvar)
        print(yvar)
        print(color_field)
        print(weight_field)
        plot = PhasePlot(my_sphere, xvar, yvar, [color_field],weight_field=weight_field)
        plot.set_cmap(color_field, color_map)
        plot._setup_plots()
        pp = plot.plots[color_field]
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
        image = bpy.data.images.new(image_name, width=ncols, height=nrows)

        image.pixels = pixels.ravel()/255.

        # activate the image in the uv editor
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.spaces.active.image = image


    

