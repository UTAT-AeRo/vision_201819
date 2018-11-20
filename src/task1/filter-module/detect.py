import cv2
import imutils
from imutils import contours
import os
import argparse
import json

# Show image (for debugging)
def show_img(image):
    cv2.imshow('img',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Detect whether there exists a spot bright enough
def process_img(file_name):
    image = cv2.imread(file_name)
    smoothed_image = cv2.bilateralFilter(image, 20, 50, 200)
    gray = cv2.cvtColor(smoothed_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=4)
    thresh = cv2.erode(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    if len(cnts) > 0:
        cnts = contours.sort_contours(cnts)[0]
        for (i, c) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(cX), int(cY)), int(radius),
                       (0, 0, 255), 2)
        return image
    return None

# Set up the command line argument parsing
def define_args():
    parser = argparse.ArgumentParser(description='Detect broken solar panels')
    parser.add_argument('-i', '--input_dir', help='specify input directory', required=True)
    parser.add_argument('-f', '--output_file', help='specify output file', required=True)
    parser.add_argument('-o', '--output_dir', help='specify output directory', required=False)
    return parser.parse_args()

# Entry point for the program
def run(input_dir, output_dir):
    pos_images = []
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            rel_path = os.path.join(root, f)
            rel_out_path = None
            if output_dir is not None:
                rel_out_path = os.path.join(output_dir, f)
            img = process_img(rel_path)
            if img is not None:
                pos_images.append(f)
                if rel_out_path is not None:
                    cv2.imwrite(rel_out_path, img)
    return pos_images

# Run
args = define_args()
input_dir = args.input_dir
output_dir = args.output_dir
output_file = args.output_file
assert input_dir != output_dir
assert os.path.exists(input_dir)
if output_dir is not None and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get output positive images
pos_images = run(input_dir, output_dir)
with open(output_file, 'w', encoding='utf8') as outfile:
    json.dump(pos_images, outfile)