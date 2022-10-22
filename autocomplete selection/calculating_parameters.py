from collections import defaultdict
import bpy
import bmesh
import gpu, bgl
from gpu_extras.batch import batch_for_shader
from struct import pack

bmg = bmesh.from_edit_mesh(bpy.context.active_object.data)

class Autocomplete(bpy.types.Operator):
    bl_idname = "scene.autocomplete"
    bl_label = "Autocomplete Selection"
    bl_description = "Toggles Weighted Normals modifier and smooth shading"

    def execute(self, context):

        

        st = bpy.types.SpaceView3D
        st.draw_handler_add(draw, (), 'WINDOW', 'POST_VIEW')

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

        return {"FINISHED"}


def autocomplete():
    obj = bpy.context.active_object
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bmg = bm

    layer = bm.faces.layers.int.get("AutocompleteSelect")
    if layer == None:
        layer = bm.faces.layers.int.new("AutocompleteSelect")
        bm.faces.ensure_lookup_table()
    
    print("Autocomplete Selection")

    parameters_faces = {
        "normal": [],
        "area": []
        }

    # fill parameters dict with data from selected faces
    for face in bm.faces:
        if face.select:
            get_parameters(face, parameters_faces)

    # calculate average of parameters
    parameters, diff = avg_parameters(parameters_faces)
    print(parameters)
    print(diff)
    
    for face in bm.faces:
        if not face.select:
            if compare_parameters(face, parameters, diff):
                face[layer] = 1
            else:
                face[layer] = 0

    bm.faces.ensure_lookup_table()
    return


def get_parameters(face, parameters):
    parameters["normal"].append(face.normal)
    parameters["area"].append(face.calc_area())


def zero():
    return 0


def vecLen(vector):
    return (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5


def avg_parameters(parameters_faces):
    avg = {}
    diff = {}
    lenght = len(parameters_faces["normal"])
    delta = 0.01

    # sum all parameters
    for i in range(lenght):
        try: avg["normal"] += parameters_faces["normal"][i]
        except: avg["normal"] = parameters_faces["normal"][i]
        try: avg["area"] += parameters_faces["area"][i]
        except: avg["area"] = parameters_faces["area"][i]

    # divide by number of selected faces
    for key in avg:
        avg[key] /= lenght

    diff["normal"] = vecLen(avg["normal"] - parameters_faces["normal"][0])+delta
    diff["area"] = abs(avg["area"] - parameters_faces["area"][0])+delta

    for i  in range(1, lenght, 1):
        diff["normal"] = max(diff["normal"], vecLen(avg["normal"] - parameters_faces["normal"][i])+delta)
        diff["area"] = max(diff["area"], abs(avg["area"] - parameters_faces["area"][i])+delta)

    return avg, diff


def compare_parameters(face, parameters, diff):
    # compare normal
    normal_diff = vecLen(face.normal - parameters["normal"])
    area_diff = abs(face.calc_area() - parameters["area"])

    print("normal", normal_diff, "area", area_diff)

    if normal_diff <= diff["normal"] and area_diff <= diff["area"]:
        return True
    else:
        return False


def get_active_faces():
    bmg.faces.ensure_lookup_table()
    coords = []
    try: 
        layer = bmg.faces.layers.int.get("AutocompleteSelect")
        tris = bmg.calc_loop_triangles()
        for face in tris:
            if face[0].face[layer] == 1:
                for v in face:
                    coords.append(v.vert.co)
    except: pass
    return coords

r, g, b, a = 1.0, 1.0, 0.0, 0.2
shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")

def draw():
    autocomplete()

    bgl.glLineWidth(1)
    batch = batch_for_shader(shader, 'TRIS', {"pos": get_active_faces()})
    shader.bind()
    color = shader.uniform_from_name("color")
    shader.uniform_vector_float(color, pack("4f", r, g, b, a), 4)
    batch.draw(shader)


addon_keymaps = []
def register():
    bpy.utils.register_class(Autocomplete)

    # Add the hotkey
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(Autocomplete.bl_idname, type='SPACE', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))




    

def unregister():
    bpy.utils.unregister_class(Autocomplete)

if __name__ == "__main__":
    register()
    