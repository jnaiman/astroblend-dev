# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
import bpy
from bpy.types import Menu, Panel, UIList, Brush, ParticleSettings
#from bl_ui.properties_grease_pencil_common import GreasePencilPanel
from bl_ui.properties_paint_common import (
        UnifiedPaintPanel,
        brush_texture_settings,
        brush_texpaint_common,
        brush_mask_texture_settings,
        )

# do I even need this class??
class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

from bpy_extras.io_utils import (ImportHelper,
                                 ExportHelper,
                                 orientation_helper_factory,
                                 path_reference_mode,
                                 axis_conversion,
                                 )

    

# JPN - below

# default units
default_viewer_units = "kpc"
default_viewer_unitsScale = "1e2"
# generate color table list for selection
import pylab as pl
#for full list use this:
#color_maps = [ m for m in pl.cm.datad]
# for slightly smaller list us this:
#color_maps = [ m for m in pl.cm.datad if (not m.startswith("idl")) & (not m.endswith("_r"))]
# only native yt ones:
from yt.visualization import _colormap_data as _cm
color_maps = [ m for m in _cm.color_map_luts if (not m.startswith("idl")) & (not m.endswith("_r"))]

# now generate color map items
color_map_items = []
for i in range(0,len(color_maps)):
    color_map_items.append( (color_maps[i], color_maps[i], color_maps[i]) )



from bpy.props import *


def initSceneProperties(scn):
   
    #bpy.types.Scene.NewABFile = StringProperty(
    #    name = "File(s)")
    #scn['NewABFile'] = "File(s) Location"
    # just 1 file at a time now
    bpy.types.Scene.NewABFile = StringProperty(
        name = "File")
    scn['NewABFile'] = "File Location"

    bpy.types.Scene.yt_object_name = StringProperty(
        name = "ytObject Name")
    scn['yt_object_name'] = "Steve"

#    bpy.types.Scene.ObjectScale = FloatProperty(
#        name = "ObjectScale")
#    scn['ObjectScale'] = (1.0, 1.0, 1.0)
    bpy.types.Scene.PointCloudNameTag = StringProperty(
        name = "PointCloudNameTag")
    scn['PointCloudNameTag'] = "Steve"

# for viewer stuff
    bpy.types.Scene.ViewerUnits = StringProperty(
        name = "Units")
    scn['ViewerUnits'] = default_viewer_units
    
    bpy.types.Scene.ViewerUnitsScale = StringProperty(
        name = "Units Scale")
    scn['ViewerUnitsScale'] = default_viewer_unitsScale

    
# isocontour stuff
    bpy.types.Scene.isocontourName = StringProperty(
        name = "Name")
    scn['isocontourName'] = "MyContour"

    bpy.types.Scene.isocontourUnits = StringProperty(
        name = "Units")
    scn['isocontourUnits'] = "kpc"
    
    bpy.types.Scene.isocontourValue = StringProperty(
        name = "Isocontour Value", 
        description = "Enter a float",
        default = '1e-24')#,
#        min = 1e-30,
#        max = 1e30)

    bpy.types.Scene.isocontourColorMap = StringProperty(
        name = "Color Map", 
        description = "Enter a color map",
        default = 'algae')#,

    bpy.types.Scene.isocontourColorMap = EnumProperty(
        items = color_map_items,
        name = "Color Map")
    scn['isocontourColorMap'] = 'algae'
    

    bpy.types.Scene.isocontourSphere = FloatProperty(
        name = "Sphere Size", 
        description = "Sphere Size",
        default = 200.00,
        min = 1e-30,
        max = 1e30)

    bpy.types.Scene.isocontourAlpha = FloatProperty(
        name = "Alpha", 
        description = "Transparency",
        default = 1.0,
        min = 0.0,
        max = 1.0)
    
    bpy.types.Scene.isocontourVariableType = StringProperty(
        name = "Variable Type")
    scn['isocontourVariableType'] = "gas"

    
    bpy.types.Scene.isocontourVariable = StringProperty(
        name = "Variable")
    scn['isocontourVariable'] = "density"

    bpy.types.Scene.isocontourColorType = StringProperty(
        name = "Color by Type")
    scn['isocontourColorType'] = "gas"

    bpy.types.Scene.isocontourColor = StringProperty(
        name = "Color by")
    scn['isocontourColor'] = "temperature"

    bpy.types.Scene.isocontourEmissivity = StringProperty(
        name = "Emissivity")
    scn['isocontourEmissivity'] = "None"

    bpy.types.Scene.isocontourEmissivityOn = BoolProperty(
        name = "Emissivity on?")
    scn['isocontourEmissivityOn'] = False
    

# pointcloud stuff
    bpy.types.Scene.pointCloudName = StringProperty(
        name = "Name")
    scn['pointCloudName'] = "MyPointCloud"
    
    bpy.types.Scene.pointCloudHaloSize = FloatProperty(
        name = "Halo Size", 
        description = "Enter a float",
        default = 0.0008)
    
    bpy.types.Scene.pointCloudColor = StringProperty(
        name = "Color by")
    scn['pointCloudColor'] = "Temperature"

    bpy.types.Scene.pointCloudColorMap = EnumProperty(
        items = color_map_items,
        name = "Color Map")
    scn['pointCloudColorMap'] = "algae"

    
    bpy.types.Scene.pointCloudColorParticle = StringProperty(
        name = "Particle Type")
    scn['pointCloudColorParticle'] = "Gas"    
    
    bpy.types.Scene.pointCloudColorLog = BoolProperty(
        name = "Log(color)?", 
        description = "True or False?")
    scn['pointCloudColorLog'] = True

    bpy.types.Scene.pointCloudnref = IntProperty(
        name = "n_ref")
    scn['pointCloudnref'] = 8

    

# for SlicePlot
    bpy.types.Scene.sliceUnits = StringProperty(
        name = "Units")
    scn['sliceUnits'] = "kpc"

    #bpy.types.Scene.sliceAxis = StringProperty(
    #    name = "Axis")
    #scn['sliceAxis'] = "z"

    bpy.types.Scene.sliceAxis = EnumProperty(
        items = [('z', 'z', 'One'), 
                 ('y', 'y', 'Two'),
                 ('x', 'x', 'Three'),
                 ('off-axis', 'off-axis', 'Four')],
        name = "Axis")
    scn['SliceAxis'] = 2

    bpy.types.Scene.sliceVariableType = StringProperty(
        name = "Variable Type")
    scn['sliceVariableType'] = "gas"
    
    bpy.types.Scene.sliceVariable = StringProperty(
        name = "Variable")
    scn['sliceVariable'] = "density"

    bpy.types.Scene.sliceName = StringProperty(
        name = "Fig Name")
    scn['sliceName'] = "MySlice"

    bpy.types.Scene.sliceObjectName = StringProperty(
        name = "Fig Obj Name")
    scn['sliceObjectName'] = "MySlice"

#    bpy.types.Scene.sliceObjectColorMap = StringProperty(
#        name = "Color Map")
#    scn['Color Map'] = "MySlice"
    bpy.types.Scene.sliceColorMap = EnumProperty(
        items = color_map_items,
        name = "Color Map")
    scn['sliceColorMap'] = "algae"
    
    
    bpy.types.Scene.sliceLinkObjName = StringProperty(
        name = "Link Obj Name")
    scn['sliceLinkObjName'] = ""

    bpy.types.Scene.sliceWidth = FloatProperty(
        name = "Width", 
        description = "Width",
        default = 20.0)

    bpy.types.Scene.sliceShowAnnotation = BoolProperty(
        name = "Annotation?", 
        description = "True or False?")
    scn['sliceShowAnnotation'] = True
    

