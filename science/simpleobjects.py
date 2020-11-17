import bpy
from scienceutils import deselect_all, join_surfaces, delete_unused_materials, makeMaterial, \
    setMaterial


class Text(object):
    def __init__(self, name = "NoName", color=(1.,1,1), scale=(1.,1,1), shadeless=True): 
        newtxt = name
        xyzloc = (0,0,0)
        self.__name = 'Text'
        emptyname = 'Empty' + self.__name # what to call empty for facing
        emptycenter = 'CenterOf:' + self.__name # where the actual tracking will be  
        # add a new empty in the center of this text
        bpy.ops.object.empty_add(type='SPHERE') # add object to track to
        esphc = bpy.data.objects['Empty']
        esphc.name = emptycenter
        esphc.location = [xyzloc[0], xyzloc[1], xyzloc[2]] # give it an offset
        bpy.ops.object.empty_add(type='SPHERE') # add object to track to
        esph = bpy.data.objects['Empty']
        esph.name = emptyname
        esph.location = [xyzloc[0], xyzloc[1], xyzloc[2]+5] # give it an offset
        # now, fix this this empty to the middle of the text
        deselect_all()
        bpy.ops.object.text_add(location=xyzloc) # make text
        bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
        bpy.ops.font.delete() # delete what is there
        bpy.ops.font.text_insert(text=newtxt) # insert new text
        bpy.ops.object.mode_set(mode='OBJECT')  # toggle to edit object mode
        self.name = name
        emptyname = 'Empty' + self.name # what to call empty for facing
        emptycenter = 'CenterOf:' + self.name # where the actual tracking will be  
        bpy.data.objects[self.name].scale = scale # scale new txt object
        txtsize = bpy.data.objects[self.name].dimensions # now, recenter this thing
        bpy.data.objects[self.name].location = (xyzloc[0] - txtsize[0]*0.5, 
                                                xyzloc[0] - txtsize[1]*0.5, 
                                                xyzloc[0] - txtsize[2]*0.5)
        tobj = bpy.data.objects[self.name]
        bpy.context.scene.objects.active = tobj # this is a key step to "highlight" esphc
        tobj.select = True
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.data.objects[self.name].constraints["Child Of"].target = esphc
        # now, link new text Center to an empty that we can move around
        esphc.rotation_mode = 'QUATERNION' #  mo betta then 'XYZ'
        deselect_all()
        bpy.context.scene.objects.active = esphc # this is a key step to "highlight" esphc
        # auto track to the new empty
        esphc.select = True
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.data.objects[emptycenter].constraints["Track To"].target = esph
        # now, set correct coords
        esphc.constraints["Track To"].track_axis = 'TRACK_Z'
        esphc.constraints["Track To"].up_axis = 'UP_Y'
        esphc.hide = True # hide this from the viewport
        self.color = color
        self.location = (0,0,0)
        self.pointing = (0,0,5)
        self.shadeless = shadeless
        self.scale = scale

    @property
    def name(self):
        self.__name = bpy.data.objects[self.__name].name
        return self.__name

    @name.setter
    def name(self,name):
        deselect_all()
        location_old = [0,0,0]
        location_old[0] = bpy.data.objects['CenterOf:'+self.__name].location[0]
        location_old[1] = bpy.data.objects['CenterOf:'+self.__name].location[1]
        location_old[2] = bpy.data.objects['CenterOf:'+self.__name].location[2]
        pointing_old = [0,0,0]
        pointing_old[0] = self.pointing[0]
        pointing_old[1] = self.pointing[1]
        pointing_old[2] = self.pointing[2]
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.ops.object.mode_set(mode='EDIT')  # toggle to edit mode
        bpy.ops.font.delete() # delete what is there
        bpy.ops.font.text_insert(text=name) # insert new text
        bpy.ops.object.mode_set(mode='OBJECT')  # toggle to edit object mode
        # now, recenter over center
        bpy.data.objects['CenterOf:'+self.__name].location = (0,0,0)
        bpy.data.objects['Empty'+self.__name].location = (0,0,5)
        txtsize = bpy.data.objects[self.__name].dimensions # now, recenter this thing
        bpy.data.objects[self.__name].location = (-0.5*txtsize[0], -0.5*txtsize[1],-0.5*txtsize[2])
        bpy.data.objects['CenterOf:'+self.__name].location = location_old
        bpy.data.objects['Empty'+self.__name].location = pointing_old
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects['Empty'+self.__name].name = 'Empty' + name
        bpy.data.objects['CenterOf:'+self.__name].name = 'CenterOf:' + name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name

    @property
    def color(self):
        self.__color = bpy.data.materials[self.name].specular_color
        return self.__color

    @color.setter
    def color(self,color): 
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        delete_unused_materials(self.name)
        sphmat = makeMaterial(self.name, color, (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
        setMaterial(bpy.data.objects[self.name], sphmat)
        self.__color = color

    @property
    def shadeless(self):
        self.__shadeless = bpy.data.materials[self.name].use_shadeless
        return self.__shadeless

    @shadeless.setter
    def shadeless(self,shadeless):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.name) != -1):
            if mat.name == self.__name:
                mat.use_shadeless = shadeless
        self.__shadeless = shadeless

    @property
    def scale(self):
        self.__scale = bpy.data.objects[self.name].scale
        return self.__scale

    @scale.setter
    def scale(self,scale):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.objects[self.name].scale = scale
        self.__scale = scale

    @property
    def location(self):
        self.__location = bpy.data.objects['CenterOf:'+self.name].location
        return self.__location

    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects['CenterOf:'+self.name]
        bpy.data.objects['CenterOf:'+self.name].location = location
        self.__location = location

    @property
    def pointing(self):
        self.__pointing = bpy.data.objects['Empty'+self.name].location
        return self.__pointing

    @pointing.setter
    def pointing(self,pointing):
        bpy.context.scene.objects.active = bpy.data.objects['Empty'+self.name]
        bpy.data.objects['Empty' + self.name].location = pointing
        self.__pointing = pointing

