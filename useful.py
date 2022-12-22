import bpy

bl_info = {
    "name": "Useful BS",
    "description": "Addon with useful tools for Brawl Stars Editing",
    "author": "xXCooBloyXx",
    "version": (1, 3),
    "blender": (3, 0, 0)
}

class UsefulPanel(bpy.types.Panel):
    bl_label = "Useful BS"
    bl_idname = "OBJECT_PT_useful"
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
        row.operator("object.fix_errors", text="Fix Errors")

        row = layout.row()
        row.label(text="UV Tools:")

        row = layout.row()
        row.operator("object.fix_glb_uv", text="Fix Glb UV")

        row = layout.row()
        row.label(text="Others:")

        row = layout.row()
        row.operator("object.clear_mats", text="Clear All Mats")

class UsefulAnimPanel(bpy.types.Panel):
    bl_label = "Useful Anim BS"
    bl_idname = "OBJECT_PT_usefulanim"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Useful BS"

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'ARMATURE'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop_search(context.object.animation_data, "action", bpy.data, "actions", text="Action")
        row = layout.row()
        if hasattr(bpy.context, "object"):
            obj = bpy.context.object
            anim_data = obj.animation_data

            if anim_data is not None and anim_data.action is not None:
                action = anim_data.action
                frame_range = action.frame_range
                end_frame = int(frame_range[1])
        row.label(text=f"Action Frames: {end_frame}")

        row = layout.row()
        row.operator("object.fix_frames", text="Fix Frames")

        row = layout.row()
        row.operator("object.bake_action", text="Bake Action")

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

class ClearMatsOperator(bpy.types.Operator):
    bl_idname = "object.clear_mats"
    bl_label = "Clear All Mats"
    bl_description = "Removes all mats from all meshes"

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
        return {'FINISHED'}

class FixErrorsOperator(bpy.types.Operator):
    bl_idname = "object.fix_errors"
    bl_label = "Fix Errors"
    bl_description = "Fixes errors when you trying to convert dae to scw, example error on convert: 'Bad joint count for vertex', this option can fix it!"

    def execute(self, context):
        # Iterate through all the meshes in the scene
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                # Go to weight paint mode and select the "limit total" option
                bpy.ops.object.select_by_type(type='MESH')
                bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
                bpy.ops.object.vertex_group_limit_total()
                bpy.ops.object.mode_set(mode='OBJECT')

                # Iterate through all the meshes without a material
                for mesh in bpy.data.meshes:
                    if not mesh.materials:
                        # Assign a material to the mesh
                        if bpy.data.materials:
                            # Assign the first material in the scene to the mesh
                            mesh.materials.append(bpy.data.materials[0])
                        else:
                            # Create a new material and assign it to the mesh
                            mat = bpy.data.materials.new(name="Material")
                            mesh.materials.append(mat)

        return {'FINISHED'}

class FixFramesOperator(bpy.types.Operator):
    bl_idname = "object.fix_frames"
    bl_label = "Fix Frames"
    bl_description = "Changing frames to frames from current action"

    def execute(self, context):
        # Iterate through all the meshes in the scene
        if hasattr(bpy.context, "object"):
            obj = bpy.context.object
            anim_data = obj.animation_data

            if anim_data is not None and anim_data.action is not None:
                action = anim_data.action
                frame_range = action.frame_range
        bpy.context.scene.frame_end = int(frame_range[1])
        return {'FINISHED'}

class BakeActionOperator(bpy.types.Operator):
    bl_idname = "object.bake_action"
    bl_label = "Bake Action"
    bl_description = "Baking action - removing empty frames in animation"

    def execute(self, context):
        # Iterate through all the meshes in the scene
        if hasattr(bpy.context, "object"):
            obj = bpy.context.object
            anim_data = obj.animation_data

            if anim_data is not None and anim_data.action is not None:
                action = anim_data.action
                frame_range = action.frame_range
        bpy.ops.object.posemode_toggle()
        bpy.ops.nla.bake(frame_start=0, frame_end=int(frame_range[1]), only_selected=False, visual_keying=True, clear_constraints=True, clear_parents=True, bake_types={'POSE'})
        bpy.ops.object.posemode_toggle()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(UsefulPanel)
    bpy.utils.register_class(UsefulAnimPanel)
    bpy.utils.register_class(FixNamesOperator)
    bpy.utils.register_class(FixUVNamesOperator)
    bpy.utils.register_class(ClearMatsOperator)
    bpy.utils.register_class(FixGlbUVOperator)
    bpy.utils.register_class(FixErrorsOperator)
    bpy.utils.register_class(FixFramesOperator)
    bpy.utils.register_class(BakeActionOperator)

def unregister():
    bpy.utils.unregister_class(UsefulPanel)
    bpy.utils.unregister_class(UsefulAnimPanel)
    bpy.utils.unregister_class(FixNamesOperator)
    bpy.utils.unregister_class(FixUVNamesOperator)
    bpy.utils.unregister_class(ClearMatsOperator)
    bpy.utils.unregister_class(FixGlbUVOperator)
    bpy.utils.unregister_class(FixErrorsOperator)
    bpy.utils.unregister_class(FixFramesOperator)
    bpy.utils.unregister_class(BakeActionOperator)

if __name__ == "__main__":
    register()
