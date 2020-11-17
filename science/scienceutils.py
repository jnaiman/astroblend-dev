import bpy



############ MATERIAL/TEXTURE FUNCTIONS #######################


# The following function is adapted from
# Nick Keeline "Cloud Generator" addNewObject
# from object_cloud_gen.py (an addon that comes with the Blender 2.6 package)

# these are if you wanna change the colors or transparencies on the fly
def makeMaterial(name, diffuse, specular, alpha, emiss, mat_type=None, halo_size=None):
    mat = bpy.data.materials.new(name)
    mat.emit = emiss # emissivity is up to 2.0!
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha  # sets transparency (0.0 = invisable)
    mat.use_transparency = True # assumes Z-transparency
#    mat.ambient = 1use  # can't have for transparency
    if mat_type is not None:
        mat.type = mat_type
    if halo_size is not None:
        mat.halo.size = halo_size
    return mat
 

# set a material on an object
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
    

# to delete unused materials from things when deleting the object
def delete_unused_materials(name):
    bpy.context.scene.objects.active=bpy.data.objects[name]
    obj = bpy.context.object
    while obj.data.materials:
        # note, in 2.69 .pop() on its own works
        obj.data.materials.pop(0, update_data=True)
        obj.data.materials.clear()
    for mat in bpy.data.materials:
        if (mat.name.find(name) != -1):
            mat.user_clear()
            bpy.data.materials.remove(mat)
            del(mat)
    # delete material slots too
    #for i in range(0,len(bpy.data.objects[name].material_slots)):
    for i in range(1,len(obj.material_slots)):
        #if len(bpy.data.objects[name].material_slots) > 0:
        #bpy.context.object.active_material_index = i
        bpy.context.object.active_material_index = 1
        bpy.ops.object.material_slot_remove()


# delete associated textures from an object
def delete_unused_textures(name):
    for tex in bpy.data.textures:
        if (tex.name.find(name) != -1):
            tex.user_clear()
            bpy.data.textures.remove(tex)
            del(tex)


