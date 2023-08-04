import math
import bpy
import pathlib
import random

        

def build_geometry_node_tree(obj, walkway, lanes, scale):
    bpy.ops.node.new_geometry_nodes_modifier()

    if obj.modifiers[-1].node_group == None:
        return
    
    geo_node_tree = obj.modifiers[-1].node_group

    # define size of curve, depending on number of lanes and scale
    curve_size = 0
    if lanes == 1:
        curve_size = 1
    elif lanes == 2:
        curve_size = 1.5
    elif lanes == 3 or lanes == 4:
        curve_size = 3

    if walkway:
        curve_size = 1

    curve_size *= scale

    # get in and out nodes and set them apart from each other
    in_node = geo_node_tree.nodes["Group Input"]
    in_node.location.x = -1000.0
    out_node = geo_node_tree.nodes["Group Output"]
    out_node.location.x = 1000.0

    # initialize all needed geometry nodes
    spline_param_00_node: bpy.types.GeometryNodeSpline = create_geo_node(geo_node_tree, "GeometryNodeSplineParameter", -8.5, -200)
    store_named_attr_00_node = create_geo_node(geo_node_tree, "GeometryNodeStoreNamedAttribute", -8.0, 0)
    curve_line_node = create_geo_node(geo_node_tree, "GeometryNodeCurvePrimitiveLine", -6.0, -80)
    store_named_attr_01_node = create_geo_node(geo_node_tree, "GeometryNodeStoreNamedAttribute", -4.0, -150)
    spline_param_01_node = create_geo_node(geo_node_tree, "GeometryNodeSplineParameter", -4.0, -400)
    curve_to_mesh_node = create_geo_node(geo_node_tree, "GeometryNodeCurveToMesh", -1.0, 0)
    set_mat_node = create_geo_node(geo_node_tree, "GeometryNodeSetMaterial", 2.0, 0)
    set_pos_node = create_geo_node(geo_node_tree, "GeometryNodeSetPosition", 5.0, 0)

    # set input values of some nodes
    store_named_attr_00_node.inputs[2].default_value = 'Gradient X'
    store_named_attr_01_node.inputs[2].default_value = 'Gradient Y'
    curve_line_node.inputs[0].default_value = (-curve_size, 0, 0)
    curve_line_node.inputs[1].default_value = (curve_size, 0, 0)
    set_mat_node.inputs[2].default_value = create_road_material(walkway, lanes, scale)
    set_pos_node.inputs[3].default_value = (0, 0, 0.01)

    # trying to get the right indentifier for the outputs of Spline Parameter nodes
    spline_param_lookup = {socket.type: socket for socket in spline_param_00_node.outputs.values()}
    print(spline_param_lookup)

    # link all nodes together
    geo_node_tree.links.new(in_node.outputs[0], store_named_attr_00_node.inputs[0])
    geo_node_tree.links.new(spline_param_01_node.outputs['Length'], store_named_attr_00_node.inputs[3])
    geo_node_tree.links.new(store_named_attr_00_node.outputs[0], curve_to_mesh_node.inputs[0])
    geo_node_tree.links.new(curve_line_node.outputs[0], store_named_attr_01_node.inputs[0])
    geo_node_tree.links.new(spline_param_01_node.outputs['Factor'], store_named_attr_01_node.inputs[3])
    geo_node_tree.links.new(store_named_attr_01_node.outputs[0], curve_to_mesh_node.inputs[1])
    geo_node_tree.links.new(curve_to_mesh_node.outputs[0], set_mat_node.inputs[0])
    geo_node_tree.links.new(set_mat_node.outputs[0], set_pos_node.inputs[0])
    geo_node_tree.links.new(set_pos_node.outputs[0], out_node.inputs[0])

    print("set up node tree")


# function, that creates node tree and sets location -> cleaner code
def create_geo_node(node_tree, type_name, node_x_location, node_y_location):
    new_node = node_tree.nodes.new(type_name)
    new_node.location.x = node_x_location * 100.0
    new_node.location.y = node_y_location
    return new_node