#    def delete(self):
#        # also, delete empty
#        deselect_all()
#        bpy.data.objects['Empty'+self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects['Empty'+self.name]
#        bpy.ops.object.delete()
#        # also, delete empty center
#        deselect_all()
#        bpy.data.objects['CenterOf:'+self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects['CenterOf:'+self.name]
#        bpy.ops.object.delete()
#        self.name = self.name
#        deselect_all() 
#        bpy.data.objects[self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects[self.name]
#        # delete assosiated materials first
#        delete_unused_materials(self.name)
#        # now, delete object
#        bpy.ops.object.delete()


class Arrow(object):

    # add an arrow
    def __init__(self, name="NoNameArrow", color = (1,1,1), scale=(0.5,0.5,0.5),  shadeless = True, 
                 tip_scale = 2.0, base_scale = 1.0):
        deselect_all()
        self.__name = 'Cylinder'
        # create arrow
        # now, make ability to point
        emptyname = 'Empty' + self.__name # what to call empty
        xyzloc = (0,0,0)
        bpy.ops.object.empty_add(type='SPHERE') # add object to track to
        esph = bpy.data.objects['Empty']
        esph.name = emptyname
        esph.location = [xyzloc[0], xyzloc[1], xyzloc[2]+5] # give it an offset
        bpy.ops.mesh.primitive_cone_add()
        bpy.ops.mesh.primitive_cylinder_add()
        cone = bpy.data.objects['Cone']
        arrow = bpy.data.objects['Cylinder']
        cone.location = (0,0,base_scale*scale[2]+scale[2]*tip_scale)
        arrow.location = (0,0,0)
        arrow.scale = (scale[0]*base_scale, scale[1]*base_scale, scale[2]*base_scale)  
        cone.scale = (tip_scale*scale[0], tip_scale*scale[1], tip_scale*scale[2])
        join_surfaces(['Cylinder','Cone'])
        arrow.rotation_mode = 'QUATERNION' #  mo betta then 'XYZ'
        self.name = name
        # auto track to the new empty
        deselect_all()
        bpy.context.scene.objects.active = bpy.data.objects[self.name] # this is a key step to "highlight" the arrow
        # auto track to the new empty
        bpy.data.objects[self.name].select = True
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.data.objects[self.name].constraints["Track To"].target = esph
        # now, set correct coords
        ddir = 'TRACK_Z'
        updir = 'UP_X'
        bpy.data.objects[self.name].constraints["Track To"].track_axis = ddir
        bpy.data.objects[self.name].constraints["Track To"].up_axis = updir
        # now, set color
        self.color = color
        self.shadeless = shadeless
        self.scale = scale
        self.pointing = (0,0,5)
        self.location = (0,0,0)

    @property
    def name(self):
        self.__name = bpy.data.objects[self.__name].name
        return self.__name

    @name.setter
    def name(self,name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects['Empty'+self.__name].name = 'Empty' + name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name

    @property
    def color(self):
        self.__color = bpy.data.materials[self.name].specular_color
        return self.__color

    @color.setter
    def color(self,color): 
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        delete_unused_materials(self.name)
        sphmat = makeMaterial(self.name, color, (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
        setMaterial(bpy.data.objects[self.name], sphmat)
        self.__color = color

    @property
    def shadeless(self):
        self.__shadeless = bpy.data.materials[self.name].use_shadeless
        return self.__shadeless

    @shadeless.setter
    def shadeless(self,shadeless):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.name) != -1):
            if mat.name == self.__name:
                mat.use_shadeless = shadeless
        self.__shadeless = shadeless

    @property
    def scale(self):
        self.__scale = bpy.data.objects[self.name].scale
        return self.__scale

    @scale.setter
    def scale(self,scale):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.objects[self.name].scale = scale
        self.__scale = scale

    @property
    def location(self):
        self.__location = bpy.data.objects[self.name].location
        return self.__location

    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects[self.name]
        bpy.data.objects[self.name].location = location
        self.__location = location

    @property
    def pointing(self):
        self.__pointing = bpy.data.objects['Empty'+self.name].location
        return self.__pointing

    @pointing.setter
    def pointing(self,pointing):
        bpy.context.scene.objects.active = bpy.data.objects['Empty'+self.name]
        bpy.data.objects['Empty' + self.name].location = pointing
        self.__pointing = pointing

#   # delete arrow ... can probably put into delete_obj_mesh
#    def delete(self):
#        deselect_all() 
#        # also, delete empty
#        deselect_all()
#        bpy.data.objects['Empty'+self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects['Empty'+self.name]
#        bpy.ops.object.delete()
#        bpy.data.objects[self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects[self.name]
#        # delete assosiated materials first
#        delete_unused_materials(self.name)
#        # now, delete object
#        bpy.ops.object.delete()


class Sphere(object):

    # add a sphere
    def __init__(self, name="NoNameSphere", color = (1,1,1), scale=(1,1,1), segments = 32, shadeless = True):
        deselect_all()
        bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, size=1.0)
        sph = bpy.data.objects['Sphere']
        self.__name = 'Sphere'
        self.name = name
        self.color = color
        self.shadeless = shadeless
        self.scale = scale
        self.location = (0,0,0)

    @property
    def name(self):
        self.__name = bpy.data.objects[self.__name].name
        return self.__name

    @name.setter
    def name(self,name):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.name = name # change materials name
        bpy.data.objects[self.__name].name = name # object name
        self.__name = name

    @property
    def color(self):
        self.__color = bpy.data.materials[self.__name].specular_color
        return self.__color

    @color.setter
    def color(self,color): 
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        delete_unused_materials(self.__name)
        sphmat = makeMaterial(self.__name, color, (1,1,1), 1.0, 0.0) # no emissivity or transperency for now
        setMaterial(bpy.data.objects[self.__name], sphmat)
        self.__color = color

    @property
    def shadeless(self):
        self.__shadeless = bpy.data.materials[self.__name].use_shadeless
        return self.__shadeless

    @shadeless.setter
    def shadeless(self,shadeless):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        for mat in bpy.data.materials:
            #if (mat.name.find(self.__name) != -1):
            if mat.name == self.__name:
                mat.use_shadeless = shadeless
        self.__shadeless = shadeless

    @property
    def scale(self):
        self.__scale = bpy.data.objects[self.__name].scale
        return self.__scale

    @scale.setter
    def scale(self,scale):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].scale = scale
        self.__scale = scale

    @property
    def location(self):
        self.__location = bpy.data.objects[self.__name].location
        return self.__location

    @location.setter
    def location(self,location):
        bpy.context.scene.objects.active = bpy.data.objects[self.__name]
        bpy.data.objects[self.__name].location = location
        self.__location = location

#    # delete sphere ... can probably put into delete_obj_mesh
#    def delete(self):
#        deselect_all() 
#        bpy.data.objects[self.name].select = True
#        bpy.context.scene.objects.active=bpy.data.objects[self.name]
#        # delete assosiated materials first
#        delete_unused_materials(self.name)
#        # now, delete object
#        bpy.ops.object.delete()
