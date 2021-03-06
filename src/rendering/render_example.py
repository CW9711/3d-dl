# usage: python rendering/render_example.py

import site
import os
import subprocess
import pathlib
import sys
import json


# Ensure source directory is in python path
src_dir = str(pathlib.Path(__file__).parents[1].resolve())
sys.path.append(os.path.join(src_dir))

# print(src_dir)
object_folder = '/vol/project/2017/530/g1753002/max/render_workspace/object_files/two_set'
output_folder = '/vol/project/2017/530/g1753002/max/render_workspace/object_poses/out'


blender_attributes = {
    "attribute_distribution_params": [["num_lamps","mid", 6], ["num_lamps","scale", 0.4], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
    "attribute_distribution" : []
}
# "attribute_distribution" : [["lamp_energy", {"dist":"UniformD","l":2000.0,"r":2400.0}]]


def generate_poses(object_folder, output_folder, renders_per_product, blender_attributes):
    "Make a call to Blender to generate poses"
    # python_sites = site.getsitepackages()[0]
    # python_sites = '/vol/project/2017/530/g1753002/ocadovenv/ocadovenv/lib/python3.5/site-packages'

    blender_path = '/vol/project/2017/530/g1753002/Blender/blender-2.79-linux-glibc219-x86_64/blender'
    blender_script_path = os.path.join(src_dir, 'rendering', 'render_poses.py')
    config_file_path = os.path.join(src_dir, 'rendering', 'config.json')

    blender_args = [blender_path, '--background', '--python', blender_script_path, '--',
                    src_dir,
                    # config_file_path,
                    object_folder,
                    output_folder,
                    str(renders_per_product),
                    json.dumps(blender_attributes)]

    # blender_args = [blender_path, '--background', '--python']

    print('Rendering...')
    subprocess.check_call(blender_args)
    print('Rendering done!')

generate_poses(object_folder, output_folder, 2);

# """ --------------- Run blender tests ------------- """
# if args.blender_tests:
#     blender_script_dir = os.path.join(project_dir, 'test', 'test_blender.py')
#     blender_args = ['blender', '--background', '--python', blender_script_dir,
#                     '--', project_dir, site.getsitepackages()[0], str(args.report_branch)]
#
#     print('Running Blender tests')
#     subprocess.check_call(blender_args)
#     print('Blender tests complete')