# unique name, so there are not materials or node trees named the same
def set_unique_name(name):
    name += str(random.randrange(10000000))
    while bpy.data.materials.get(name):
        name = name + str(random.randrange(10000000))
    
    return name


# create a shader node tree for the material of the street
def create_road_material(walkway, lanes, scale):
    name = set_unique_name("RoadMaterial")
    road_mat = bpy.data.materials.new(name)
    road_mat.use_nodes = True
    nodes = road_mat.node_tree.nodes

    # get path to fitting image
    script_dir = get_script_dir()
    if walkway:
        imgpath = (script_dir / "textures/walk_path.jpg")
    else:
        if lanes == 1:
            imgpath = (script_dir / "textures/one_lane.jpg")
        elif lanes == 2:
            imgpath = (script_dir / "textures/two_lane.jpg")
        elif lanes == 3:
            imgpath = (script_dir / "textures/four_lane.png")
        elif lanes == 4:
            imgpath = (script_dir / "textures/four_lane.png")

    img = bpy.data.images.load(imgpath.__str__())

    # get divide value, fitting to road size
    divide_value = 0.0
    if lanes == 1 or lanes == 2:
        divide_value = 3.0 * scale
    elif lanes == 3 or lanes == 4:
        divide_value = 6.0 * scale

    # get and set all nodes
    principled_BSDF = nodes.get('Principled BSDF')
    attr_node_00 = nodes.new('ShaderNodeAttribute')
    attr_node_01 = nodes.new('ShaderNodeAttribute')
    combine_xyz_node = nodes.new('ShaderNodeCombineXYZ')
    divide_node = nodes.new('ShaderNodeVectorMath')
    tex_node: bpy.types.Node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img

    # set certain attributes
    attr_node_00.attribute_name = "Gradient X" # Gets the value of a GeometryNodeStoreNamedAttribute from the geometry node tree
    attr_node_01.attribute_name = "Gradient Y"
    divide_node.operation = 'DIVIDE'
    divide_node.inputs[1].default_value = (divide_value, 1.0, 1.0) # make texture not repeat too often
    
    road_mat.node_tree.links.new(attr_node_00.outputs[2], combine_xyz_node.inputs[0])
    road_mat.node_tree.links.new(attr_node_01.outputs[2], combine_xyz_node.inputs[1])
    road_mat.node_tree.links.new(combine_xyz_node.outputs[0], divide_node.inputs[0])
    road_mat.node_tree.links.new(divide_node.outputs[0], tex_node.inputs[0])
    road_mat.node_tree.links.new(tex_node.outputs[0], principled_BSDF.inputs[0])
    return road_mat


def set_origin_to_geometry_node_group():
    # https://blender.stackexchange.com/questions/247900/how-to-set-the-origin-of-a-procedurally-created-mesh-in-geometry-nodes
    return



# get parent directory, in this case the addons root directory
def get_script_dir(): 
    script_path = __file__
    script_dir = pathlib.Path(script_path).resolve().parent
    return script_dir


def covert_to_mesh(obj):
    mesh = bpy.data.meshes.new_from_object(obj)
    final_obj = bpy.data.objects.new(obj.name, mesh)
    final_obj.matrix_world = obj.matrix_world    
    return final_obj


def link_to_collection(obj):
    collection = bpy.data.collections.get('Collection')
    if (collection):
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)
    
    
def deselect_all_curves():
    # deselect all curves in the scene
    for curve in bpy.data.curves:
        for spline in curve.splines:
            
            if spline.type != 'BEZIER':
                print('only bezier splines allowed')
                continue
            
            total_points = len(spline.bezier_points)
            if total_points == 0:
                continue
            
            # Iterate over each point in the spline
            for point in spline.bezier_points:
                # deselect the points controls
                point.select_control_point = False
                point.select_left_handle = False
                point.select_right_handle = False