import bpy
from scienceutils import join_surfaces, deselect_all, makeMaterial, setMaterial



class ytGrid(object):
    def __init__(self, ds, grid_name="ytGrid", center = None, scale = [1., 1., 1.], thickness = 0.001):
        right_edge = ds.index.grid_right_edge.in_units('unitary')
        left_edge =  ds.index.grid_left_edge.in_units('unitary')

        if center is None:
            center = ds.domain_center.in_units('unitary')
            
        ng = 0
        center_grid = [right_edge[ng,0]-left_edge[ng,0],right_edge[ng,1]-left_edge[ng,1],right_edge[ng,2]-left_edge[ng,2]]
        #center_grid = [center_grid[0]*0.5+center[0],center_grid[1]*0.5+center[1], center_grid[2]*0.5+center[2]]
        #center_grid = [center_grid[0]*0.5,center_grid[1]*0.5, center_grid[2]*0.5]
        center_grid = [left_edge[ng,0]+center_grid[0]*0.5, left_edge[ng,1]+center_grid[1]*0.5, left_edge[ng,2]+center_grid[2]*0.5]
        
        bpy.ops.mesh.primitive_cube_add(radius=1.0)
        bpy.ops.object.modifier_add(type='WIREFRAME') # make wireframe
        start_name = bpy.context.scene.objects.active.name
        bpy.data.objects[start_name].name = grid_name
        bpy.data.objects[grid_name].location = (center_grid[0],center_grid[1],center_grid[2])
        # you need to divide by 2 since scale = 1 means a box takes up 2 BU blocks
        boxscalings = [right_edge[ng,0]-left_edge[ng,0],right_edge[ng,1]-left_edge[ng,1],right_edge[ng,2]-left_edge[ng,2]]
        bpy.data.objects[grid_name].scale = (scale[0]/2.*boxscalings[0], scale[1]/2.*boxscalings[1], scale[2]/2.*boxscalings[2])

        # loop through and make grids, join them
        for ng in range(1,len(right_edge[:,0])):
            active_grid = grid_name + 'tmp'
            center_grid = [right_edge[ng,0]-left_edge[ng,0],right_edge[ng,1]-left_edge[ng,1],right_edge[ng,2]-left_edge[ng,2]]
            center_grid = [left_edge[ng,0]+center_grid[0]*0.5, left_edge[ng,1]+center_grid[1]*0.5, left_edge[ng,2]+center_grid[2]*0.5]
            #center_grid = [center_grid[0]*0.5+center[0],center_grid[1]*0.5+center[1], center_grid[2]*0.5+center[2]]
            bpy.ops.mesh.primitive_cube_add(radius=1.0)
            bpy.ops.object.modifier_add(type='WIREFRAME') # make wireframe
            start_name = bpy.context.scene.objects.active.name
            bpy.data.objects[start_name].name = active_grid
            bpy.data.objects[active_grid].location = (center_grid[0],center_grid[1],center_grid[2])
            # you need to divide by 2 since scale = 1 means a box takes up 2 BU blocks
            boxscalings = [right_edge[ng,0]-left_edge[ng,0],right_edge[ng,1]-left_edge[ng,1],right_edge[ng,2]-left_edge[ng,2]]
            bpy.data.objects[active_grid].scale = (scale[0]/2.*boxscalings[0], scale[1]/2.*boxscalings[1], scale[2]/2.*boxscalings[2])
            # add to first grid by joining
            join_surfaces([grid_name,active_grid])

        # change thickness
        bpy.data.objects[grid_name].modifiers['Wireframe'].thickness = thickness




