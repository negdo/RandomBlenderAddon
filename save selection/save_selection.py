bl_info = {
    "name": "Save Selection",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
from bpy.utils import resource_path
import bmesh
import numpy as np

class SaveSelection(bpy.types.Operator):
    bl_idname = "scene.save_selection"
    bl_label = "Save Selection"
    bl_description = "Temporary save selected objects"


    def execute(self, context):
        selection = bpy.context.selected_objects
        bpy.context.scene['SavedSelection'] = selection

        return {"FINISHED"}


class RestoreSelected(bpy.types.Operator):
    bl_idname = "scene.restore_selection"
    bl_label = "Restore Selection"
    bl_description = "Restore temporary saved object selection"


    def execute(self, context):
        selection = bpy.context.scene.get('SavedSelection')

        names = []
        for i in selection:
            names.append(i.name)
        
        print(names)

        for obj in bpy.data.objects:
            # Check if object names match
            if obj.name in names:
                obj.select_set(True)
            else:
                obj.select_set(False)

        return {"FINISHED"}


class SaveSelectionEdit(bpy.types.Operator):
    bl_idname = "scene.save_selection_edit"
    bl_label = "Save Selection"
    bl_description = "Temporary save selected vertices/edges/faces"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        obj = bpy.context.active_object

        #BMESH of active object
        bm = bmesh.new() 
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()

        # add new layer on vertices
        layer = bm.verts.layers.int.get("savedSelectionCounter")
        print(layer)
        if layer == None:
            print("creating new layer")
            layer = bm.verts.layers.int.new("savedSelectionCounter")
            bm.verts.ensure_lookup_table()

        # get next number
        if bpy.context.scene.get('saveCounter') == None:
            bpy.context.scene['saveCounter'] = 1
            n = 1
        else:
            bpy.context.scene['saveCounter'] += 1
            n = bpy.context.scene['saveCounter']

        for i in range(len(obj.data.vertices)):
            if obj.data.vertices[i].select:
                bm.verts[i][layer] = n
        
        # Finish up, write the bmesh back to the mesh
        bm.to_mesh(obj.data)
        bm.free()  # free and prevent further access

        bpy.ops.object.editmode_toggle()

        return {"FINISHED"}


class RestoreSelectedEdit(bpy.types.Operator):
    bl_idname = "scene.restore_selection_edit"
    bl_label = "Restore Selection"
    bl_description = "Restore temporary saved vertex/edge/face selection"

    def execute(self, context):
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        obj = bpy.context.active_object
        selected_vertices = np.zeros(len(obj.data.vertices))

        #BMESH of active object
        bm = bmesh.new() 
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()

        layer = bm.verts.layers.int.get("savedSelectionCounter")
        if layer != None:
            print("Found stuff")
            for i in range(len(obj.data.vertices)):
                print(bm.verts[i][layer])
                # if number in vertex is equal to saveCounter
                obj.data.vertices[i].select = (bm.verts[i][layer] == bpy.context.scene['saveCounter'])

            
        bm.free()  # free and prevent further access

        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}



def draw_save_selected_menu(self, context):
    # add operator to context menu
    layout = self.layout
    #layout.separator()
    layout.operator("scene.save_selection")
    layout.operator("scene.restore_selection")

def draw_save_selected_edit_menu(self, context):
    # add operator to context menu
    layout = self.layout
    #layout.separator()
    layout.operator("scene.save_selection_edit")
    layout.operator("scene.restore_selection_edit")
    

def register():
    bpy.utils.register_class(SaveSelection)
    bpy.utils.register_class(RestoreSelected)
    bpy.utils.register_class(SaveSelectionEdit)
    bpy.utils.register_class(RestoreSelectedEdit)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_save_selected_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_save_selected_edit_menu)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_save_selected_menu)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(draw_save_selected_edit_menu)
    bpy.utils.unregister_class(SaveSelection)
    bpy.utils.unregister_class(RestoreSelected)
    bpy.utils.unregister_class(SaveSelectionEdit)
    bpy.utils.unregister_class(RestoreSelectedEdit)


if __name__ == "__main__":
    register()

    