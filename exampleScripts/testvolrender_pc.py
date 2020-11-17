#filename = '~/data/TipsyGalaxy/galaxy.00300'
## sph or amr?
#file_type = 'sph'


filename = '~/data/IsolatedGalaxy/galaxy0030/galaxy0030'
file_type = 'amr'


from yt import load
import numpy as np
import bmesh
from scienceutils import deselect_all
from scienceutils import makeMaterial, setMaterial, delete_object


# remap to 0->1 for emissivity range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)    



ds = load(filename)

if file_type == 'sph':
    # get coords and color data
    dd = ds.all_data()
    #xcoord = dd['Gas','Coordinates'][:,0].v
    #ycoord = dd['Gas','Coordinates'][:,1].v
    #zcoord = dd['Gas','Coordinates'][:,2].v
    xcoord = (dd['Gas','Coordinates'][:,0].in_units('unitary')).v
    ycoord = (dd['Gas','Coordinates'][:,1].in_units('unitary')).v
    zcoord = (dd['Gas','Coordinates'][:,2].in_units('unitary')).v
    cs = dd[('Gas', 'Density')]
    color_log = True
    if color_log: cs = np.log10(cs)


if file_type == 'amr':
    dd = ds.all_data()
    cs = dd['density']
    cs[cs < 0.0] = 1e-50
    cs = np.log10(cs.value)
    xcoord = dd['x']
    ycoord = dd['y']
    zcoord = dd['z']
#    level = 2
#    all_data = ds.covering_grid(level=level, left_edge=[0,0.0,0.0],dims=ds.domain_dimensions*2**level)
#    pointdata = np.log10(all_data['density']).flatten()
#    pointdata_save = np.array(pointdata)
#    # rescale from 0->1
#    minp = pointdata.min()
#    maxp = pointdata.max()
#    for i in range(0,len(pointdata)):
#        pointdata[i] = translate(pointdata[i], minp, maxp, 0, 1.)
#    # set low bounds = 0
#    pointdata[pointdata_save < -27] = 0.0
#    cs = pointdata



mi, ma = cs.min(), cs.max()
cs = (cs - mi) / (ma - mi)


#for i in range(0,len(cs)):
#    cs[i] = translate(cs[i],mi, ma, 0.0, 1.0)

#cs = cs.value

particle_name_base = 'particle_cloud'

# how many levels of "density"
ndens = 10

# re-map to this bin size
pn = 0
pn_names = []
for i in range(1,ndens):
    ind = np.where( (cs < 1.0*i/(ndens-1.)) & (cs >= 1.0*(i-1)/(ndens-1.)) )[0]
    if len(ind) > 0:
        #print(ind)
        # ok, plot only things with this range of "densities"
        particle_name = particle_name_base + str(pn).zfill(3)
        # create sph data into meshes and color them
        me = bpy.data.meshes.new(particle_name)
        ob = bpy.data.objects.new(particle_name,me)
        ob.location = (0,0,0)
        bpy.context.scene.objects.link(ob)    # Link object to scene
        coords = [(0,0,0)]
        me.from_pydata(coords,[],[])
        ob.location = (0,0,0)
        ob = bpy.data.objects[particle_name] # select right object
        deselect_all()
        ob.select = True
        bpy.context.scene.objects.active=ob
        # I think we *don't* want to set a material
        #mat = makeMaterial(particle_name, (1.0, 1,1), 
        #                   (1,1,1), 1.0, 1.0, mat_type = 'HALO', halo_size=0.0008)
        #setMaterial(ob,mat)
        # add in verts
        bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
        bm = bmesh.from_edit_mesh(ob.data)
        # now, find all verts with this color index (ind)
        # move original vertex to actual location
        if hasattr(bm.verts, "ensure_lookup_table"): # to make it work with 2.73
            bm.verts.ensure_lookup_table()
        # first coord
        bm.verts[0].co = (xcoord[ind[0]], ycoord[ind[0]],zcoord[ind[0]])
        for i in range(1,len(xcoord[ind])):
            bm.verts.new((xcoord[ind[i]],ycoord[ind[i]],zcoord[ind[i]]))
        bmesh.update_edit_mesh(ob.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        print(bpy.data.objects[particle_name].location)
        pn_names.append(str(pn).zfill(3))
        pn += 1




# for now, lets scale things up to make a bigger cloud...if sph
if file_type = 'sph':
    for ob in bpy.data.objects:
        if ob.name.find(particle_name_base) != -1:
            ob.scale = (100, 100, 100)


# we'll keep the name cube... for now
cube_name_base = 'Cube'



mat_name_base = cube_name_base + 'Mat'
tex_name_base = cube_name_base + 'Tex'



# how big points should be
pc_radius = 0.01
base_level = 0.0

for i in range(0,len(pn_names)):
#for i in range(2,3):
    # add acube
    cube_name = cube_name_base + str(i).zfill(3)
    flagg = True
    for ob in bpy.data.objects:
        if ob.name == cube_name:
            flagg = False
    if flagg:
        radius = 1.0
        if file_type == 'amr':
            radius = 0.5
        bpy.ops.mesh.primitive_cube_add(radius=radius)
        bpy.data.objects['Cube'].name = cube_name
    else:
        delete_object(cube_name)
    cube = bpy.data.objects[cube_name]
    cube.location = (0,0,0)
    if file_type == 'amr':
        cube.location = (0.5, 0.5, 0.5)
    mat_name = mat_name_base + str(i).zfill(3)
    # make a material
    mat = bpy.data.materials.new(mat_name)
    mat.type = 'VOLUME'
    mat.volume.density = 0.0 # lower?
    mat.volume.density_scale = 1.0 # upper?
    mat.volume.scattering = 1.4
    mat.volume.emission = 0.0
    mat.transparency_method = 'Z_TRANSPARENCY'
    setMaterial(bpy.data.objects[cube_name], mat)
    # Create texture 
    mtex = mat.texture_slots.add()
    mat.active_texture_index = 0
    tex_name = tex_name_base + str(i).zfill(3)
    tex = bpy.data.textures.new(tex_name, type = 'POINT_DENSITY')
    mat.active_texture = tex
    tex.use_color_ramp = True
    bpy.data.textures[tex_name].point_density.point_source = 'OBJECT'
    bpy.data.textures[tex_name].point_density.object = bpy.data.objects[particle_name_base + str(i).zfill(3)]
    bpy.data.textures[tex_name].point_density.radius = pc_radius
    mat.texture_slots[0].texture_coords = 'ORCO' # generated coords
    mat.texture_slots[0].mapping = 'CUBE' # map to a cube
    # NO idea
    ts = mat.texture_slots[0]
    ts.use_map_density = True
    ts.density_factor = 1.0*i/(ndens-1.)+base_level
    ts.use_map_emission = True
    ts.emission_factor = 1.0*i/(ndens-1.)+base_level
    ts.use_map_color_emission = True
    ts.emission_color_factor = 1.0*i/(ndens-1.)+base_level
    #*** add in the opacity in the ramp here? from 0->1?




from science import Camera

cam = Camera()
cam.location = (0,0,2)


# to delete
if False:
    for ob in bpy.data.objects:
        if ob.name.find(cube_name_base) != -1:
            delete_object(ob)



       
