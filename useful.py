import bpy

bl_info = {
    "name": "Useful BS",
    "description": "Addon with useful tools for Brawl Stars Editing",
    "author": "xXCooBloyXx",
    "version": (1, 1),
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

        row = layout.row()
        row.label(text="UV Tools:")

        row = layout.row()
        row.operator("object.fix_glb_uv", text="Fix Glb UV")

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

class FixGlbUVOperator(bpy.types.Operator):
    bl_idname = "object.fix_glb_uv"
    bl_label = "Fix Glb UV"
    bl_description = "Fixes UV from glb models"

    def execute(self, context):

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.context.area.ui_type = 'UV'
        bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(0.000244, 0.000244, 0.000244), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.translate(value=(0, 1, 0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.area.ui_type = 'VIEW_3D'
        bpy.ops.object.editmode_toggle()
		
        return {'FINISHED'}

def register():
    bpy.utils.register_class(UsefulPanel)
    bpy.utils.register_class(FixUVNamesOperator)
    bpy.utils.register_class(FixNamesOperator)
    bpy.utils.register_class(FixGlbUVOperator)

def unregister():
    bpy.utils.unregister_class(UsefulPanel)
    bpy.utils.unregister_class(FixUVNamesOperator)
    bpy.utils.unregister_class(FixNamesOperator)
    bpy.utils.unregister_class(FixGlbUVOperator)


if __name__ == "__main__":
    register()
