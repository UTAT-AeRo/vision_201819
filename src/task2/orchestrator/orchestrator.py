"""This is the task 2 orcastrator it should be called from the directory it is
in."""
import os
from os.path import join, dirname, abspath
import sys
import json

# ================= CONSTANTS ==================================================
IMAGE_FORMATS = ('.bmp', '.jpg', '.png')

# ==============================================================================
# checking input
if len(sys.argv) <= 2:
    raise FileNotFoundError("must specify input and output folder")

input_folder = sys.argv[1]
output_folder = sys.argv[2]

# making needed dirs
script_path = dirname(os.path.realpath(__file__))
temp_path = join(script_path, 'temp')

if not os.path.exists(temp_path):
    os.makedirs(temp_path)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

paths_to_all = [abspath(join(input_folder, filename))
                for filename in os.listdir(input_folder)]

paths_to_all_images = [path for path in paths_to_all
                       if path.lower().endswith(IMAGE_FORMATS)]

json_for_images = []
for path_to_image in paths_to_all_images:
    image_entry = dict()
    image_entry["file"] = path_to_image
    image_entry["gps"] = []
    image_entry["pixels"] = []
    json_for_images.append(image_entry)

input_json_path = join(temp_path, 'input_images.json')
with open(input_json_path, 'w') as input_json:
    json.dump(json_for_images, input_json)

path_to_image_flattener = join(join(script_path, os.pardir),
                               join('flattening_module', 'imageflattener.py'))

path_to_damageselector = join(join(script_path, os.pardir),
                               join('damage_selection_gui', 'damageselector.py'))

os.system(f'python {path_to_image_flattener} --input {input_json_path}\
            --output {temp_path}')

os.system(f'python {path_to_damageselector} \
            --input {join(temp_path, "result.json")} \
            --output {output_folder}')

