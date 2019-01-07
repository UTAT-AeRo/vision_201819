import os
import argparse
import json

# Given a filepath and an output file, this program scans the given directory and outputs a json file similar to
#
#{
#  "positive": ["../common/test/2018-05-25_16-22-29-018.bmp", "../common/test/2018-05-25_16-22-29-685.bmp"]
#}
#
# for the ID Significant Changes module to use since its just IR Location module repurposed for identifying significant changes

# Set up the command line argument parsing
def define_args():
    parser = argparse.ArgumentParser(description='Detect broken solar panels')
    parser.add_argument('-i', '--input_dir', help='specify input directory', required=True)
    parser.add_argument('-o', '--output_file', help='specify output file', required=True)
    return parser.parse_args()

# Entry point for the program
def run(input_dir):
    pos_images = []
    for root, _, files in os.walk(input_dir):
        for f in files:
            rel_path = os.path.join(root, f)
            pos_images.append(os.path.abspath(rel_path))
    return pos_images

if __name__ == "__main__":
    args = define_args()
    input_dir = args.input_dir
    output_file = args.output_file
    assert os.path.exists(input_dir)

    # Get output positive images
    pos_images = run(input_dir)
    with open(output_file, 'w') as outfile:
        json.dump({"positive":pos_images}, outfile)