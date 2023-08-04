# https://blender.stackexchange.com/questions/278948/coons-patch-bezier-curve
# https://www.youtube.com/watch?v=Ve9h7-E8EuM
# https://www.youtube.com/watch?v=aVwxzDHniEw&t=143s
# source (bc. I can't come up with that shit on my own...| me neighter): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# Missing (for the street to have basic functionality):
# -Allow users to reopen the properties panel
# -Scaling of Street-Curve
# -Name of Object
# -extrude along Y-Axis

import math
import pathlib
from mathutils import geometry, Vector, Matrix
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

def get_script_dir(): 
    script_path = __file__
    script_dir = pathlib.Path(script_path).resolve().parent
    return script_dir

def add_object(self):

    # Create bezier circle and randomize.
    bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True)
    bpy.ops.curve.subdivide(number_cuts=4)
    # bpy.ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0, seed=0)
    bpy.ops.transform.resize(value=(2.0, 2.0, 3.5))
    bpy.ops.object.mode_set(mode='OBJECT')
    curve = bpy.context.active_object

    # Create plane.
    bpy.ops.mesh.primitive_plane_add(calc_uvs=True, size=0.1)
    plane1 = bpy.context.active_object
    # bpy.ops.object.mode_set(mode='EDIT')
    # bpy.ops.mesh.merge(type='CENTER')
    # bpy.ops.object.mode_set(mode='OBJECT')
    script_dir = get_script_dir()
    treepath = (script_dir / "Objects/Tree.obj")
    # img = bpy.data.images.load(treepath.__str__())

    bpy.ops.wm.obj_import(filepath=treepath.__str__(),
                          directory=script_dir.__str__() + "/Objects/", files=[{"name": "Tree.obj", "name": "Tree.obj"}])
    tree1 = bpy.context.active_object
    #tree1.rotation_euler = (90, 0, 0)
    tree1.scale = (0.1, 0.1, 0.1)
    tree1.parent = plane1
    tree1.hide_set(True)
    plane1.instance_type = 'FACES'

    bpy.ops.mesh.primitive_plane_add(calc_uvs=True, size=0.1)
    plane2 = bpy.context.active_object
    # bpy.ops.object.mode_set(mode='EDIT')
    # bpy.ops.mesh.merge(type='CENTER')
    # bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.wm.obj_import(filepath="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/Objects/Tree.obj",
                          directory="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/Objects/", files=[{"name": "Tree.obj", "name": "Tree.obj"}])
    tree2 = bpy.context.active_object

    tree2.scale = (0.1, 0.1, 0.1)
    tree2.parent = plane2
    tree2.hide_set(True)
    plane2.instance_type = 'FACES'

    # Append modifiers.
    array_mod1 = plane1.modifiers.new(name='Array', type='ARRAY')
    curve_mod1 = plane1.modifiers.new(name='Curve', type='CURVE')

    # Array modifier properties.
    array_mod1.fit_type = 'FIT_CURVE'
    array_mod1.curve = curve
    array_mod1.use_relative_offset = True
    # array_mod1.relative_offset_displace = (self.tree_distance, 0.0, 0.0) # Adjust the offset values here (x, y, z).
    # Adjust the offset values here (x, y, z).
    array_mod1.relative_offset_displace = (3, 0.0, 0.0)

    # Curve modifier properties.
    curve_mod1.object = curve
    curve_mod1.deform_axis = 'POS_X'

    plane1.location[1] = 0.5

    array_mod2 = plane2.modifiers.new(name='Array', type='ARRAY')
    curve_mod2 = plane2.modifiers.new(name='Curve', type='CURVE')

    # Array modifier properties.
    array_mod2.fit_type = 'FIT_CURVE'
    array_mod2.curve = curve
    array_mod2.use_relative_offset = True
    array_mod2.relative_offset_displace = (3, 0.0, 0.0)

    # Curve modifier properties.
    curve_mod2.object = curve
    curve_mod2.deform_axis = 'POS_X'

    plane2.location[1] = -0.5


    plane1.select_set(True)
    bpy.ops.object.duplicates_make_real()
    # plane1.duplicates_make_real()
    bpy.ops.object.select_all(action='DESELECT')

    plane2.select_set(True)
    bpy.ops.object.duplicates_make_real()
    # plane2.duplicates_make_real()
    bpy.ops.object.select_all(action='DESELECT')




    for obj in bpy.data.objects:
        # Check if the object's name contains "tree"
        if "tree" in obj.name.lower():
            print("fount tree")
            # Select the object
            obj.select_set(True)
            obj.rotation_euler[1] = 0
            bpy.ops.object.select_all(action='DESELECT')


    # Apply modifiers and separate the Objects
    # bpy.ops.object.modifier_apply(modifier="Array")
    # bpy.ops.object.mode_set(mode='EDIT')
    # bpy.ops.mesh.separate(type="LOOSE")
    # bpy.ops.object.mode_set(mode='OBJECT')

    # bpy.ops.object.select_all(action='DESELECT')


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
    tree_distance: IntProperty(
        name="Tree Count",
        description="Distance between trees",
        default=0,
        min=-50,
        max=50,
        subtype='UNSIGNED',
    )
    tree_offset: IntProperty(
        name="Tree Offset",
        description="Distance from trees to the middle of the road",
        default=5,
        min=1,
        max=10,
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