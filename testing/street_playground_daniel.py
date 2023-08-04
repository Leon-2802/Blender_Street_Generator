# https://blender.stackexchange.com/questions/278948/coons-patch-bezier-curve
# https://www.youtube.com/watch?v=Ve9h7-E8EuM
# https://www.youtube.com/watch?v=aVwxzDHniEw&t=143s
# source (bc. I can't come up with that shit on my own...| me neighter): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# Missing (for the street to have basic functionality):
# -Allow users to reopen the properties panel
# -Scaling of Street-Curve
# -Name of Object
# -extrude along Y-Axis


from mathutils import geometry
from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty, IntProperty
from bpy.types import Operator
import bpy


bl_info = {
    "name": "Street Generator",
    "author": "Daniel Litterst and Leon Gobbert",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Street Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

# Bäume richtig generieren
# Deko-Objekte an Bezier Punkten spawnen
# ...oder an Kuve entlang, wenns geht
# ggf. Sachen an einem Punkt spawnen und selbst setzten lassen
# offset
# (!!Kurve wird ggf. dann gezeichnetes)

def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y
    cuts = self.cuts

    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    # import tree
    bpy.ops.wm.obj_import(filepath="C:\\GitHub\\DVMP_FuwaTwin\\StreetGenerator\\Tree.obj", directory="C:\\GitHub\\DVMP_FuwaTwin\\StreetGenerator\\", files=[{"name":"Tree.obj", "name":"Tree.obj"}])
    tree = bpy.context.active_object
    tree.scale = (0.1, 0.1, 0.1)




    res_per_section = 6
    interpolate_bezier = geometry.interpolate_bezier
    ops_curve = bpy.ops.curve
    ops_mesh = bpy.ops.mesh

    # Create a curve, subdivide and randomize it.
    ops_curve.primitive_bezier_curve_add(enter_editmode=True)
    ops_curve.subdivide(number_cuts=cuts)
    # # bpy.ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0.01, seed=0)

    # # After randomizing the curve, recalculate its normals so
    # # the cubes calculated by interpolate bezier will be more
    # # evenly spaced.
    # ops_curve.select_all(action='SELECT')
    # ops_curve.normals_make_consistent(calc_length=True)

    # # Switch back to object mode and cache references to the curve
    # # and its bezier points.
    # bpy.ops.object.mode_set(mode='OBJECT')
    # bez_curve = bpy.context.active_object
    # # bez_points = bez_curve.data.splines[0].bezier_points







    # # Create an empty list.
    # points_on_curve = []

    # # Loop through the bezier points in the bezier curve.
    # bez_len = len(bez_points)
    # i_range = range(1, bez_len, 1)
    # for i in i_range:

    #     # Cache a current and next point.
    #     curr_point = bez_points[i - 1]
    #     next_point = bez_points[i]

    #     # Calculate bezier points for this segment.
    #     calc_points = interpolate_bezier(
    #         curr_point.co,
    #         curr_point.handle_right,
    #         next_point.handle_left,
    #         next_point.co,
    #         res_per_section + 1)

    #     # The last point on this segment will be the
    #     # first point on the next segment in the spline.
    #     if i != bez_len - 1:
    #         calc_points.pop()

    #     # Concatenate lists.
    #     points_on_curve += calc_points

    #     # Create an empty parent under which cubes will be placed.

    #     # For each point created by interpolate bezier, create a cube.
    #     # cube_rad = 1.5 / (res_per_section * bez_len)
    #     # for point in points_on_curve:
    #     #     # bpy.ops.object.empty_add(type='PLAIN_AXES', location=bez_curve.location)
    #     #     # group = bpy.context.active_object
    #     #     # point_translation = bpy.context.object.matrix_local.to_translation()
    #     #     # ops_mesh.primitive_cube_add(location=point, size=0.1, rotation=point)
    #     #     # ops_mesh.primitive_cube_add(location=point, size=0.1)

    #     #     # ops_mesh.primitive_cube_add(radius=cube_rad, location=point)
    #     #     cube = bpy.context.active_object
    #     #     # cube.parent = curve
    
    # bpy.ops.node.new_geometry_nodes_modifier()
    # bpy.ops.node.add_node(type="GeometryNodeInstanceOnPoints", use_transform=True)
    # bpy.ops.node.translate_attach_remove_on_cancel(TRANSFORM_OT_translate={"value":(-5.54033, 46.8233, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":True, "view2d_edge_pan":True, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False}, NODE_OT_attach={}, NODE_OT_insert_offset={})
    
    # geo_nodes = bpy.ops.node.translate_attach_remove_on_cancel(TRANSFORM_OT_translate={"value":(-240.696, -186.677, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":True, "view2d_edge_pan":True, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False}, NODE_OT_attach={}, NODE_OT_insert_offset={})
    # bpy.ops.node.link(detach=False, drag_start=(-293.272, -306.494))

    # geo_nodes.nodes["Object Info"].inputs[0].default_value = tree
    # geo_nodes.nodes["Instance on Points"].inputs[6].default_value[1] = 0.1
    # geo_nodes.nodes["Instance on Points"].inputs[6].default_value[2] = 0.1
    # geo_nodes.nodes["Instance on Points"].inputs[6].default_value[0] = 0.1
    

    # add GeometryNodes modifier
    bpy.ops.object.modifier_add(type='NODES')

    # access active object node_group
    node_group = bpy.context.object.modifiers[0].node_group

    nodes = node_group.nodes

    insonpoint_1 = nodes.new(type="GeometryNodeInstanceOnPoints")
    insonpoint_1.location.x += 600
    insonpoint_1.location.y += 100

    # insonpoint_2 = nodes.new(type="GeometryNodeObjectInfo")
    # insonpoint_2.location.x += 850
    # insonpoint_2.location.y -= 100


class OBJECT_OT_add_object(Operator):
    """Create a new Street Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Street Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="Scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )
    cuts: IntProperty(
        name="Cuts",
        description="Number of cuts along the street",
        default=1,
        min=0,
        max=100,
        subtype='UNSIGNED'
    )
    


    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}

# Registration
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Street Object",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()


# # https://blender.stackexchange.com/questions/278948/coons-patch-bezier-curve
# # https://www.youtube.com/watch?v=Ve9h7-E8EuM
# # https://www.youtube.com/watch?v=aVwxzDHniEw&t=143s
# # source (bc. I can't come up with that shit on my own...| me neighter): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# # Missing (for the street to have basic functionality):
# # -Allow users to reopen the properties panel
# # -Scaling of Street-Curve
# # -Name of Object
# # -extrude along Y-Axis

# from mathutils import geometry, Vector, Matrix
# from bpy_extras.object_utils import AddObjectHelper, object_data_add
# from bpy.props import FloatVectorProperty, IntProperty
# from bpy.types import Operator
# import bpy


# bl_info = {
#     "name": "Street Generator",
#     "author": "Daniel Litterst and Leon Gobbert",
#     "version": (1, 0),
#     "blender": (3, 5, 0),
#     "location": "View3D > Add > Mesh > New Object",
#     "description": "Adds a new Street Object",
#     "warning": "",
#     "doc_url": "",
#     "category": "Add Mesh",
# }


# def add_object(self, context):
#     scale_x = self.scale.x
#     scale_y = self.scale.y
#     cuts = self.cuts

#     verts = [
#         Vector((-1 * scale_x, 1 * scale_y, 0)),
#         Vector((1 * scale_x, 1 * scale_y, 0)),
#         Vector((1 * scale_x, -1 * scale_y, 0)),
#         Vector((-1 * scale_x, -1 * scale_y, 0)),
#     ]

#     edges = []
#     faces = [[0, 1, 2, 3]]

#     res_per_section = 6
#     interpolate_bezier = geometry.interpolate_bezier
#     ops_curve = bpy.ops.curve
#     ops_mesh = bpy.ops.mesh

#     # Create a curve, subdivide and randomize it.
#     ops_curve.primitive_bezier_curve_add(enter_editmode=True)
#     ops_curve.subdivide(number_cuts=cuts)

#     # After randomizing the curve, recalculate its normals so
#     # the cubes calculated by interpolate bezier will be more
#     # evenly spaced.
#     ops_curve.select_all(action='SELECT')
#     ops_curve.normals_make_consistent(calc_length=True)

#     # Switch back to object mode and cache references to the curve
#     # and its bezier points.
#     bpy.ops.object.mode_set(mode='OBJECT')
#     bez_curve = bpy.context.active_object
#     bez_points = bez_curve.data.splines[0].bezier_points

#     # Create an empty list.
#     points_on_curve = []

#     # Loop through the bezier points in the bezier curve.
#     bez_len = len(bez_points)
#     i_range = range(1, bez_len, 1)

#     for i in i_range:

#         # Cache a current and next point.
#         curr_point = bez_points[i - 1]
#         next_point = bez_points[i]

#         # Calculate bezier points for this segment.
#         calc_points = interpolate_bezier(
#             curr_point.co,
#             curr_point.handle_right,
#             next_point.handle_left,
#             next_point.co,
#             res_per_section + 1)

#         # The last point on this segment will be the
#         # first point on the next segment in the spline.
#         if i != bez_len - 1:
#             calc_points.pop()

#         # Concatenate lists.
#         points_on_curve += calc_points

#         # Create an empty parent under which cubes will be placed.
#         bpy.ops.object.empty_add(
#             type='PLAIN_AXES', location=bez_curve.location)
#         group = bpy.context.active_object

#         # For each point created by interpolate bezier, create a cube.
#         cube_rad = 1.5 / (res_per_section * bez_len)
#         # Align the cubes with the tangent of the spline
#         for point in points_on_curve:
#             ops_mesh.primitive_cube_add(location=point, size=0.1)
#             cube = bpy.context.active_object
#             cube.parent = group

#             # Get the tangent vector at the current point
#             spline = bez_curve.data.splines[0]
#             tangent = Vector()
#             if spline.type == 'BEZIER':
#                 i = int(point[0] * (len(spline.bezier_points) - 1))
#                 handle_left = spline.bezier_points[i].handle_left
#                 handle_right = spline.bezier_points[i].handle_right
#                 tangent = handle_right - handle_left
#             else:
#                 i = int(point[0] * (len(spline.points) - 1))
#                 p1 = spline.points[i].co
#                 p2 = spline.points[i + 1].co
#                 tangent = p2 - p1
#             t = tangent.normalized()

#             # Calculate the rotation matrix to align the cube with the tangent
#             up = Vector((0, 0, 1))
#             axis = up.cross(t)
#             angle = up.angle(t)
#             matrix = Matrix.Rotation(angle, 4, axis)

#             # Apply the rotation to the cube
#             cube.matrix_world = matrix @ cube.matrix_world


# class OBJECT_OT_add_object(Operator):
#     """Create a new Street Object"""
#     bl_idname = "mesh.add_object"
#     bl_label = "Add Street Object"
#     bl_options = {'REGISTER', 'UNDO'}

#     scale: FloatVectorProperty(
#         name="Scale",
#         default=(1.0, 1.0, 1.0),
#         subtype='TRANSLATION',
#         description="scaling",
#     )
#     cuts: IntProperty(
#         name="Cuts",
#         description="Number of cuts along the street",
#         default=1,
#         min=0,
#         max=100,
#         subtype='UNSIGNED'
#     )

#     def execute(self, context):
#         add_object(self, context)
#         return {'FINISHED'}

# # Registration


# def add_object_button(self, context):
#     self.layout.operator(
#         OBJECT_OT_add_object.bl_idname,
#         text="Add Street Object",
#         icon='PLUGIN')


# # This allows you to right click on a button and link to documentation
# def add_object_manual_map():
#     url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
#     url_manual_mapping = (
#         ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
#     )
#     return url_manual_prefix, url_manual_mapping


# def register():
#     bpy.utils.register_class(OBJECT_OT_add_object)
#     bpy.utils.register_manual_map(add_object_manual_map)
#     bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


# def unregister():
#     bpy.utils.unregister_class(OBJECT_OT_add_object)
#     bpy.utils.unregister_manual_map(add_object_manual_map)
#     bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


# if __name__ == "__main__":
#     register()
