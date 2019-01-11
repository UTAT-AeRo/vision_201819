# Author: Abdul. D`
# Purpose: Plot POIs on a file.
import json
import sys
import cv2 as cv
import numpy
import argparse

# https://docs.python.org/2/howto/argparse.html
_p = argparse.ArgumentParser()
_p.add_argument("-im", '--inputmap', type=str, help="The location/filename of the input map json file.", default="map.json");
_p.add_argument('-id', '--inputdamaged', type=str, help="The location/filanem of the damaged panels JSON file.", default="damaged.json");
_p.add_argument("-o", '--output', type=str, help="The output file name.", default="usc_utataero_....jpg");
_p.add_argument("-pi", '--pinimage', type=str, help="The file name of the marker image.", default="pinpoint.png");
_p.add_argument("-ps", '--pinscale', type=float, help="The scale you'd like for the pin image.", default=0.05);
_a = _p.parse_args();

# Terminology:
# im is the input map, id is the input damaged (json files)...

try:
	im_file = _a.inputmap;	
	im_json = None;
	with open(im_file, 'r') as f:
		im_json = json.load(f);			
except Exception as e:
	print('Could not open input map.');
	print(e);
	exit()
	
try:
	id_file = _a.inputdamaged;
	with open(id_file, 'r') as f:
		id_json = json.load(f);	
except Exception as e:
	print('Could not open input damaged.');
	print(e);
	exit()

try:
	output_file = _a.output;
	# todo
except Exception as e:
	print('Could not create output image.');
	print(e);
	exit()
	
try:
	pin_image = cv.imread(_a.pinimage, cv.IMREAD_UNCHANGED);
	pin_image = cv.resize(pin_image, (0,0), fx=_a.pinscale, fy=_a.pinscale);
	pin_image_width = pin_image.shape[1];
	pin_image_height = pin_image.shape[0];
	pin_image_alpha = pin_image[:,:,3] /255.0;	
	im_image_alpha = 1.0 - pin_image_alpha;
	print(pin_image_alpha.shape);
	print(im_image_alpha.shape);
	cv.imshow('',pin_image);
	cv.waitKey(0);		
except Exception as e:
	print('Could not lead and manipulate pin image.');
	print(e);
	exit();

print('Plot POIs Configuration Setup:');
print('-------------------------');
print('Map file:', im_file);
print('Damaged file:', id_file);
print('Output file:',output_file);
97
# Read the file into 
im_img = cv.imread(im_json['filename']);
im_imgsize = im_img.shape;
im_width = im_imgsize[1];
im_height = im_imgsize[0];

im_tl = im_json['topleft'];
im_br = im_json['bottomright'];
dx = im_br['long'] - im_tl['long'];
dy = im_tl['lat'] - im_br['lat'];

# For each coordinate position we have
for coords in id_json['damaged']:
	# place a marker 
	lat = coords['lat'];
	long = coords['long'];
	
	# pixel along x
	px = ((long - im_tl['long'])/dx) * im_width;
	py = ((im_tl['lat'] - lat)/dy) * im_height;
	
	# at x,y the image is drawn to the right and then bottom
	# So we go -width/2 and -height
	pxd = int(px - pin_image_width/2);
	pxd2 = int(pxd + pin_image_width);
	pyd = int(py - pin_image_height);
	pyd2 = int(pyd + pin_image_height);	
	for chan in range(0,3): 
		# we replace channels on the destination image..	
		im_img[pyd:pyd2,pxd:pxd2,chan] = (pin_image_alpha * pin_image[:, :, chan] + im_image_alpha * im_img[pyd:pyd2,pxd:pxd2,chan]);

							  
# output new image
cv.imwrite(output_file, im_img);