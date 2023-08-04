# source: https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13

import math
from bpy.props import FloatVectorProperty, IntProperty, FloatProperty
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


def add_object(self):
    
    # Create curve object
    street_curve = bpy.data.curves.new('BezierCurve', 'CURVE')
    street_curve.dimensions = '3D'

    # Create a new spline for the curve
    spline = street_curve.splines.new('BEZIER')
    spline.bezier_points.add(self.cuts + 1)

    define_control_points(self.start_point, self.end_point, spline)

    # Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
    street_curve.fill_mode = 'HALF'
    # Breadth of extrusion, modified by lanes
    street_curve.extrude = 0.125 * self.lanes
    # create object out of curve
    obj = bpy.data.objects.new('StreetObject', street_curve)
    # Set origin right between start and end points (How tf does it work?!)

    # link to scene-collection
    collection = bpy.data.collections.get('Collection')
    if (collection):
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)


def define_control_points(start, end, spline):
    # get step-size to distribute control points evenly between start and end
    distance = end - start
    step_size = distance / (len(spline.bezier_points) - 1)

    handle_offset = step_size / 7

    # Set control points for curve
    for i in range(len(spline.bezier_points)):
        spline.bezier_points[i].tilt = 1.5708 # tilt each spline by 90 degrees
        if (i == 0):
            spline.bezier_points[i].co = start
            spline.bezier_points[i].handle_left = (
                (start.x-handle_offset.x), (start.y-handle_offset.y), (start.z-handle_offset.z))
            spline.bezier_points[i].handle_right = (
                (start.x+handle_offset.x), (start.y+handle_offset.y), (start.z+handle_offset.z))
        elif (i == (len(spline.bezier_points) - 1)):
            spline.bezier_points[i].co = end
            spline.bezier_points[i].handle_left = (
                (end.x-handle_offset.x), (end.y-handle_offset.y), (end.z-handle_offset.z))
            spline.bezier_points[i].handle_right = (
                (end.x+handle_offset.x), (end.y+handle_offset.y), (end.z+handle_offset.z))
        else:
            current = start + (step_size * i)
            spline.bezier_points[i].co = (current.x, current.y, current.z)
            spline.bezier_points[i].handle_left = (
                (current.x-handle_offset.x), (current.y-handle_offset.y), (current.z-handle_offset.z))
            spline.bezier_points[i].handle_right = (
                (current.x+handle_offset.x), (current.y+handle_offset.y), (current.z+handle_offset.z))


def get_unit_vec(start, end, factor):
    vec = end - start
    vec_len = math.sqrt(math.pow(vec.x, 2) +
                        math.pow(vec.y, 2)+math.pow(vec.z, 2))
    if (vec_len == 0):
        return (0, 0, 0)
    else:
        unit_vec = vec / vec_len
        return unit_vec*factor


class OBJECT_OT_add_object(Operator):
    """Create a new Street Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Street Object"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()

    start_point: FloatVectorProperty(
        name="Start Point",
        default=(0.0, 0.0, 0.0),
        subtype='XYZ',
        description="Choose a point where the street should begin",
    )
    end_point: FloatVectorProperty(
        name="End Point",
        default=(4.0, 0.0, 0.0),
        subtype='XYZ',
        description="Choose a point where the street should end",
    )
    lanes: IntProperty(
        name="Lanes",
        description="Number of lanes the street should have",
        default=1,
        min=1,
        max=4,
        subtype='UNSIGNED',
    )
    cuts: IntProperty(
        name="Control Points",
        description="Number of control points between start and end point",
        default=2,
        min=1,
        max=100,
        subtype='UNSIGNED',
    )

    def execute(self, context):
        add_object(self)
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
