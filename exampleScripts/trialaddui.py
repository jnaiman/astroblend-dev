# this is just runable in the text editor... for now

import bpy


class HelloWorldPanelTools2(bpy.types.Panel):
    """Creates a Panel in the tools properties window"""
    bl_category = "Tools"
    bl_label = "Hello World Panel2"
    bl_idname = "OBJECT_PT_helloTools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")


def register():
    bpy.utils.register_class(HelloWorldPanelTools2)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanelTools2)


if __name__ == "__main__":
    register()