#def import_ytsph(filename, halo_sizes, color_field, color_map, color_log, n_ref, scale):
def import_ytsph(filename, halo_sizes, color_field, color_map, color_log, n_ref):

    from yt import load
    import numpy as np
    import bmesh
    from scienceutils import deselect_all
    from scienceutils import makeMaterial, setMaterial

    ds = load(filename)

    # strip "/" for naming
    xnn2 = 0
    xnn = 0
    # you only want the file name, not all the directory stuff
    while xnn != -1:
        xnn2 = xnn
        xnn = filename.find('/',xnn+1)

    fname_out = filename[xnn2+1:]            

    # get coords and color data
    dd = ds.all_data()
    #xcoord = dd['Gas','Coordinates'][:,0].v
    #ycoord = dd['Gas','Coordinates'][:,1].v
    #zcoord = dd['Gas','Coordinates'][:,2].v
    xcoord = (dd['Gas','Coordinates'][:,0].in_units('unitary')).v
    ycoord = (dd['Gas','Coordinates'][:,1].in_units('unitary')).v
    zcoord = (dd['Gas','Coordinates'][:,2].in_units('unitary')).v
    cs = dd[color_field]

    # map colorcode to 256 material colors
    if color_log: cs = np.log10(cs)

    mi, ma = cs.min(), cs.max()
    cs = (cs - mi) / (ma - mi)

    from yt.visualization._colormap_data import color_map_luts # import colors 
    # the rgb colors
    colors = color_map_luts[color_map]

    x = np.mgrid[0.0:1.0:colors[0].shape[0]*1j]
    # how the values map to the colors
    color_index = (np.interp(cs,x,x)*(colors[0].shape[0]-1)).astype("uint8")
    color_index_list = color_index.tolist()

    name = []
    hused = []
    scale = [(1.0, 1.0, 1.0)]
    # create scale if necessary
    if len(scale[:][:]) < color_index.max(): # generate larger scale
        sc = (scale[0][0], scale[0][1], scale[0][2])
        scale = []
        for i in range(color_index.min(), color_index.max()):
            scale.append(sc)

    # also, allow for multiple halo sizes
    if len(halo_sizes) < color_index.max():
        hs = halo_sizes[0]
        halo_sizes = []
        for i in range(color_index.min(), color_index.max()):
            halo_sizes.append(hs)

    # create sph data into meshes and color them
    for ind in range(color_index.min(), color_index.max()):
        cl = [i for i,j in enumerate(color_index_list) if j == ind]
        if len(cl) > 0:
            #print("particle name")
            #print(name)
            fname = fname_out + '_' + str(ind)
            name.append('particle_'+fname)
            hused.append(halo_sizes[ind])
            me = bpy.data.meshes.new('particleMesh_'+fname)
            ob = bpy.data.objects.new('particle_'+fname,me)
            ob.location = (0,0,0)
            bpy.context.scene.objects.link(ob)    # Link object to scene
            coords = [(0,0,0)]
            me.from_pydata(coords,[],[])
            ob.location = (0,0,0)
            ob = bpy.data.objects['particle_'+fname] # select right object
            deselect_all()
            ob.select = True
            bpy.context.scene.objects.active=ob
            mat = makeMaterial('particle_'+fname, 
                                       (colors[0][ind],colors[1][ind],colors[2][ind]), 
                                       (1,1,1), 1.0, 1.0, mat_type = 'HALO', halo_size=halo_sizes[ind])
            setMaterial(ob,mat)
            # add in verts
            bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
            bm = bmesh.from_edit_mesh(ob.data)
            # now, find all verts with this color index (ind)
            # move original vertex to actual location
            if hasattr(bm.verts, "ensure_lookup_table"): # to make it work with 2.73
                bm.verts.ensure_lookup_table()

            bm.verts[0].co = (xcoord[cl[0]]*scale[ind][0],ycoord[cl[0]]*scale[ind][1],zcoord[cl[0]]*scale[ind][2])
            #print('coords')
            #print(xcoord[cl[0]], ycoord[cl[0]], zcoord[cl[0]])
            for i in range(1,len(xcoord[cl])):
                bm.verts.new((xcoord[cl[i]]*scale[ind][0],ycoord[cl[i]]*scale[ind][1],zcoord[cl[i]]*scale[ind][2]))
            bmesh.update_edit_mesh(ob.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            #print(ind)
            #print(bpy.data.objects['particle_' + fname].name)
            print(bpy.data.objects['particle_' + fname].location)

    #print("NAME OUT HERE")
    #print(name)
    return name, ds, hused



# internal importer from yt
def _import_ytsurface(vertices, colors, alpha, emisses, colorindex, 
                      meshname='Steve', meshlocation=(0,0,0), plot_index=0):
    import numpy as np
    deselect_all()
    nftype = [("f1","int"),("f2","int"),("f3","int"),("f4","int")]
    newfaces = np.empty(int(len(vertices)/3.), dtype=nftype) # store sets of face colors
    cc = 0
    for i in range(0,int(len(vertices)/3.)):
        newfaces[i] = (cc, cc+1, cc+2, cc) # repeat last for triangles
        cc = cc+3
    me = bpy.data.meshes.new(meshname+"Mesh")
    ob = bpy.data.objects.new(meshname,me)
    ob.location = meshlocation   # position object at 3d-cursor
    bpy.context.scene.objects.link(ob)                # Link object to scene
    # Fill the mesh with verts, edges, faces 
    me.from_pydata(vertices.tolist(),[],newfaces.tolist())
    me.update(calc_edges=True)    # Update mesh with new data
    # materials woop woop!
    obj = bpy.data.objects[meshname]
    bpy.context.scene.objects.active=obj
    for i in range(0,len(colors[0])):
        mat = makeMaterial(meshname+str(i)+'_'+str(plot_index), 
                           (colors[0][i],colors[1][i],colors[2][i]), 
                           (1,1,1), alpha, emisses[i])
        setMaterial(obj,mat)
    # now, do individual mat indecies
    for i in range(0,len(newfaces)):
        me.polygons[i].material_index = colorindex[i]




def import_ytsurface(filename, isosurface_value = 1e-27, surf_type='sphere', radius = 10.0, 
                     radius_units = "mpc", surface_field="density",  
                     meshname = 'Allen',  
                     transparency = 1.0, dist_fac = None,
                     color_field = None, emit_field = None, color_map = "algae", 
                     color_log = True, emit_log = True, plot_index = None, 
                     color_field_max = None, color_field_min = None, 
                     emit_field_max = None, emit_field_min = None, emissivity_units = None,
                     force_override = False):
    
    from yt import load, add_field
    import yt
    import numpy as np

    emit_field_name = None
    if emit_field is not None:
        if emissivity_units is None:
            emissivity_units = "g**2*K**0.5/cm**6"
            #emissivity_units = 'auto'
        # check if we have a function or a string for the return in a function
        emit_function = emit_field
        if isinstance(emit_field,str): # if w are inputting a string from the gui
            def _Emissivity(field, data):
                import numpy as np
                return (eval("data['gas','density']*data['gas','density']*np.sqrt(data['gas','temperature'])"))
            emit_function = _Emissivity
            emit_field_name = ('gas','emissivity') # so far only emissivity for gas...
    
    pf = yt.load(filename)
    if emit_field is not None:
        pf.add_field(("gas","emissivity"), units="g**2*K**0.5/cm**6", function=_Emissivity, force_override=True)
    
    # for only 1 value
    if isinstance(isosurface_value, float):
        isosurface_value = [isosurface_value]
        transparency = [transparency]
        plot_index = 0
    #if surf_type is 'sphere':
    #    presurf = pf.sphere("max", (radius, radius_units)) 
    #else:
    #    print("Waaaahhoooo, don't know anything else!  Am doing spherical surface for the time being")
    #    presurf = pf.sphere("max", (radius, radius_units)) 
    for i in range(0,len(isosurface_value)):
        
        
        trans = transparency[i]
#        dd = pf.h.sphere("max", (radius, radius_units))
#        surf = pf.h.surface(dd, surface_field, isosurface_value[i])
        dd = pf.sphere("max", (radius, radius_units))
        surf = pf.surface(dd, surface_field, isosurface_value[i])
        #surf = pf.surface(presurf, surface_field, isosurface_value[i])
        m_name = meshname + '_' + str(i)
        vertices, colors, alpha, emisses, colorindex = surf.export_blender(transparency = trans, dist_fac = dist_fac,
                                                                           color_field = color_field, emit_field = emit_field_name, color_map = color_map, 
                                                                           color_log = color_log, emit_log = emit_log, plot_index = i, 
                                                                           color_field_max = color_field_max, color_field_min = color_field_min, 
                                                                           emit_field_max = emit_field_max, emit_field_min = emit_field_min)


        
        #emit_field_name = ('gas','emissivity')
        #emit_field_max = None
        #emit_field_min = None
        #color_field_max = None
        #color_field_min = None
        #color_map = "algae"

        #vertices, colors, alpha, emisses, colorindex = surf.export_blender(transparency = trans, 
        #                                                                   color_field = color_field, emit_field = emit_field_name, color_map = color_map, 
        #                                                                   plot_index = 0, 
        #                                                                   color_field_max = color_field_max, color_field_min = color_field_min, 
        #                                                                   emit_field_max = emit_field_max, emit_field_min = emit_field_min)


        
        _import_ytsurface(vertices, colors, alpha, emisses, colorindex, m_name, (0,0,0), i)
    return pf






        

def import_ytsurface_old():
    import yt
    import numpy as np

    # different data - FLASH
    filename = '~/data/GasSloshing/sloshing_nomag2_hdf5_plt_cnt_0100'
    sphere_rad = 15.0 # in kpc

    #Enzo
    filename = '~/data/IsolatedGalaxy/galaxy0030/galaxy0030'
    sphere_rad = 200.0 # in kpc


    outfile = 'galsurfaces'

    rho = 1e-27 # for each surface
    trans = 1.0 # for transparency of each surface

    color_field = 'temperature' # color your surface by this
    def _Emissivity(field, data):
        import numpy as np
        return (eval("data['gas','density']*data['gas','density']*np.sqrt(data['gas','temperature'])"))
    #yt.add_field("emissivity", units="g**2*K**0.5/cm**6", function=_Emissivity, force_override=True)
    pf = yt.load(filename)
    pf.add_field(("gas","emissivity"), units="g**2*K**0.5/cm**6", function=_Emissivity, force_override=True)


    # emissivity of the material

    # for testing
    print(_Emissivity)
    print(pf)
    print(filename)
    
    #pf.add_field("emissivity", units="auto", function=_Emissivity, force_override=True)

    
    yt.SlicePlot(pf, 'z', ("gas","emissivity"), width = (200.0, 'kpc')).save('~/Desktop/mytest_blender.png')
    #yt.SlicePlot(pf, 'z', ("gas","density"), width = (200.0, 'kpc')).save('~/Desktop/mytest_blender.png')

    dd = pf.sphere("max", (sphere_rad, "kpc"))

    surf = pf.surface(dd, 'density', rho)
    #surf.export_obj(outfile, transparency = trans, 
    #                color_field=color_field, emit_field = 'emissivity')

    emit_field_name = ('gas','emissivity')
#    emit_field_name = ('gas','density')
    emit_field_max = None
    emit_field_min = None
    color_field_max = None
    color_field_min = None
    color_map = "algae"
    #m_name = "steve"

    vertices, colors, alpha, emisses, colorindex = surf.export_blender(transparency = trans, 
                                                                       color_field = color_field, emit_field = emit_field_name, color_map = color_map, 
                                                                       plot_index = 0, 
                                                                       color_field_max = color_field_max, color_field_min = color_field_min, 
                                                                       emit_field_max = emit_field_max, emit_field_min = emit_field_min)

    print(vertices)

    #_import_ytsurface(vertices, colors, alpha, emisses, colorindex, m_name, (0,0,0), i)

    return pf