# for ProjectionPlot
    bpy.types.Scene.projectionUnits = StringProperty(
        name = "Units")
    scn['projectionUnits'] = "kpc"

    bpy.types.Scene.projectionAxis = EnumProperty(
        items = [('z', 'z', 'One'), 
                 ('y', 'y', 'Two'),
                 ('x', 'x', 'Three'),
                 ('off-axis', 'off-axis', 'Four')],
        name = "Axis")
    scn['projectionAxis'] = 'z'

    bpy.types.Scene.projectionVariableType = StringProperty(
        name = "Variable Type")
    scn['projectionVariableType'] = "gas"
    
    
    bpy.types.Scene.projectionVariable = StringProperty(
        name = "Variable")
    scn['projectionVariable'] = "temperature"

    bpy.types.Scene.projectionWeightVariableType = StringProperty(
        name = "Weight Variable Type")
    scn['projectionWeightVariableType'] = "gas"

    bpy.types.Scene.projectionColorMap = EnumProperty(
        items = color_map_items,
        name = "Color Map")
    scn['projectionColorMap'] = "algae"
    
    bpy.types.Scene.projectionWeightVariable = StringProperty(
        name = "Weight Variable")
    scn['projectionWeightVariable'] = "density"

#    bpy.types.Scene.projectionName = StringProperty(
#        name = "Fig Name")
#    scn['projectionName'] = "MyProjection"

    bpy.types.Scene.projectionObjectName = StringProperty(
        name = "Fig Obj Name")
    scn['projectionObjectName'] = "MyProjection"

    bpy.types.Scene.projectionLinkObjName = StringProperty(
        name = "Link Obj Name")
    scn['projectionLinkObjName'] = ""

    bpy.types.Scene.projectionWidth = FloatProperty(
        name = "Width", 
        description = "Width",
        default = 20.0)
    
    bpy.types.Scene.projectionShowAnnotation = BoolProperty(
        name = "Annotation?", 
        description = "True or False?")
    scn['projectionShowAnnotation'] = True


# for PhasePlot
    bpy.types.Scene.phaseUnits = StringProperty(
        name = "Units")
    scn['phaseUnits'] = "kpc"

    bpy.types.Scene.phaseVariableTypeX = StringProperty(
        name = "X Variable Type")
    scn['phaseVariableTypeX'] = "gas"
    bpy.types.Scene.phaseVariableTypeY = StringProperty(
        name = "Y Variable Type")
    scn['phaseVariableTypeY'] = "gas"
    bpy.types.Scene.phaseVariableTypeZ = StringProperty(
        name = "Z Variable Type")
    scn['phaseVariableTypeZ'] = "gas"

    
    bpy.types.Scene.phaseVariableX = StringProperty(
        name = "X Variable")
    scn['phaseVariableX'] = "density"
    bpy.types.Scene.phaseVariableY = StringProperty(
        name = "Y Variable")
    scn['phaseVariableY'] = "temperature"
    bpy.types.Scene.phaseVariableZ = StringProperty(
        name = "Z Variable")
    scn['phaseVariableZ'] = "cell_mass"

    bpy.types.Scene.phaseWeightType = StringProperty(
        name = "Weight Variable Type")
    scn['phaseWeightType'] = "gas"
    bpy.types.Scene.phaseWeight = StringProperty(
        name = "Weight Variable")
    scn['phaseWeight'] = "None"

    
    bpy.types.Scene.phaseName = StringProperty(
        name = "Fig Name")
    scn['phaseName'] = "MyPhasePlot"

    bpy.types.Scene.phaseColorMap = EnumProperty(
        items = color_map_items,
        name = "Color Map")
    scn['phaseColorMap'] = "algae"
    
    bpy.types.Scene.phaseLinkObjName = StringProperty(
        name = "Link Obj Name")
    scn['phaseLinkObjName'] = ""

    bpy.types.Scene.phaseWidth = FloatProperty(
        name = "Width", 
        description = "Width",
        default = 200.0)
    
    bpy.types.Scene.phaseWireFrameSphere = BoolProperty(
        name = "Wireframe?", 
        description = "True or False?")
    scn['phaseWireFrameSphere'] = True


    
    
# grid stuff
    bpy.types.Scene.gridName = StringProperty(
        name = "Grid Obj Name")
    scn['gridName'] = "MyGrid"



# hack for not displaying the preview stuff
    bpy.types.Scene.HackTexture = BoolProperty(
        name = "Turn off and off tex hack for voxel data", 
        description = "True or False?")
    scn['HackTexture'] = False

    
    return
 
initSceneProperties(bpy.context.scene)

# ------- try to overwrite this -------------
from bl_ui.properties_material import active_node_mat

def context_tex_datablock(context):
    idblock = context.material
    if idblock:
        return active_node_mat(idblock)

    idblock = context.lamp
    if idblock:
        return idblock

    idblock = context.world
    if idblock:
        return idblock

    idblock = context.brush
    if idblock:
        return idblock

    idblock = context.line_style
    if idblock:
        return idblock

    if context.particle_system:
        idblock = context.particle_system.settings

    return idblock


class TextureButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "texture"

    @classmethod
    def poll(cls, context):
        tex = context.texture
        return tex and (tex.type != 'NONE' or tex.use_nodes) and (context.scene.render.engine in cls.COMPAT_ENGINES)


class TEXTURE_PT_preview(TextureButtonsPanel, Panel):
    bl_label = "Preview"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_GAME'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture
        slot = getattr(context, "texture_slot", None)
        idblock = context_tex_datablock(context)

        if not context.scene.HackTexture: 
            if idblock:
                layout.template_preview(tex, parent=idblock, slot=slot)
            else:
                layout.template_preview(tex, slot=slot)

        #Show Alpha Button for Brush Textures, see #29502
        if context.space_data.texture_context == 'BRUSH':
            layout.prop(tex, "use_preview_alpha")


