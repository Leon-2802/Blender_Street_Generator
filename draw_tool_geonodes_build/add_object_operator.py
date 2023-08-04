import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty
from bpy.types import Operator
from . import helper_functions
from . import add_decoration


def add_object(self):
    street_curve = bpy.data.curves.new('BezierCurve', 'CURVE')
    street_curve.dimensions = '3D'

    # switch all open 3d views to view scene from top -> drawn street lays on ground
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            override = bpy.context.copy()
            override["area"] = area
            bpy.ops.view3d.view_axis(override, type='TOP', align_active=False) 
            if  area.spaces.active.region_3d.is_perspective:
                bpy.ops.view3d.view_persportho(override)
            else:
                pass

    # higher resolution = cleaner curves
    street_curve.resolution_u = 40
    # create object out of curve
    obj = bpy.data.objects.new('Street', street_curve)
    # link to scene-collection and select obj
    collection = bpy.data.collections.get('Collection')
    if (collection):
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)

    # Set the context for the operator
    bpy.context.view_layer.objects.active = obj
    # Toggle to Edit Mode
    bpy.ops.object.editmode_toggle()
    bpy.ops.wm.tool_set_by_id(name="builtin.draw")
    
    # Define a custom handler function to apply the geo nodes
    def handle_spline_draw(context):
        bpy.app.handlers.depsgraph_update_post.clear()

        helper_functions.build_geometry_node_tree(obj, self.walkway, self.lanes, self.scaleFactor)
        add_decoration.add_decoration(self, obj)

        # deselect all curve controls
        helper_functions.deselect_all_curves()
        # back to object mode
        bpy.ops.object.editmode_toggle()


    # Register the handler function
    bpy.app.handlers.depsgraph_update_post.append(handle_spline_draw)


class OBJECT_OT_add_object(Operator):
    """Paint a new Street Object"""
    bl_idname = "curve.paint_street"
    bl_label = "Paint Street Curve"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()

    walkway: BoolProperty(
        name="Walkway",
        description="Whether to have a street or walkway texture",
        default=False
    )

    lanes: IntProperty(
        name="Lanes",
        description="Number of lanes the street should have",
        default=1,
        min=1,
        max=4,
        subtype='UNSIGNED',
    )

    scaleFactor: FloatProperty(
        name="Scale Factor",
        description="Scale width of street",
        default=0.1,
        min=0.1,
        max=10.0,
        step=0.1
    )

    def execute(self, context):
        add_object(self)
        return {'FINISHED'}