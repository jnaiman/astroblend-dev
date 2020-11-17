import science
import yt
import matplotlib.pyplot as plt
import numpy as np
import bmesh
from scienceutils import join_surfaces

filename = '/Users/jillnaiman/data/TipsyGalaxy/galaxy.00300'

ds = yt.load(filename, n_ref=8)
color_field = ('Gas', 'Temperature') 

color_log = True
color_map = 'Rainbow'

# these two things play off eachother!
halo_size = 0.108 # need to play with this
set_cam = (0,0,70)

scale = [(1.0, 1.0, 1.0)]

# strip "/" for naming
xnn2 = 0
xnn = 0
# you only want the file name, not all the directory stuff
while xnn != -1:
    xnn2 = xnn
    xnn = filename.find('/',xnn+1)

fname_out = filename[xnn2+1:]            



dd = ds.all_data()
xcoord = dd['Gas','Coordinates'][:,0].v
ycoord = dd['Gas','Coordinates'][:,1].v
zcoord = dd['Gas','Coordinates'][:,2].v
cs = dd[color_field]

# map colorcode to 256 material colors
if color_log: cs = np.log10(cs)

mi, ma = cs.min(), cs.max()
cs = (cs - mi) / (ma - mi)


from yt.visualization._colormap_data import color_map_luts # import colors for mtl file
# the rgb colors
colors = color_map_luts[color_map]

x = np.mgrid[0.0:1.0:colors[0].shape[0]*1j]
# how the values map to the colors
color_index = (np.interp(cs,x,x)*(colors[0].shape[0]-1)).astype("uint8") 
color_index_list = color_index.tolist()


# create sph data into meshes and color them
for ind in range(color_index.min(), color_index.max()):
    cl = [i for i,j in enumerate(color_index_list) if j == ind]
    if len(cl) > 0:
        fname = fname_out + '_' + str(ind)
        me = bpy.data.meshes.new('particleMesh_'+fname)
        ob = bpy.data.objects.new('particle_'+fname,me)
        ob.location = (0,0,0)
        bpy.context.scene.objects.link(ob)    # Link object to scene
        coords = [(0,0,0)]
        me.from_pydata(coords,[],[])
        ob.location = (0,0,0)
        ob = bpy.data.objects['particle_'+fname] # select right object
        science.deselect_all()
        ob.select = True
        bpy.context.scene.objects.active=ob
        mat = science.makeMaterial('particle_'+str(ind), 
                                   (colors[0][ind],colors[1][ind],colors[2][ind]), 
                                   (1,1,1), 1.0, 1.0, mat_type = 'HALO', halo_size=halo_size)
        science.setMaterial(ob,mat)
        # add in verts
        bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
        bm = bmesh.from_edit_mesh(ob.data)
        # now, find all verts with this color index (ind)
        # move original vertex to actual location
        bm.verts[0].co = (xcoord[cl[0]]*scale[0][0],ycoord[cl[0]]*scale[0][1],zcoord[cl[0]]*scale[0][2])
        for i in range(1,len(xcoord[cl])):
            bm.verts.new((xcoord[cl[i]]*scale[0][0],ycoord[cl[i]]*scale[0][1],zcoord[cl[i]]*scale[0][2]))
        bmesh.update_edit_mesh(ob.data)
        bpy.ops.object.mode_set(mode='OBJECT')

# NOOOOPE loses the colors :(    
# now join up into one happy surface
## (i) find first particle set
#flagg = -1
#for obj in bpy.data.objects:
#    name = obj.name
#    if (name.find(fname_out) != -1) and (flagg != -1): # combine
#        name_array = [name_array1, name]
#        join_surfaces(name_array)
#    if (name.find(fname_out) != -1) and (flagg == -1): # first instance, name array
#        name_array1 = name
#        flagg = 1
    


cam = science.Camera()
cam.location = set_cam
cam.clip_begin = 0.0001

lighting = science.Lighting('EMISSION')

