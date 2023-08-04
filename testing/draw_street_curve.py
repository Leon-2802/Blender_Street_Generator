from bpy.props import IntProperty
from bpy.types import Operator
import bpy
import random


bl_info = {
    "name": "Street Draw",
    "author": "Daniel Litterst and Leon Gobbert",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Add > Mesh > Test Draw",
    "description": "Adds a new Street Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


def add_object(self, context):
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
        build_geometry_node_tree(obj)
        # back to object mode
        bpy.ops.object.editmode_toggle()
               

    # Register the handler function
    bpy.app.handlers.depsgraph_update_post.append(handle_spline_draw)


def build_geometry_node_tree(obj):
    bpy.ops.node.new_geometry_nodes_modifier()
    geo_node_tree = obj.modifiers[-1].node_group

    in_node = geo_node_tree.nodes["Group Input"]
    in_node.location.x = -1000.0
    out_node = geo_node_tree.nodes["Group Output"]
    out_node.location.x = 1000.0
    spline_param_00_node: bpy.types.GeometryNodeSpline = create_geo_node(geo_node_tree, "GeometryNodeSplineParameter", -8.5, -200)
    store_named_attr_00_node = create_geo_node(geo_node_tree, "GeometryNodeStoreNamedAttribute", -8.0, 0)
    curve_line_node = create_geo_node(geo_node_tree, "GeometryNodeCurvePrimitiveLine", -6.0, -80)
    store_named_attr_01_node = create_geo_node(geo_node_tree, "GeometryNodeStoreNamedAttribute", -4.0, -150)
    spline_param_01_node = create_geo_node(geo_node_tree, "GeometryNodeSplineParameter", -4.0, -400)
    curve_to_mesh_node = create_geo_node(geo_node_tree, "GeometryNodeCurveToMesh", -1.0, 0)
    set_mat_node = create_geo_node(geo_node_tree, "GeometryNodeSetMaterial", 2.0, 0)
    set_pos_node = create_geo_node(geo_node_tree, "GeometryNodeSetPosition", 5.0, 0)

    store_named_attr_00_node.inputs[2].default_value = 'Gradient X'
    store_named_attr_01_node.inputs[2].default_value = 'Gradient Y'
    curve_line_node.inputs[0].default_value = (-1, 0, 0)
    curve_line_node.inputs[1].default_value = (1, 0, 0)
    set_mat_node.inputs[2].default_value = create_road_material()
    set_pos_node.inputs[3].default_value = (0, 0, 0.01)

    print(spline_param_00_node.output_template)

    # find_outputs(curve_line_node)
    spline_param_lookup = {socket.type: socket for socket in spline_param_00_node.outputs.values()}
    print(spline_param_lookup)


    geo_node_tree.links.new(in_node.outputs[0], store_named_attr_00_node.inputs[0])
    geo_node_tree.links.new(spline_param_lookup["VALUE"], store_named_attr_00_node.inputs[3])
    geo_node_tree.links.new(store_named_attr_00_node.outputs[0], curve_to_mesh_node.inputs[0])
    geo_node_tree.links.new(curve_line_node.outputs[0], store_named_attr_01_node.inputs[0])
    geo_node_tree.links.new(spline_param_01_node.outputs['Factor'], store_named_attr_01_node.inputs[3])
    geo_node_tree.links.new(store_named_attr_01_node.outputs[0], curve_to_mesh_node.inputs[1])
    geo_node_tree.links.new(curve_to_mesh_node.outputs[0], set_mat_node.inputs[0])
    geo_node_tree.links.new(set_mat_node.outputs[0], set_pos_node.inputs[0])
    geo_node_tree.links.new(set_pos_node.outputs[0], out_node.inputs[0])

    print("set up node tree")


def create_geo_node(node_tree, type_name, node_x_location, node_y_location):
    new_node = node_tree.nodes.new(type_name)
    new_node.location.x = node_x_location * 100.0
    new_node.location.y = node_y_location
    return new_node


def find_outputs(node):
    sockets = dict()
    for socket in node.outputs.values():
        sockets[socket.type] = socket
    
    import pprint
    pprint.pprint(sockets)


def set_unique_name(name):
    name += str(random.randrange(10000000))
    while bpy.data.materials.get(name):
        name = name + str(random.randrange(10000000))
    
    return name


def create_road_material():
    name = set_unique_name("RoadMaterial")
    road_mat = bpy.data.materials.new(name)
    road_mat.use_nodes = True
    nodes = road_mat.node_tree.nodes

    imgpath = "C:/Users/Le_go/Documents/GitHub/DVMP_FuwaTwin/StreetGenerator/draw_tool_geonodes_build/textures/four_lane.png"
    img = bpy.data.images.load(imgpath)

    principled_BSDF = nodes.get('Principled BSDF')
    attr_node_00 = nodes.new('ShaderNodeAttribute')
    attr_node_01 = nodes.new('ShaderNodeAttribute')
    combine_xyz_node = nodes.new('ShaderNodeCombineXYZ')
    divide_node = nodes.new('ShaderNodeVectorMath')
    tex_node: bpy.types.Node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img

    attr_node_00.attribute_name = "Gradient X"
    attr_node_01.attribute_name = "Gradient Y"
    divide_node.operation = 'DIVIDE'
    divide_node.inputs[1].default_value = (3.0, 1.0, 1.0)
    
    road_mat.node_tree.links.new(attr_node_00.outputs[2], combine_xyz_node.inputs[0])
    road_mat.node_tree.links.new(attr_node_01.outputs[2], combine_xyz_node.inputs[1])
    road_mat.node_tree.links.new(combine_xyz_node.outputs[0], divide_node.inputs[0])
    road_mat.node_tree.links.new(divide_node.outputs[0], tex_node.inputs[0])
    road_mat.node_tree.links.new(tex_node.outputs[0], principled_BSDF.inputs[0])
    return road_mat

class OBJECT_OT_add_object(Operator):
    """Create a new Street Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Street Object"
    bl_options = {'REGISTER', 'UNDO'}

    lanes: IntProperty(
        name="Lanes",
        description="Number of lanes the street should have",
        default=1,
        min=1,
        max=4,
        subtype='UNSIGNED',
    )

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# Registration
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Draw Street Object",
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
    OBJECT_OT_add_object()