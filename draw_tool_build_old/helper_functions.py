import math
import bpy
import pathlib
import random


def define_control_points(start, end, spline):
    # get step-size to distribute control points evenly between start and end
    distance = end - start
    step_size = distance / (len(spline.bezier_points) - 1)

    handle_offset = step_size / 7

    # Set control points for curve
    for i in range(len(spline.bezier_points)):
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
            
        

def assign_road_material(walkway, lanes):
    mat_name = set_unique_mat_name("RoadMaterial")
    print(mat_name)
    road_mat = bpy.data.materials.new(mat_name)
    road_mat.use_nodes = True
    nodes = road_mat.node_tree.nodes

    # clear node tree
    for node in nodes:
        nodes.remove(node)

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

    # build node tree
    output = nodes.new(type = 'ShaderNodeOutputMaterial')
    diffuse = nodes.new(type = 'ShaderNodeBsdfDiffuse' )
    tex_node: bpy.types.Node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_mapping: bpy.types.ShaderNodeMapping = nodes.new(type='ShaderNodeMapping')
    tex_mapping.vector_type = 'TEXTURE'
    tex_mapping.inputs[3].default_value = (0.01, 1.0, 1.0)

    # link it all together
    links = road_mat.node_tree.links
    links.new(tex_coord.outputs["UV"], tex_mapping.inputs["Vector"])
    links.new(tex_mapping.outputs["Vector"], tex_node.inputs["Vector"])
    links.new(tex_node.outputs[0], diffuse.inputs[0])
    links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )

    # append to active object
    bpy.context.object.data.materials.append(road_mat)



# get parent directory, in this case the addons root directory
def get_script_dir(): 
    script_path = __file__
    script_dir = pathlib.Path(script_path).resolve().parent
    return script_dir


def set_unique_mat_name(name):
    name += str(random.randrange(10000000))
    while bpy.data.materials.get(name):
        name = name + str(random.randrange(10000000))
    
    return name


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


def get_unit_vec(start, end, factor):
    vec = end - start
    vec_len = math.sqrt(math.pow(vec.x, 2) +
                        math.pow(vec.y, 2)+math.pow(vec.z, 2))
    if (vec_len == 0):
        return (0, 0, 0)
    else:
        unit_vec = vec / vec_len
        return unit_vec*factor
    

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