# change the color of the text or mesh
def set_object_color(name, color = None, shadeless = None):
    if shadeless is None:
        shadeless = True
    if color is None:
        color = (0,0,0.)
    # now, set color
    # first, remove other materials
    deselect_all()
    bpy.data.objects[name].select = True
    delete_unused_materials(name)
    textmat = makeMaterial(name, color, (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
    setMaterial(bpy.data.objects[name], textmat)
    # also, make shadeless
    if shadeless:
        bpy.data.materials[name].use_shadeless = True

# make 2 meshes into one mesh
def join_surfaces(name_list):
    deselect_all()
    # join objects
    bpy.context.scene.objects.active = bpy.data.objects[name_list[0]]
    for i in range(0,len(name_list)):
        bpy.data.objects[name_list[i]].select = True
    bpy.ops.object.join()


###################################################################

############################## FIGURES #############################
#  to come...

# delete associated images from an object
def delete_unused_images(name):
    for img in bpy.data.images:
        if (img.name.find(name) != -1):
            img.user_clear()
            bpy.data.images.remove(img)
            del(img)
        

#######################################################################

##################### MISC HELPER FUNCTIONS ##########################


# delete a mesh from an obj file
def delete_object(name_or_object, scene_name='Scene'):
    # decide if we are deleting by name or by object
    if isinstance(name_or_object,str):
        name = name_or_object
        unhide_object(name)
        deselect_all() 
        bpy.data.objects[name].select = True
        bpy.context.scene.objects.active=bpy.data.objects[name]
        emptyFlag = True
        if (bpy.data.objects[name].type == 'EMPTY'):
            emptyFlag = False
        if (bpy.data.objects[name].type != 'LAMP') and (bpy.data.objects[name].type != 'EMPTY'):
            # delete assosiated materials first
            delete_unused_materials(name)
            # delete associated textures
            delete_unused_textures(name)
        # now, delete object
        # have to do it this way to actually remove it from memeroy
        me = bpy.data.objects[name].data
        scene = bpy.data.scenes[scene_name]
        scene.objects.unlink(bpy.data.objects[name])
        if (bpy.data.objects[name].type != 'LAMP') and (bpy.data.objects[name].type != 'EMPTY'):
            me.user_clear()
            bpy.data.meshes.remove(me)
            bpy.data.objects.remove(bpy.data.objects[name])
        # also, delete empty, if there is one
        deselect_all()
        if (emptyFlag):
            for obj in bpy.data.objects:
                if ((obj.name.find(name) != -1) and (obj.name.find('Empty') != -1)):
                    bpy.data.objects['Empty'+name].select=True
                    bpy.context.scene.objects.active=bpy.data.objects['Empty'+name]
                    bpy.ops.object.delete()            
        #else:
            #bpy.ops.object.delete()            
            #bpy.data.objects.remove(bpy.data.objects[name])
        # also, delete empty of text center, if there is one
        deselect_all()
        for obj in bpy.data.objects:
            if ((obj.name.find(name) != -1) and (obj.name.find('CenterOf:') != -1)):
                bpy.data.objects['CenterOf:'+name].select=True
                bpy.context.scene.objects.active=bpy.data.objects['CenterOf:'+name]
                bpy.ops.object.delete()
    elif (not isinstance(name_or_object, str)) and isinstance(name_or_object.name,str): # not an array
        name = name_or_object.name
        unhide_object(name)
        deselect_all() 
        bpy.data.objects[name].select = True
        bpy.context.scene.objects.active=bpy.data.objects[name]
        emptyFlag = True
        if (bpy.data.objects[name].type == 'EMPTY'):
            emptyFlag = False
        if (bpy.data.objects[name].type != 'LAMP') and (bpy.data.objects[name].type != 'EMPTY'):
        #    # delete assosiated materials first
            delete_unused_materials(name)
        #    # delete associated textures
            delete_unused_textures(name)
        # now, delete object
        # have to do it this way to actually remove it from memeroy
        me = bpy.data.objects[name].data
        scene = bpy.data.scenes[scene_name]
        scene.objects.unlink(bpy.data.objects[name])
        if (bpy.data.objects[name].type != 'LAMP') and (bpy.data.objects[name].type != 'EMPTY'):
            me.user_clear()
            from simpleobjects import Text as txtchk
            if isinstance(name_or_object,txtchk) is False:
                bpy.data.meshes.remove(me)
            bpy.data.objects.remove(bpy.data.objects[name])
        # also, delete empty, if there is one
        deselect_all()
        if (emptyFlag):
            for obj in bpy.data.objects:
                if ((obj.name.find(name) != -1) and (obj.name.find('Empty') != -1)):
                    bpy.data.objects['Empty'+name].select=True
                    bpy.context.scene.objects.active=bpy.data.objects['Empty'+name]
                    bpy.ops.object.delete()
        #else:
        #    bpy.data.objects.remove(bpy.data.objects[name])
        # also, delete empty of text center, if there is one
        deselect_all()
        for obj in bpy.data.objects:
            if ((obj.name.find(name) != -1) and (obj.name.find('CenterOf:') != -1)):
                bpy.data.objects['CenterOf:'+name].select=True
                bpy.context.scene.objects.active=bpy.data.objects['CenterOf:'+name]
                bpy.ops.object.delete()
        # delete reference to object
        del(name_or_object)
  
    else:
        for name in name_or_object.name:
            #print("YO!!!")
            unhide_object(name)
            deselect_all() 
            bpy.data.objects[name].select = True
            bpy.context.scene.objects.active=bpy.data.objects[name]
            if bpy.data.objects[name].type != 'LAMP':
                # delete assosiated materials first
                delete_unused_materials(name)
                # delete associated textures
                delete_unused_textures(name)
            # now, delete object
            # have to do it this way to actually remove it from memeroy
            me = bpy.data.objects[name].data
            scene = bpy.data.scenes[scene_name]
            scene.objects.unlink(bpy.data.objects[name])
            me.user_clear()
            if bpy.data.objects[name].type != 'LAMP':
                bpy.data.meshes.remove(me)
                bpy.data.objects.remove(bpy.data.objects[name])
            # also, delete empty, if there is one
            deselect_all()
            for obj in bpy.data.objects:
                if ((obj.name.find(name) != -1) and (obj.name.find('Empty') != -1)):
                    bpy.data.objects['Empty'+name].select=True
                    bpy.context.scene.objects.active=bpy.data.objects['Empty'+name]
                    bpy.ops.object.delete()
            # also, delete empty of text center, if there is one
            deselect_all()
            for obj in bpy.data.objects:
                if ((obj.name.find(name) != -1) and (obj.name.find('CenterOf:') != -1)):
                    bpy.data.objects['CenterOf:'+name].select=True
                    bpy.context.scene.objects.active=bpy.data.objects['CenterOf:'+name]
                    bpy.ops.object.delete()
        # delete reference to object
        del(name_or_object)
  

# deselect all the things
def deselect_all():
    scene = bpy.context.scene
    for ob in scene.objects:
        ob.select = False


def hide_object(name,hide_render=True):
# hide an object in both 3D viewer and render
    bpy.data.objects[name].hide = True
    bpy.data.objects[name].hide_render = hide_render


def unhide_object(name):
# hide an object in both 3D viewer and render
    bpy.data.objects[name].hide = False
    bpy.data.objects[name].hide_render = False



