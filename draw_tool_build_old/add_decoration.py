# https://blender.stackexchange.com/questions/278948/coons-patch-bezier-curve
# https://www.youtube.com/watch?v=Ve9h7-E8EuM
# https://www.youtube.com/watch?v=aVwxzDHniEw&t=143s
# source (bc. I can't come up with that shit on my own...| me neighter): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# Missing (for the street to have basic functionality):
# -Allow users to reopen the properties panel
# -Scaling of Street-Curve
# -Name of Object
# -extrude along Y-Axis

# Bäume richtig generieren
# Deko-Objekte an Bezier Punkten spawnen
# ...oder an Kuve entlang, wenns geht
# ggf. Sachen an einem Punkt spawnen und selbst setzten lassen
# offset
# (!!Kurve wird ggf. dann gezeichnetes)

import math
from mathutils import geometry, Vector, Matrix
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty, IntProperty
from bpy.types import Operator
import bpy

def add_decoration(self, curve):

    bpy.ops.object.mode_set(mode='OBJECT')

    for obj in bpy.data.objects:
        obj.select_set(False)
    # Create plane.
    bpy.ops.mesh.primitive_plane_add(calc_uvs=True, size=0.01) ######### ADD SINGLE VERT OR AN EMPTY
    plane1 = bpy.context.active_object
    bpy.ops.wm.obj_import(filepath="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/Tree.obj",
                          directory="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/", files=[{"name": "Tree.obj", "name": "Tree.obj"}])
    tree1 = bpy.context.active_object
    tree1.use_instance_vertices_rotation(True)
    tree1.scale = (0.1, 0.1, 0.1)
    tree1.parent = plane1
    tree1.hide_set(True)
    plane1.instance_type = 'FACES'


    bpy.ops.mesh.primitive_plane_add(calc_uvs=True, size=0.1)
    plane2 = bpy.context.active_object
    bpy.ops.wm.obj_import(filepath="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/Tree.obj",
                          directory="C:/GitHub/DVMP_FuwaTwin/StreetGenerator/", files=[{"name": "Tree.obj", "name": "Tree.obj"}])
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
    array_mod1.relative_offset_displace = (50, 0.0, 0.0)
    # array_mod1.count

    # Curve modifier properties.
    curve_mod1.object = curve
    curve_mod1.deform_axis = 'POS_X'

    plane1.location[1] = 0.5
    #tree1.location[1] = 0.5

    # tree1.location[1] = self.tree_offset * 0.1

    array_mod2 = plane2.modifiers.new(name='Array', type='ARRAY')
    curve_mod2 = plane2.modifiers.new(name='Curve', type='CURVE')

    # Array modifier properties.
    array_mod2.fit_type = 'FIT_CURVE'
    array_mod2.curve = curve
    array_mod2.use_relative_offset = True
    # array_mod2.relative_offset_displace = (self.tree_distance, 0.0, 0.0) # Adjust the offset values here (x, y, z).
    # Adjust the offset values here (x, y, z).
    array_mod2.relative_offset_displace = (50, 0.0, 0.0)

    # Curve modifier properties.
    curve_mod2.object = curve
    curve_mod2.deform_axis = 'POS_X'

    plane2.location[1] = -0.5
    #tree2.location[1] = -0.5

    # Apply modifiers and separate the Objects
    # bpy.ops.object.modifier_apply(modifier="Array")
    # bpy.ops.object.mode_set(mode='EDIT')
    # bpy.ops.mesh.separate(type="LOOSE")
    # bpy.ops.object.mode_set(mode='OBJECT')

    # bpy.ops.object.select_all(action='DESELECT')