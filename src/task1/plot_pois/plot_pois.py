# Author: Abdul. D`
# Purpose: Plot POIs on a file.
import json
import sys
import cv2 as cv # IMPORTANT, I DO THIS BEACUSE I'M LAZY!
import argparse

# https://docs.python.org/2/howto/argparse.html
_p = argparse.ArgumentParser()
_p.add_argument("-im", '--inputmap', type=str, help="The location/filename of the input map json file.", default="map.json");
_p.add_argument('-id', '--inputdamaged', type=str, help="The location/filanem of the damaged panels JSON file.", default="damaged.json");
_p.add_argument("-o", '--output', type=str, help="The output file name.", default="usc_utataero_....jpg");
_a = _p.parse_args();

# Terminology:
# im is the input map, id is the input damaged (json files)...

try:
	im_file = _a.inputmap;	
	im_json = None;
	with open(im_file, 'r') as f:
		im_json = json.load(f);			
except e:
	print('Could not open input map.');
	print(e);
	exit()
	
try:
	id_file = _a.inputdamaged;
	with open(id_file, 'r') as f:
		id_json = json.load(f);	
except e:
	print('Could not open input damaged.');
	print(e);
	exit()

try:
	output_file = _a.output;
	# todo
except e:
	print('Could not create output image.');
	print(e);
	exit()

print('Plot POIs Configuration Setup:');
print('-------------------------');
print('Map file:', im_file);
print('Damaged file:', id_file);
print('Output file:',output_file);

im_img = cv.imread(im_json['filename']);
cv.imshow('image', im_img);	
cv.waitKey(0);

