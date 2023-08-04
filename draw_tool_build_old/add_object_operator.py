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
    # Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
    street_curve.fill_mode = 'HALF'
    # Breadth of extrusion, modified by lanes
    if self.lanes == 3:
        street_curve.extrude = 4
    street_curve.extrude = 1 * self.lanes * self.scaleFactor
    # create object out of curve
    obj = bpy.data.objects.new('Street', street_curve)
    # link to scene-collection
    helper_functions.link_to_collection(obj)

    # Set the context for the operator
    bpy.context.view_layer.objects.active = obj
    # Toggle to Edit Mode
    bpy.ops.object.editmode_toggle()
    # select draw tool
    bpy.ops.wm.tool_set_by_id(name="builtin.draw")
    
    # Define a custom handler function to apply the tilt and the material
    def handle_spline_draw(context):
        # unassign this method from the handler, so it's only called once
        bpy.app.handlers.depsgraph_update_post.clear()
        # assign material
        helper_functions.assign_road_material(self.walkway, self.lanes)
        # Access the active object (the drawn splines)
        for curve in bpy.data.curves:

            if curve == street_curve: 
                # add decorations
                # add_decoration.add_decoration(self, street_curve)
                for spline in curve.splines:
                    
                    if spline.type != 'BEZIER':
                        print('only bezier splines allowed')
                        continue
                    
                    total_points = len(spline.bezier_points)
                    if total_points == 0:
                        continue
                    
                    # Iterate over each point in the spline
                    for point in spline.bezier_points:
                        # Modify the tilt by 90 degrees
                        point.tilt = 1.5708  # 90 degrees in radians
                        # deselect the points controls
                        point.select_control_point = False
                        point.select_left_handle = False
                        point.select_right_handle = False
                
                # back to object mode
                bpy.ops.object.editmode_toggle()
        


    # Register the handler function
    bpy.app.handlers.depsgraph_update_post.append(handle_spline_draw)



class OBJECT_OT_add_object(Operator):
    """Paint a new Street Object"""
    bl_idname = "curve.paint_street_old"
    bl_label = "Paint Street Curve Old"
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