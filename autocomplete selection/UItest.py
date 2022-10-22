import bpy, gpu, bgl
import bmesh
from gpu_extras.batch import batch_for_shader
from struct import pack

obj = bpy.context.active_object
mat = obj.matrix_world
context = bpy.context
bm = bmesh.from_edit_mesh(obj.data)

def get_coords():
    print([mat @ v.co for v in bm.verts])
    return [mat @ v.co for v in bm.verts]

def get_active_coords():
    coords = []
    tris = bm.calc_loop_triangles()
    for face in tris:
        if face.select:
            coords += [mat @ v.co for v in face.verts]
    return coords

def get_active_faces():
    coords = []
    tris = bm.calc_loop_triangles()
    for face in tris:
        if face[0].face.select:
            for v in face:
                coords.append(v.vert.co)

            #coords += [mat @ v.co for v in face[0].face.verts]

    print(len(coords))
    return coords


r, g, b, a = 1.0, 1.0, 0.0, 0.2
shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")

def draw():
    bgl.glLineWidth(1)
    batch = batch_for_shader(shader, 'TRIS', {"pos": get_active_faces()})
    shader.bind()
    color = shader.uniform_from_name("color")
    shader.uniform_vector_float(color, pack("4f", r, g, b, a), 4)
    batch.draw(shader)

if __name__ == "__main__":
    st = bpy.types.SpaceView3D
    st.draw_handler_add(draw, (), 'WINDOW', 'POST_VIEW')

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()