class TEXTURE_PT_context_texture(TextureButtonsPanel, Panel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_GAME'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        # if not (hasattr(context, "texture_slot") or hasattr(context, "texture_node")):
        #     return False
        return ((context.material or
                 context.world or
                 context.lamp or
                 context.texture or
                 context.line_style or
                 context.particle_system or
                 isinstance(context.space_data.pin_id, ParticleSettings) or
                 context.texture_user) and
                (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout

        slot = getattr(context, "texture_slot", None)
        node = getattr(context, "texture_node", None)
        space = context.space_data
        tex = context.texture
        idblock = context_tex_datablock(context)
        pin_id = space.pin_id

        space.use_limited_texture_context = True

        if space.use_pin_id and not isinstance(pin_id, Texture):
            idblock = id_tex_datablock(pin_id)
            pin_id = None

        if not space.use_pin_id:
            layout.prop(space, "texture_context", expand=True)
            pin_id = None

        if space.texture_context == 'OTHER':
            if not pin_id:
                layout.template_texture_user()
            user = context.texture_user
            if user or pin_id:
                layout.separator()

                row = layout.row()

                if pin_id:
                    row.template_ID(space, "pin_id")
                else:
                    propname = context.texture_user_property.identifier
                    row.template_ID(user, propname, new="texture.new")

                if tex:
                    split = layout.split(percentage=0.2)
                    if tex.use_nodes:
                        if slot:
                            split.label(text="Output:")
                            split.prop(slot, "output_node", text="")
                    else:
                        split.label(text="Type:")
                        split.prop(tex, "type", text="")
            return

        tex_collection = (pin_id is None) and (node is None) and (not isinstance(idblock, Brush))

        if tex_collection:
            row = layout.row()

            if not context.scene.HackTexture:
                row.template_list("TEXTURE_UL_texslots", "", idblock, "texture_slots", idblock, "active_texture_index", rows=2)

            col = row.column(align=True)
            col.operator("texture.slot_move", text="", icon='TRIA_UP').type = 'UP'
            col.operator("texture.slot_move", text="", icon='TRIA_DOWN').type = 'DOWN'
            col.menu("TEXTURE_MT_specials", icon='DOWNARROW_HLT', text="")

        if tex_collection:
            layout.template_ID(idblock, "active_texture", new="texture.new")
        elif node:
            layout.template_ID(node, "texture", new="texture.new")
        elif idblock:
            layout.template_ID(idblock, "texture", new="texture.new")

        if pin_id:
            layout.template_ID(space, "pin_id")

        if tex:
            split = layout.split(percentage=0.2)
            if tex.use_nodes:
                if slot:
                    split.label(text="Output:")
                    split.prop(slot, "output_node", text="")
            else:
                split.label(text="Type:")
                split.prop(tex, "type", text="")

            
# ----------- stop over writing -----------------------

#filename = "/Users/jillnaiman1/astroblend-dev/science/full3dpanel274.py"
#exec(compile(open(filename).read(), filename, 'exec'))


# AstroBlend utilities
class VIEW3D_PT_tools_ABObjects_objects(View3DPanel, Panel):
    bl_category = "AB Objects"
    #bl_context = "objectmode"
    bl_label = "Load File"
    #bl_options = {'DEFAULT_ACTIVE'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column(align=True)
        layout.operator("abload_file.button", text="Open a Sim file", icon='FILE_FOLDER')

class VIEW3D_PT_tools_ABObjects_viewoptions(View3DPanel, Panel):
    bl_category = "AB Objects"
    #bl_context = "objectmode"
    bl_label = "Viewer Options"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column(align=True)
        layout.prop(scn, 'ViewerUnits')
        layout.prop(scn, 'ViewerUnitsScale')
        layout.operator("ytviewscale.button", text="Rescale Domain")
        col = layout.column(align=True)
        view = context.space_data
        sub = col.column(align=True)
        sub.prop(view, "grid_lines", text="Lines")
        #sub.prop(view, "grid_scale", text="Scale")
        subsub = sub.column(align=True)
        subsub.prop(view, "grid_subdivisions", text="Subdivisions")

# button to print & display field list
class YTVIEWSCALE_OT_Button(bpy.types.Operator):
    bl_idname = "ytviewscale.button"
    bl_label = "Button"

    def execute(self, context):
        scn = context.scene
        # rescale the grid by the new coords
        new_units = scn['ViewerUnits']
        new_scale = float(scn['ViewerUnitsScale'])
        old_units = default_viewer_units
        old_scale = float(default_viewer_unitsScale)
        
        from yt import units
        v = vars(units)
        #vv = dir(units)
        gs = v[new_units]/v[old_units]*new_scale/old_scale
        # now rescale
        for a in bpy.context.screen.areas:
            if a.type == 'VIEW_3D':
                a.spaces[0].grid_scale = gs
        
            


        return{'FINISHED'}    


        

# to load in a datafile
IOOBJOrientationHelper = orientation_helper_factory("IOOBJOrientationHelper", axis_forward='-Z', axis_up='Y')
class ImportYTData(bpy.types.Operator, ImportHelper, IOOBJOrientationHelper):
    """Load  a data File"""
    bl_idname = "abload_file.button"
    bl_label = "Import Data"
    bl_options = {'PRESET', 'UNDO'}

    filter_glob = StringProperty(
            default="*",
            options={'HIDDEN'},
            )

    def execute(self, context):
        from science import Load as LD
    
        # not quite sure why we need this....
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "filter_glob",
                                            "split_mode",
                                            ))
        if bpy.data.is_saved and context.user_preferences.filepaths.use_relative_paths:
            import os
            keywords["relpath"] = os.path.dirname((bpy.data.path_resolve("filepath", False).as_bytes()))

        context.scene.NewABFile = keywords["filepath"]

        myobject = LD(context.scene.NewABFile)#, context.scene.yt_object_name)
        obj = bpy.context.active_object
        obj['ABFile'] = context.scene.NewABFile
        scn = context.scene
        from yt import units
        v = vars(units)        
        # now, we are going to rescale things to the over all scale of the box
        #boxscalings = [(myobject.ds.domain_right_edge.in_units(scn['ViewerUnits'])-myobject.ds.domain_left_edge.in_units(scn['ViewerUnits']))]
        #bs = boxscalings[0]
        bs = myobject.ds.domain_width.in_units(scn['ViewerUnits'])*0.5
        bc = myobject.ds.domain_center.in_units(scn['ViewerUnits'])
        #print(myobject.ds.domain_right_edge.in_units(scn['ViewerUnits']))
        #maxsc = max(boxscalings[0])
        new_units = scn['ViewerUnits']
        new_scale = float(scn['ViewerUnitsScale'])
        myobject.scale = [( bs[0]/(v[new_units]*new_scale), bs[1]/(v[new_units]*new_scale), bs[2]/(v[new_units]*new_scale) )]
        myobject.location = [( bc[0]/(v[new_units]*new_scale), bc[1]/(v[new_units]*new_scale), bc[2]/(v[new_units]*new_scale) )]
        
        return{'FINISHED'}    


    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        box = layout.box()
        row = box.row()
        row = box.row()
        row = layout.split(percentage=0.67)


 

# AstroBlend functions
class VIEW3D_PT_tools_ABOBJECTS_obprops(View3DPanel, Panel):
    bl_category = "AB Objects"
    bl_context = "objectmode"
    bl_label = "Domain Properties"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene

        obj = context.active_object
        if obj:
            col = layout.column(align=True)
            #col.label(text="OBJECT PROPERTIES:")
            obj = context.active_object
            layout.prop(obj, 'name')
            layout.prop(obj, 'scale')
            layout.prop(obj, 'location')
            layout.operator("ds_fieldlist.button", text="Field List")
            layout.operator("ds_derivedfieldlist.button", text="Derived Field List")



# button to print & display field list
class DSFieldlist_OT_Button(bpy.types.Operator):
    bl_idname = "ds_fieldlist.button"
    bl_label = "Button"

    def execute(self, context):
        from yt import load
        # check out if the isosurface exists, and if so, delete before regeneration
        not_a_domain = False

        # this check doesn't work for some reason...
        #try:
        #    context.active_object['ABFile']
        #except NameError:
        #    not_a_domain = True
        #print(not_a_domain)

        if not not_a_domain:
            filename = context.active_object['ABFile']
            ds = load(filename)
            ds.index
            print('FIELD LIST')
            for field in ds.field_list:
                print(field)
        else:
            print("Are you sure this is a domain object?")
        
        return{'FINISHED'}    


    
# button to print & display derived field list
class DSDerivedFieldlist_OT_Button(bpy.types.Operator):
    bl_idname = "ds_derivedfieldlist.button"
    bl_label = "Button"

    def execute(self, context):
        from yt import load
        # check out if the isosurface exists, and if so, delete before regeneration
        filename = context.active_object['ABFile']
        ds = load(filename)
        ds.index
        print('DERIVED FIELD LIST')
        for field in ds.derived_field_list:
            print(field)
        
        return{'FINISHED'}    
    
            

# pointcloud the panel
class VIEW3D_PT_tools_ABPlots_pointcloud(View3DPanel, Panel):
    bl_category = "AB Objects"
    bl_context = "objectmode"
    bl_label = "Point Cloud"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene

        obj = context.active_object
        if obj:
            col = layout.column(align=True)
            layout.prop(scn, 'pointCloudName')
            layout.prop(scn, 'pointCloudHaloSize')
            layout.prop(scn, 'pointCloudColor')
            layout.prop(scn, 'pointCloudColorParticle')
            layout.prop(scn, 'pointCloudColorLog')
            layout.prop(scn, 'pointCloudnref')
            layout.prop(scn, 'pointCloudColorMap')
            layout.operator("pointcloud.button", text="Generate Point Cloud")
            layout.operator("deletepointcloud.button", text="Delete Point Cloud")

            

#   AB pointcloud Button
class POINTCLOUD_OT_Button(bpy.types.Operator):
    bl_idname = "pointcloud.button"
    bl_label = "Button"

    def execute(self, context):
        domain_name = context.scene.objects.active.name
        from science import Lighting, overall_scale #, objects, Load
        from science import Load as LD
        from scienceutils import delete_object, deselect_all
        scn = context.scene
        # check out if the isosurface exists, and if so, delete before regeneration
        filename = context.active_object['ABFile']
        halo_sizes = context.scene.pointCloudHaloSize
        color_field = (context.scene.pointCloudColorParticle,context.scene.pointCloudColor)
        color_log = context.scene.pointCloudColorLog
        n_ref = context.scene.pointCloudnref
        namein = context.scene.pointCloudName
#        color_map = "algae"
        color_map = context.scene.pointCloudColorMap
#        for obj in bpy.data.objects:
#            if obj.name == context.scene.pointCloudName:
#                delete_object(context.active_object.name) # JPN - needs to input scene name
#        names_list = bpy.data.objects[scn['PointCloudNameTag']]['ABGroupName']
#        for n in names_list:
#            delete_object(n)

        Lighting('EMISSION') # make emissivity lighting
        myobject = LD(filename, halo_sizes=[halo_sizes], color_field=color_field,
                      color_map=color_map, color_log=color_log,
                      n_ref=n_ref)
        # this tags the last group with the ABFile and Group Name... not sure if we need to do this
        obj = bpy.context.active_object
        obj['ABFile'] = filename
        obj['ABGroupName'] = myobject.name
        scn['PointCloudNameTag'] = obj.name

        from yt import units
        v = vars(units)        
        # now, we are going to rescale things to the over all scale of the box
        #boxscalings = [(myobject.ds.domain_right_edge.in_units(scn['ViewerUnits'])-myobject.ds.domain_left_edge.in_units(scn['ViewerUnits']))]
        #bs = boxscalings[0]
        bs = myobject.ds.domain_width.in_units(scn['ViewerUnits'])*0.5
        bc = myobject.ds.domain_center.in_units(scn['ViewerUnits'])

        new_units = scn['ViewerUnits']
        new_scale = float(scn['ViewerUnitsScale'])
        myobject.scale = [( bs[0]/(v[new_units]*new_scale), bs[1]/(v[new_units]*new_scale), bs[2]/(v[new_units]*new_scale) )]
        myobject.location = [( bc[0]/(v[new_units]*new_scale), bc[1]/(v[new_units]*new_scale), bc[2]/(v[new_units]*new_scale) )] # I think we want to do this

        #bpy.ops.object.constraint_add(type='COPY_LOCATION')
        #names_list = bpy.data.objects[scn['PointCloudNameTag']]['ABGroupName']
        #for n in names_list:
        #    deselect_all()
        #    bpy.data.objects[n].select = True
        #    bpy.context.scene.objects.active = bpy.data.objects[n]
        #    bpy.ops.object.constraint_add(type='COPY_LOCATION')
        #    bpy.data.objects[n].constraints["Copy Location"].target = bpy.data.objects[domain_name]
        #    bpy.ops.object.constraint_add(type='COPY_SCALE')
        #    bpy.data.objects[n].constraints["Copy Scale"].target = bpy.data.objects[domain_name]

        return{'FINISHED'}    


#   AB pointcloud Button
class POINTCLOUD_OT_Button_delete(bpy.types.Operator):
    bl_idname = "deletepointcloud.button"
    bl_label = "Button"

    def execute(self, context):
        from scienceutils import delete_object
        # get the name
        scn = context.scene
        names_list = bpy.data.objects[scn['PointCloudNameTag']]['ABGroupName']
        for n in names_list:
            delete_object(n)
        return{'FINISHED'}    
            

class VIEW3D_PT_tools_ABPlots_isocontour(View3DPanel, Panel):
    bl_category = "AB Objects"
    bl_context = "objectmode"
    bl_label = "IsoContours"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene

        obj = context.active_object
        if obj:
            col = layout.column(align=True)
            layout.prop(scn, 'isocontourName')
            layout.prop(scn, 'isocontourSphere')
            layout.prop(scn, 'isocontourUnits')
            layout.prop(scn, 'isocontourVariableType')
            layout.prop(scn, 'isocontourVariable')
            layout.prop(scn, 'isocontourValue')
            layout.prop(scn, 'isocontourColorType')
            layout.prop(scn, 'isocontourColor')
            layout.prop(scn, 'isocontourColorMap')
            layout.prop(scn, 'isocontourEmissivity')

            if scn['isocontourEmissivity'] != "None":
                layout.prop(scn, 'isocontourEmissivityOn')
                
            layout.prop(scn, 'isocontourAlpha')
            layout.operator("isocontour.button", text="Generate Contour")
            layout.operator("deleteisocontour.button", text="Delete Contour")

#   AB pointcloud Button
class ISOCONTOUR_OT_Button_delete(bpy.types.Operator):
    bl_idname = "deleteisocontour.button"
    bl_label = "Button"

    def execute(self, context):
        from scienceutils import delete_object
        # get the name
        scn = context.scene
        delete_object(bpy.data.objects[scn['isocontourName'] + '_0'])
        return{'FINISHED'}    
            
            
#   AB isosurface Button
class ISOCONTOUR_OT_Button(bpy.types.Operator):
    bl_idname = "isocontour.button"
    bl_label = "Button"

    def execute(self, context):
        domain_name = context.scene.objects.active.name
#        from science import objects
        from science import overall_scale
        from scienceutils import delete_object
        from science import Load as LD
        # check out if the isosurface excists, and if so, delete before regeneration
        filename = context.scene.NewABFile
        #print("FNAME")
        #print(context.scene.NewABFile)
        print(context.scene['NewABFile'])
#        isosurface_value = context.scene.isocontourValue
        isosurface_value = float(context.scene.isocontourValue)
        radius = context.scene.isocontourSphere
        radius_units = context.scene.isocontourUnits 
        surface_field = context.scene.isocontourVariable
        surface_field_type = context.scene.isocontourVariableType
        color_field = context.scene.isocontourColor
        color_field_type = context.scene.isocontourColorType
        trans = context.scene.isocontourAlpha
        #namein = context.active_object.name
        namein = context.scene.isocontourName
        dist_fac = None
        emit_field = None
#        color_map = "algae"
        color_map = context.scene.isocontourColorMap
        color_log = True
        emit_log = True
        plot_index = None
        color_field_max = None
        color_field_min = None
        emit_field_max = None
        emit_field_min = None
        #emissivity_units = None

        # if we have a defined emit field, then generate that
        if context.scene.isocontourEmissivity == "None":
            emiss_in = None
        else:
            emiss_in = context.scene.isocontourEmissivity
            from science import Lighting
            if context.scene.isocontourEmissivityOn:
                Lighting('EMISSION') # make emissivity lighting
            else:
                Lighting('SUN')

        # delete old objects
        for obj in bpy.data.objects:
            if obj.name == context.scene.isocontourName + '_0':
                delete_object(context.active_object.name) # JPN - needs to input scene name
                
        myobject = LD(filename, scale = (1., 1.0, 1.0), isosurface_value = isosurface_value, 
                      surf_type='sphere', radius = radius, 
                      radius_units = radius_units, surface_field=(surface_field_type,surface_field), 
                      meshname = namein, transparency = trans, 
                      color_field=(color_field_type,color_field), color_map = color_map,
                      emit_field=emiss_in, force_override=True) 
        #myobject = LD()
        #from science import objects
        #print("right here")
        #ds = objects.import_ytsurface()
        #print("after right here")
        #print(ds)
        obj = bpy.context.active_object
        obj['ABFile'] = filename
        obj.location = myobject.ds.domain_center.in_units('unitary')*overall_scale # CHANGE THIS FOR RIGHT LOCATION!!!

        from yt import units
        v = vars(units)
        scn = context.scene
        # now, we are going to rescale things to the over all scale of the box
        #boxscalings = [(myobject.ds.domain_right_edge.in_units(scn['ViewerUnits'])-myobject.ds.domain_left_edge.in_units(scn['ViewerUnits']))]
        #bs = boxscalings[0]
        bs = myobject.ds.domain_width.in_units(scn['ViewerUnits'])*0.5
        bc = myobject.ds.domain_center.in_units(scn['ViewerUnits']) #this one we will be re-centering... for now, we want off - center isos too
        new_units = scn['ViewerUnits']
        new_scale = float(scn['ViewerUnitsScale'])
        myobject.scale = [( bs[0]/(v[new_units]*new_scale), bs[1]/(v[new_units]*new_scale), bs[2]/(v[new_units]*new_scale) )]
        myobject.location = [( bc[0]/(v[new_units]*new_scale), bc[1]/(v[new_units]*new_scale), bc[2]/(v[new_units]*new_scale) )]



        # now, we are going to rescale things to the over all scale of the box
        #boxscalings = [(myobject.ds.domain_right_edge-myobject.ds.domain_left_edge)]
        #maxsc = max(boxscalings[0])
        #myobject.scale = [(overall_scale/maxsc,overall_scale/maxsc,overall_scale/maxsc)]
        # finally, have it such that the object is tracked to the domain -> if the domain changes so does the plot
        #bpy.ops.object.constraint_add(type='COPY_LOCATION')
        #bpy.data.objects[scn.isocontourName].constraints["Copy Location"].target = bpy.data.objects[domain_name]
        #bpy.ops.object.constraint_add(type='COPY_SCALE')
        #bpy.data.objects[scn.isocontourName].constraints["Copy Scale"].target = bpy.data.objects[domain_name]

        return{'FINISHED'}    
            

# grid the panel
class VIEW3D_PT_tools_ABPlots_grid(View3DPanel, Panel):
    bl_category = "AB Objects"
    bl_context = "objectmode"
    bl_label = "Grid"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene

        obj = context.active_object

        # also, allow for grid thickness if grid excists
        for obj in bpy.data.objects:
            if obj.name == scn.gridName:
                layout.prop(obj.modifiers['Wireframe'], 'thickness')

        if obj:
            col = layout.column(align=True)
            layout.prop(scn, 'gridName')
            layout.operator("grid.button", text="Generate Grid")
            layout.operator("deletegrid.button", text="Delete Grid")


#   AB grid Button
class GRID_OT_Button_delete(bpy.types.Operator):
    bl_idname = "deletegrid.button"
    bl_label = "Button"

    def execute(self, context):
        from scienceutils import delete_object
        # get the name
        scn = context.scene
        delete_object(bpy.data.objects[scn['gridName']])
        return{'FINISHED'}    

                

#   AB grid Button
class GRID_OT_Button(bpy.types.Operator):
    bl_idname = "grid.button"
    bl_label = "Button"

    def execute(self, context):
        domain_name = context.scene.objects.active.name
        from yt import load
        from scienceutils import delete_object
        from science import objects
        # check out if the grid excists, and if so, delete before regeneration
        filename = context.scene.NewABFile
        thickness = 0.001
        gridName = context.scene.gridName
        for obj in bpy.data.objects:
            if obj.name == context.scene.gridName:
                delete_object(context.active_object.name) # JPN - needs to input scene name
        ds = load(filename)
        obj = bpy.context.active_object
        obj['ABFile'] = filename
        objects.ytGrid(ds, grid_name = context.scene.gridName, center=None, scale=[1., 1., 1.])
        # finally, have it such that the object is tracked to the domain -> if the domain changes so does the plot
        #bpy.ops.object.constraint_add(type='COPY_LOCATION')
        #bpy.data.objects[scn.gridName].constraints["Copy Location"].target = bpy.data.objects[domain_name]
        #bpy.ops.object.constraint_add(type='COPY_SCALE')
        #bpy.data.objects[scn.gridName].constraints["Copy Scale"].target = bpy.data.objects[domain_name]

        from yt import units
        scn = context.scene
        v = vars(units)
        obj = bpy.context.active_object # now grid is active
        # now, we are going to rescale things to the over all scale of the box
        #boxscalings = [(ds.domain_right_edge.in_units(scn['ViewerUnits'])-ds.domain_left_edge.in_units(scn['ViewerUnits']))]
        #print(boxscalings)
        #print(len(boxscalings))
        #bs = boxscalings[0]
        #else:
        #    bs = boxscalings
        bs = ds.domain_width.in_units(scn['ViewerUnits'])*0.5
        bc = ds.domain_center.in_units(scn['ViewerUnits'])
        new_units = scn['ViewerUnits']
        new_scale = float(scn['ViewerUnitsScale'])
        print(( bs[0]/(v[new_units]*new_scale), bs[1]/(v[new_units]*new_scale), bs[2]/(v[new_units]*new_scale) ))
        print(obj)
        obj.scale = ( bs[0]/(v[new_units]*new_scale), bs[1]/(v[new_units]*new_scale), bs[2]/(v[new_units]*new_scale) )
        obj.location = ( bc[0]/(v[new_units]*new_scale), bc[1]/(v[new_units]*new_scale), bc[2]/(v[new_units]*new_scale) )


        
        return{'FINISHED'}    

                

# slice plots
class VIEW3D_PT_tools_ABPlots_sliceplots(View3DPanel, Panel):
    bl_category = "AB Plots"
    bl_context = "objectmode"
    bl_label = "Slice Plots"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene

        col = layout.column(align=True)
        layout.prop(scn, 'sliceLinkObjName')
        layout.prop(scn, 'sliceObjectName')
        layout.prop(scn, 'sliceUnits')
        layout.prop(scn, 'sliceWidth')
        layout.prop(scn, 'sliceVariableType')
        layout.prop(scn, 'sliceVariable')
        layout.prop(scn, 'sliceColorMap')
        layout.prop(scn, 'sliceShowAnnotation')
        layout.prop(scn, 'sliceAxis')


        #obj = context.active_object
        #obj = bpy.data.objects[scn.sliceObjectName]
        for obj in bpy.data.objects:
            if obj:
                if obj.name == scn.sliceObjectName:
                    col = layout.column(align=True)
                    #col.label(text="Center:")
                    row = col.row(align=True)
                    layout.prop(obj, 'location')
                    
                    # if using off-axis, then allow for a normal
                    if scn.sliceAxis == 'off-axis':
                        #col.label(text="Normal:")
                        row = col.row(align=True)
                        for obj in bpy.data.objects:
                            if obj.name == 'Empty'+scn.sliceObjectName:
                                layout.prop(obj, 'location', text = 'Normal')

        col = layout.column(align=True)
        layout.operator("slice.button", text="Generate Slice")
        layout.operator("deleteslice.button", text="Delete Slice")
                                

#   AB slice delete Button
class SLICE_OT_Button_delete(bpy.types.Operator):
    bl_idname = "deleteslice.button"
    bl_label = "Button"

    def execute(self, context):
        from scienceutils import delete_object
        # get the name
        scn = context.scene
        delete_object(bpy.data.objects[scn['sliceName']])
        return{'FINISHED'}    

                                

#   AB slice Button
class SLICE_OT_Button(bpy.types.Operator):
    bl_idname = "slice.button"
    bl_label = "Button"

    def execute(self, context):
        emptysize = 0.005 # this should change with domain size - JPN
        emptylocation = 0.25 # this should change with domain size - JPN
        from yt import load
        from science import plots, deselect_all, delete_object
        from numpy import zeros
        scn = context.scene
        flagg = True
        domain_name = context.scene.objects.active.name
        from science import overall_scale
        from yt import units
        new_units = scn['ViewerUnits']
        new_scale = float(scn['ViewerUnitsScale'])
        v = vars(units)        
        fac = overall_scale
        fac *= v[scn.sliceUnits]/(v[new_units]*new_scale)

        
        for ob in bpy.data.objects: # if we have a plan, activate it
            if ob.name == scn.sliceObjectName:
                context.scene.objects.active = bpy.data.objects[scn.sliceObjectName]
                flagg = False
        if flagg: # else, create it
            bpy.ops.mesh.primitive_plane_add(radius=1.0) 
            context.active_object.name = scn.sliceObjectName
            # move to location of domain
            bpy.data.objects[scn.sliceObjectName].location = bpy.data.objects[scn.sliceLinkObjName].location
            # rescale
            bpy.data.objects[scn.sliceObjectName].scale = bpy.data.objects[scn.sliceLinkObjName].scale

        tobj = bpy.data.objects[scn.sliceObjectName]
        tobj.rotation_mode = 'QUATERNION' #  mo betta then 'XYZ'

        # for off axis projections
        if scn.sliceAxis == 'off-axis':
            # loop through and see if we have the correct empty
            flagg = True
            for ob in bpy.data.objects:
                if ob.name == 'Empty'+scn.sliceObjectName:
                    flagg = False
            if flagg: # if we don't have an empty, create it!
                bpy.ops.object.empty_add(type='SPHERE') # add object to track to
                #bpy.ops.object.empty_add(type='SINGLE_ARROW') # add object to track to
                esph = context.scene.objects.active
                esph.name = 'Empty' + scn.sliceObjectName
                esph.scale = (emptysize, emptysize, emptysize) # make it small ish
                esph.location = bpy.data.objects[scn.sliceObjectName].location
                #esph.location[2] = (esph.location[2] + emptylocation)/fac # give it an offset
                ### HACK
                esph.location[2] = 10.0
                deselect_all()
                # auto track to the new empty
                tobj.select = True
                esph.select = True
                bpy.ops.object.track_set(type='TRACKTO')
                # now, set correct coords
                bpy.data.objects[scn.sliceObjectName].constraints['AutoTrack'].track_axis = 'TRACK_NEGATIVE_Z'
                bpy.data.objects[scn.sliceObjectName].constraints['AutoTrack'].up_axis = 'UP_X'
                deselect_all()
                # make it rotate with the rotation of the figure
                
                
                context.scene.objects.active = tobj
        else: # we are doing x/y/z slices, so delete an empty if its there
            for ob in bpy.data.objects:
                if ob.name == 'Empty'+scn.sliceObjectName:
                    delete_object(ob.name) # JPN - need to add correct scene info
                    context.scene.objects.active = bpy.data.objects[scn.sliceObjectName]
                    # remove all constraints
                    for c in bpy.data.objects[scn.sliceObjectName].constraints:
                        bpy.data.objects[scn.sliceObjectName].constraints.remove(c)
            if scn.sliceAxis == 'z':
                tobj.rotation_quaternion = (1,0,0,0)
            elif scn.sliceAxis == 'y':
                tobj.rotation_quaternion = (1,1,0,0)
            elif scn.sliceAxis == 'x':
                tobj.rotation_quaternion = (1,0,1,0)

        myf = bpy.data.objects[scn.sliceLinkObjName]['ABFile']
        ds = load(myf)

        # to get things facing correctly, we need to rotate around local z
        

        # now, we are going to rescale things to the over all scale of the box
        #boxscalings = [(ds.domain_right_edge.in_units(scn['ViewerUnits'])-ds.domain_left_edge.in_units(scn['ViewerUnits']))]
        #bs = boxscalings[0]
        bs = ds.domain_width.in_units(scn['ViewerUnits'])*0.5
        bpy.data.objects[scn.sliceObjectName].scale = (scn.sliceWidth*fac,scn.sliceWidth*fac,scn.sliceWidth*fac)
        
        # now, derive the locations of the projections from this plane
        slcCenter = zeros(3)
        # example filename: /Users/jillnaiman1/data/IsolatedGalaxy/galaxy0030/galaxy0030
        for i in range(0,3): #need to recenter if object has moved
            #slcCenter[i] = bpy.data.objects[domain_name].location[i]*bs[i]/(v[new_units]*new_scale)
            slcCenter[i] = bpy.data.objects[domain_name].location[i]*(v[new_units]*new_scale)/(bs[i]*2.)

        if scn.sliceAxis != 'off-axis':
            plots.ytSlicePlot(ds, image_name=scn.sliceObjectName, axis=scn.sliceAxis,
                              variable=(scn.sliceVariableType,scn.sliceVariable),
                              center=[slcCenter[0],slcCenter[1],slcCenter[2]],
                              width=scn.sliceWidth, units = scn.sliceUnits, color_map = scn.sliceColorMap,
                              show_annotations = scn.sliceShowAnnotation)
        else:
            normalx = bpy.data.objects['Empty'+scn.sliceObjectName].location[0] - bpy.data.objects[scn.sliceObjectName].location[0]
            normaly = bpy.data.objects['Empty'+scn.sliceObjectName].location[1] - bpy.data.objects[scn.sliceObjectName].location[1]
            normalz = bpy.data.objects['Empty'+scn.sliceObjectName].location[2] - bpy.data.objects[scn.sliceObjectName].location[2]
            plots.ytSlicePlot(ds, image_name=scn.sliceObjectName, axis=[normalx,normaly,normalz],
                              variable=(scn.sliceVariableType,scn.sliceVariable),
                              center=[slcCenter[0],slcCenter[1],slcCenter[2]],
                              width=scn.sliceWidth, units = scn.sliceUnits, color_map = scn.sliceColorMap,
                              show_annotations = scn.sliceShowAnnotation)



        # finally, have it such that the slice plot is tracked to the domain -> if the domain changes so does the plot
        #bpy.ops.object.constraint_add(type='COPY_LOCATION')
        #bpy.data.objects[scn.sliceObjectName].constraints["Copy Location"].target = bpy.data.objects[domain_name]
        #bpy.ops.object.constraint_add(type='COPY_SCALE')
        #bpy.data.objects[scn.sliceObjectName].constraints["Copy Scale"].target = bpy.data.objects[domain_name]
        
        return{'FINISHED'}    
    


# projection plots
class VIEW3D_PT_tools_ABPlots_projectionplots(View3DPanel, Panel):
    bl_category = "AB Plots"
    bl_context = "objectmode"
    bl_label = "Projection Plots"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene

        col = layout.column(align=True)
        layout.prop(scn, 'projectionLinkObjName')
        layout.prop(scn, 'projectionObjectName')
        layout.prop(scn, 'projectionUnits')
        layout.prop(scn, 'projectionWidth')
        layout.prop(scn, 'projectionVariableType')
        layout.prop(scn, 'projectionVariable')
        layout.prop(scn, 'projectionColorMap')
        layout.prop(scn, 'projectionWeightVariableType')
        layout.prop(scn, 'projectionWeightVariable')
        layout.prop(scn, 'projectionShowAnnotation')
        layout.prop(scn, 'projectionAxis')

        for obj in bpy.data.objects:
            if obj:
                if obj.name == scn.projectionObjectName:
                    col = layout.column(align=True)
                    #col.label(text="Center:")
                    row = col.row(align=True)
                    layout.prop(obj, 'location')

                    # if using off-axis, then allow for a normal
                    if scn.projectionAxis == 'off-axis':
                        #col.label(text="Normal:")
                        row = col.row(align=True)
                        for obj in bpy.data.objects:
                            if obj.name == 'Empty'+scn.projectionObjectName:
                                layout.prop(obj, 'location', text = 'Normal')

        col = layout.column(align=True)
        layout.operator("projection.button", text="Generate Projection")
        layout.operator("deleteprojection.button", text="Delete Projection")

                                
#   AB slice delete Button
class PROJECTION_OT_Button_delete(bpy.types.Operator):
    bl_idname = "deleteprojection.button"
    bl_label = "Button"

    def execute(self, context):
        from scienceutils import delete_object
        # get the name
        scn = context.scene
        delete_object(bpy.data.objects[scn['projectionObjectName']])
        return{'FINISHED'}    

 
                                

#   AB isosurface Button
class PROJECTION_OT_Button(bpy.types.Operator):
    bl_idname = "projection.button"
    bl_label = "Button"

    def execute(self, context):
        emptysize = 0.05 # this should change with domain size - JPN
        emptylocation = 0.25 # this should change with domain size - JPN
        from yt import load
        from science import plots, deselect_all, delete_object, overall_scale
        from numpy import zeros
        scn = context.scene
        flagg = True
        # first off, save the name of the domain box that is active
        domain_name = context.scene.objects.active.name
        for ob in bpy.data.objects: # if we have a plane, activate it
            if ob.name == scn.projectionObjectName:
                context.scene.objects.active = bpy.data.objects[scn.projectionObjectName]
                flagg = False
        if flagg: # else, create it
            bpy.ops.mesh.primitive_plane_add(radius=1.0) 
            context.active_object.name = scn.projectionObjectName
            # move to location of domain
            bpy.data.objects[scn.projectionObjectName].location = bpy.data.objects[scn.projectionLinkObjName].location
            # rescale
            bpy.data.objects[scn.projectionObjectName].scale = bpy.data.objects[scn.projectionLinkObjName].scale

        tobj = bpy.data.objects[scn.projectionObjectName]
        tobj.rotation_mode = 'QUATERNION' #  mo betta then 'XYZ'

        # for off axis projections
        if scn.projectionAxis == 'off-axis':
            # loop through and see if we have the correct empty
            flagg = True
            for ob in bpy.data.objects:
                if ob.name == 'Empty'+scn.projectionObjectName:
                    flagg = False
            if flagg: # if we don't have an empty, create it!
                bpy.ops.object.empty_add(type='SPHERE') # add object to track to
                esph = context.scene.objects.active
                esph.name = 'Empty' + scn.projectionObjectName
                esph.scale = (emptysize, emptysize, emptysize) # make it small ish
                esph.location = bpy.data.objects[scn.projectionObjectName].location
                esph.location[2] = esph.location[2] + emptylocation # give it an offset
                deselect_all()
                # auto track to the new empty
                tobj.select = True
                esph.select = True
                bpy.ops.object.track_set(type='TRACKTO')
                # now, set correct coords
                bpy.data.objects[scn.projectionObjectName].constraints['AutoTrack'].track_axis = 'TRACK_NEGATIVE_Z'
                bpy.data.objects[scn.projectionObjectName].constraints['AutoTrack'].up_axis = 'UP_X'
                deselect_all()
                context.scene.objects.active = tobj
        else: # we are doing x/y/z projections, so delete an empty if its there
            for ob in bpy.data.objects:
                if ob.name == 'Empty'+scn.projectionObjectName:
                    delete_object(ob.name) # JPN - need to add correct scene info
                    context.scene.objects.active = bpy.data.objects[scn.projectionObjectName]
                    # remove all constraints
                    for c in bpy.data.objects[scn.projectionObjectName].constraints:
                        bpy.data.objects[scn.projectionObjectName].constraints.remove(c)
            if scn.projectionAxis == 'z':
                tobj.rotation_quaternion = (1,0,0,0)
            elif scn.projectionAxis == 'y':
                tobj.rotation_quaternion = (1,1,0,0)
            elif scn.projectionAxis == 'x':
                tobj.rotation_quaternion = (1,0,1,0)

                
        myf = bpy.data.objects[scn.projectionLinkObjName]['ABFile']
        ds = load(myf)

        # rescale plane to width
        #fac = (ds.domain_width.in_units('unitary')[0]).value/(ds.domain_width.in_units(scn.projectionUnits)[0]).value
        fac = overall_scale

        from yt import units
        v = vars(units)        
        # now, we are going to rescale things to the over all scale of the box
        #boxscalings = [(ds.domain_right_edge.in_units(scn['ViewerUnits'])-ds.domain_left_edge.in_units(scn['ViewerUnits']))]
        #bs = boxscalings[0]
        bs = ds.domain_width.in_units(scn['ViewerUnits'])*0.5
        new_units = scn['ViewerUnits']
        new_scale = float(scn['ViewerUnitsScale'])
        fac *= v[scn.projectionUnits]/(v[new_units]*new_scale)
        bpy.data.objects[scn.projectionObjectName].scale = (scn.projectionWidth*fac,scn.projectionWidth*fac,scn.projectionWidth*fac)
        
        # now, derive the locations of the projections from this plane
        slcCenter = zeros(3)
        # example filename: /Users/jillnaiman1/data/IsolatedGalaxy/galaxy0030/galaxy0030
        for i in range(0,3): #need to recenter if object has moved
            #slcCenter[i] = bpy.data.objects[domain_name].location[i]*bs[i]/(v[new_units]*new_scale)
            slcCenter[i] = bpy.data.objects[domain_name].location[i]*(v[new_units]*new_scale)/(bs[i]*2.)
        print(slcCenter)
        print(scn.projectionWidth)
        print(bs)
        #slcCenter = (0.5, 0.5, 0.5)
        if scn.projectionAxis != 'off-axis':
            plots.ytProjectionPlot(ds, image_name=scn.projectionObjectName, axis=scn.projectionAxis,
                                   variable=(scn.projectionVariableType,scn.projectionVariable),
                                   weight_variable = (scn.projectionWeightVariableType,scn.projectionWeightVariable),
                                   center=[slcCenter[0],slcCenter[1],slcCenter[2]],
                                   width=scn.projectionWidth, units = scn.projectionUnits, color_map = scn.projectionColorMap,
                                   show_annotations = scn.projectionShowAnnotation)
        else:
            normalx = bpy.data.objects['Empty'+scn.projectionObjectName].location[0] - bpy.data.objects[scn.projectionObjectName].location[0]
            normaly = bpy.data.objects['Empty'+scn.projectionObjectName].location[1] - bpy.data.objects[scn.projectionObjectName].location[1]
            normalz = bpy.data.objects['Empty'+scn.projectionObjectName].location[2] - bpy.data.objects[scn.projectionObjectName].location[2]
            plots.ytProjectionPlot(ds, image_name=scn.projectionObjectName, axis=[normalx,normaly,normalz],
                                   variable=scn.projectionVariable, weight_variable = (scn.projectionWeightVariableType,scn.projectionWeightVariable),
                                   center=[slcCenter[0],slcCenter[1],slcCenter[2]],
                                   width=scn.projectionWidth, units = scn.projectionUnits, color_map = scn.projectionColorMap,
                                   show_annotations = scn.projectionShowAnnotation)
            
        # finally, have it such that the slice plot is tracked to the domain -> if the domain changes so does the plot
        #bpy.ops.object.constraint_add(type='COPY_LOCATION')
        #bpy.data.objects[scn.projectionObjectName].constraints["Copy Location"].target = bpy.data.objects[domain_name]
        #bpy.ops.object.constraint_add(type='COPY_SCALE')
        #bpy.data.objects[scn.projectionObjectName].constraints["Copy Scale"].target = bpy.data.objects[domain_name]

        return{'FINISHED'}    




############################## PHASE PLOTS #############################
# slice plots
class VIEW3D_PT_tools_ABPlots_phaseplots(View3DPanel, Panel):
    bl_category = "AB Plots"
    bl_context = "objectmode"
    bl_label = "Phase Plots"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene

        col = layout.column(align=True)
        layout.prop(scn, 'phaseLinkObjName')
        layout.prop(scn, 'phaseName')
        layout.prop(scn, 'phaseUnits')
        layout.prop(scn, 'phaseWidth')
        layout.prop(scn, 'phaseWireFrameSphere')

# maybe replace with something fancier:
#        for obj in bpy.data.objects:
#            if obj.name == scn.gridName:
#                layout.prop(obj.modifiers['Wireframe'], 'thickness')

        
        layout.prop(scn, 'phaseVariableTypeX')
        layout.prop(scn, 'phaseVariableX')
        layout.prop(scn, 'phaseVariableTypeY')
        layout.prop(scn, 'phaseVariableY')
        layout.prop(scn, 'phaseVariableTypeZ')
        layout.prop(scn, 'phaseVariableZ')

        layout.prop(scn, 'phaseWeightType')
        layout.prop(scn, 'phaseWeight')

        
        layout.prop(scn, 'phaseColorMap')

        for obj in bpy.data.objects:
            if obj:
                if obj.name == scn.phaseName:
                    col = layout.column(align=True)
                    row = col.row(align=True)
                    layout.prop(obj, 'location') # this will be the location of the sphere
                    
        col = layout.column(align=True)
        layout.operator("phase.button", text="Generate Phase Plot")
        layout.operator("deletephase.button", text="Delete Phase")
                                

#   AB slice delete Button
class PHASE_OT_Button_delete(bpy.types.Operator):
    bl_idname = "deletephase.button"
    bl_label = "Button"

    def execute(self, context):
        from scienceutils import delete_object
        # get the name
        scn = context.scene
        delete_object(bpy.data.objects[scn['phaseName']])
        return{'FINISHED'}    

                                

#   AB slice Button
class PHASE_OT_Button(bpy.types.Operator):
    bl_idname = "phase.button"
    bl_label = "Button"

    def execute(self, context):
        # how many sphere segments
        segments = 16
        thickness = 0.0001
        # activate domain
        from science import deselect_all
        deselect_all()
        bpy.data.objects[context.scene.phaseLinkObjName].select = True
        bpy.context.scene.objects.active = bpy.data.objects[context.scene.phaseLinkObjName]
        #bpy.data.objects[context.scene.phaseLinkObjName].active = True
        filename = context.active_object['ABFile']  # this is true if you have selected a domain
        domain_name = context.active_object.name
        from yt import load
        from science import plots, deselect_all, delete_object
        from numpy import zeros
        scn = context.scene
        flagg = True
        domain_name = context.scene.objects.active.name
        from science import overall_scale
        from yt import units
        new_units = scn['ViewerUnits']
        new_scale = float(scn['ViewerUnitsScale'])
        v = vars(units)        
        fac = overall_scale
        fac *= v[scn.sliceUnits]/(v[new_units]*new_scale)
        if scn.phaseWeight == "None":
            weight = None
        else:
            weight = (scn.phaseWeightType, scn.phaseWeight)
        
        for ob in bpy.data.objects: # if we have a sphere, activate it
            if ob.name == scn.phaseName:
                context.scene.objects.active = bpy.data.objects[scn.phaseName]
                flagg = False
        if flagg: # else, create it
            bpy.ops.mesh.primitive_uv_sphere_add(size=1.0, segments = segments) 
            context.active_object.name = scn.phaseName
            bpy.data.objects[scn.phaseName].location = bpy.data.objects[domain_name].location # put in zero of domain to start... I think

        if scn.phaseWireFrameSphere:
            bpy.data.objects[scn.phaseName].modifiers.clear()
            bpy.ops.object.modifier_add(type='WIREFRAME') # make wireframe
            bpy.data.objects[scn.phaseName].modifiers['Wireframe'].thickness = thickness

        else:
            bpy.data.objects[scn.phaseName].modifiers.clear()


        ds = load(filename)        

        # now, we are going to rescale things to the over all scale of the box
        #boxscalings = [(ds.domain_right_edge.in_units(scn['ViewerUnits'])-ds.domain_left_edge.in_units(scn['ViewerUnits']))]
        #bs = boxscalings[0]
        bpy.data.objects[scn.phaseName].scale = (scn.phaseWidth*fac,scn.phaseWidth*fac,scn.phaseWidth*fac)
        
        # now, derive the locations of the projections from this plane
        slcCenter = zeros(3)
        for i in range(0,3): #need to recenter if object has moved
#            slcCenter[i] = bpy.data.objects[scn.phaseName].location[i]*ds.domain_width.in_units(scn.phaseUnits)[i]/(v[new_units]*new_scale)
            slcCenter[i] = (bpy.data.objects[scn.phaseName].location[i]*(v[new_units]*new_scale))/((ds.domain_width.in_units(new_units))[i])#/v[scn.phaseUnits]
            #slcCenter[i] -= (ds.domain_center.in_units(new_units))[i]

        plots.ytPhasePlot(ds, image_name=scn.phaseName, xvar = (scn.phaseVariableTypeX, scn.phaseVariableX),
                          yvar = (scn.phaseVariableTypeY, scn.phaseVariableY),
                          color_field = (scn.phaseVariableTypeZ, scn.phaseVariableZ), weight_field = weight,
                          sphere_radius = scn.phaseWidth, center = slcCenter, sphere_units = scn.phaseUnits,
                          color_map = scn.phaseColorMap)


        # return context to sphere
        deselect_all()
        bpy.data.objects[context.scene.phaseName].select = True
        bpy.context.scene.objects.active = bpy.data.objects[context.scene.phaseName]
        
                          
        
        return{'FINISHED'}    
    


    

#-- end JPN --

        
if __name__ == "__main__":  # only for live edit.
    bpy.utils.register_module(__name__)
