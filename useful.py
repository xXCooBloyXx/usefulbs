import bpy

bl_info = {
    "name": "Useful BS",
    "description": "Addon with useful tools for Brawl Stars Editing",
    "author": "xXCooBloyXx",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Useful BS",
    "category": "Object"
}

class UsefulPanel(bpy.types.Panel):
    bl_label = "Useful BS"
    bl_idname = "OBJECT_PTP_useful"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Useful BS"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Fix Tools:")

        row = layout.row()
        row.operator("object.fix_uv_names", text="Fix UV Names")

        row = layout.row()
        row.operator("object.fix_names", text="Fix Names")

class FixUVNamesOperator(bpy.types.Operator):
    bl_idname = "object.fix_uv_names"
    bl_label = "Fix UV Names"
    bl_description = "Rename all mesh UV maps to the same, by this u can join meshes into one without losing UV"

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for uv_map in obj.data.uv_layers:
                    uv_map.name = "UVMap"
        return {'FINISHED'}

class FixNamesOperator(bpy.types.Operator):
    bl_idname = "object.fix_names"
    bl_label = "Fix Names"
    bl_description = "Rename mesh data to name of mesh(End ugly ""Cube"" names etc.)"

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.data.name = obj.name+"-mesh"
        return {'FINISHED'}

def register():
    bpy.utils.register_class(UsefulPanel)
    bpy.utils.register_class(FixUVNamesOperator)
    bpy.utils.register_class(FixNamesOperator)

def unregister():
    bpy.utils.unregister_class(UsefulPanel)
    bpy.utils.unregister_class(FixUVNamesOperator)
    bpy.utils.unregister_class(FixNamesOperator)

if __name__ == "__main__":
    register()