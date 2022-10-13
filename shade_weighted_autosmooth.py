bl_info = {
    "name": "auto smooth addon",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
from bpy.utils import resource_path
from pathlib import Path


class WeightedAutoSmooth(bpy.types.Operator):
    bl_idname = "scene.weightedsmooth"
    bl_label = "Shade Weighted Auto Smooth Shortcut"
    bl_description = "Toggles Weighted Normals modifier and smooth shading"

    def execute(self, context):
        obj = bpy.context.active_object
        if obj != None and obj.type == 'MESH':
            # find if weighted normals modifier exists
            found  = False
            for md in obj.modifiers:
                if md.type == 'WEIGHTED_NORMAL':
                    
                    # remove modifier and shade flat
                    modifier_to_remove = obj.modifiers.get("WeightedNormal")
                    obj.modifiers.remove(modifier_to_remove)
                    bpy.ops.object.shade_flat()

                    found = True
                    break
            
            if not found:
                # add weighted normals modifier with "keep sharp" and then shade autosmooth
                bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
                bpy.context.object.modifiers["WeightedNormal"].keep_sharp = True
                bpy.ops.object.shade_smooth(use_auto_smooth=True)

        return {"FINISHED"}


def draw_weightedsmooth_menu(self, context):
    # add operator to context menu
    layout = self.layout
    layout.separator()
    layout.operator("scene.weightedsmooth", text="Toggle Weighted Smooth")

    

def register():
    bpy.utils.register_class(WeightedAutoSmooth)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_weightedsmooth_menu)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_weightedsmooth_menu)
    bpy.utils.unregister_class(WeightedAutoSmooth)


if __name__ == "__main__":
    register()

    