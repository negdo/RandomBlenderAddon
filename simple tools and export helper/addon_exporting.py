bl_info = {
    "name": "Simple Tools and Exporting Helper",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
from bpy.utils import resource_path
from pathlib import Path


class HardJoin(bpy.types.Operator):
    bl_idname = "scene.hard_join"
    bl_label = "Hard Join"
    bl_info = "Convert to Mesh and join selected"
    
    def execute(self, context):
        # convert to mesh and join
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.join()
        return {"FINISHED"}


class RemoveMaterials(bpy.types.Operator):
    bl_idname = "scene.remove_materials"
    bl_label = "Remove Materials"
    bl_info = "Remove all materials on selected object"
    
    def execute(self, context):
        # delete materials
        bpy.context.object.active_material_index = 0
        for i in range(10):
            bpy.ops.object.material_slot_remove()

        # apply transformations
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {"FINISHED"}


class ApplyAllTransformations(bpy.types.Operator):
    bl_idname = "scene.apply_all_transformations"
    bl_label = "Apply Transformations"
    bl_info = "Applys location, rotation and scale"
    
    def execute(self, context):
        # apply transformations
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {"FINISHED"}
    

class FlipX(bpy.types.Operator):
    bl_idname = "scene.flip_x"
    bl_label = "X"
    bl_info = "Scale x -1 and flip normals"
    
    def execute(self, context):
        #scale x -1
        #edit mode
        #select all
        #flip normals
        
        bpy.ops.transform.resize(value=(-1, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.263331, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

class FlipY(bpy.types.Operator):
    bl_idname = "scene.flip_y"
    bl_label = "Y"
    bl_info = "Scale y -1 and flip normals"
    
    def execute(self, context):
        #scale y -1
        #edit mode
        #select all
        #flip normals
        
        bpy.ops.transform.resize(value=(1, -1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.263331, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

class FlipZ(bpy.types.Operator):
    bl_idname = "scene.flip_z"
    bl_label = "Z"
    bl_info = "Scale z -1 and flip normals"
    
    def execute(self, context):
        #scale z -1
        #edit mode
        #select all
        #flip normals
        
        bpy.ops.transform.resize(value=(1, 1, -1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.263331, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}   

class Normals(bpy.types.Operator):
    bl_idname = "scene.normals"
    bl_label = "Normals"
    
    def execute(self, context):
        #toggle normals
        if bpy.context.space_data.overlay.show_face_orientation == True:
            bpy.context.space_data.overlay.show_face_orientation = False
        else:
            bpy.context.space_data.overlay.show_face_orientation = True
        
        return {"FINISHED"}


class Convex(bpy.types.Operator):
    # Adds geo nodes group for convex mesh
    bl_idname = "scene.convex"
    bl_label = "Convert to Convex"
    bl_info = "Adds convex hull over every separate mesh island"

    def execute(self, context):
        selected_objs = bpy.context.selected_objects

        for obj in selected_objs:
            if obj.type == 'MESH':
                obj.display_type = 'WIRE'
                
                if obj.modifiers.get("Convex Mesh") is None: # can not find GeometryNodes modifier, add new one
                    md_node = obj.modifiers.new(type='NODES', name='Convex Mesh')

                    try:
                        md_node.node_group = bpy.data.node_groups['Convex Mesh']
                    except:
                        self.append(context) #append geonodes group, if cant be found
                        md_node.node_group = bpy.data.node_groups['Convex Mesh']
                    
        return {"FINISHED"}


    def append(self, context):
        #append node group
        USER = Path(resource_path('USER'))
        src = USER / "scripts/addons"

        file_path = src / "NodeTree.blend"
        inner_path = "NodeTree"
        object_name = "Convex Mesh"

        bpy.ops.wm.append(
            filepath=str(file_path / inner_path / object_name),
            directory=str(file_path / inner_path),
            filename=object_name
        )



####### UI ########


class SimpleTools(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Simple Tools"
    bl_idname = "SCENE_PT_layout_simple_tools"
    bl_category = "MyTools"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("scene.normals")

        split = col.split(factor=0.5)
        col1,col2 = (split.column(),split.column())
        col1.label(text="Flip Object")
        row = col2.row(align=True)
        row.use_property_split = True
        row.operator("scene.flip_x")
        row.operator("scene.flip_y")
        row.operator("scene.flip_z")


class UnrealHelper(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Exporting Helper"
    bl_idname = "SCENE_PT_layout_unreal_helper"
    bl_category = "MyTools"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator("scene.hard_join")
        col.operator("scene.apply_all_transformations")
        col.operator("scene.remove_materials")
        col.separator()
        col.operator("scene.convex")        




def register():
    bpy.utils.register_class(HardJoin)
    bpy.utils.register_class(RemoveMaterials)
    bpy.utils.register_class(ApplyAllTransformations)
    bpy.utils.register_class(FlipX)
    bpy.utils.register_class(FlipY)
    bpy.utils.register_class(FlipZ)
    bpy.utils.register_class(Normals)
    bpy.utils.register_class(Convex)

    bpy.utils.register_class(SimpleTools)
    bpy.utils.register_class(UnrealHelper)

def unregister():
    bpy.utils.unregister_class(SimpleTools)
    bpy.utils.unregister_class(UnrealHelper)

    bpy.utils.unregister_class(HardJoin)
    bpy.utils.unregister_class(RemoveMaterials)
    bpy.utils.unregister_class(ApplyAllTransformations)
    bpy.utils.unregister_class(FlipX)
    bpy.utils.unregister_class(FlipY)
    bpy.utils.unregister_class(FlipZ)
    bpy.utils.unregister_class(Normals)
    bpy.utils.unregister_class(Convex)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()