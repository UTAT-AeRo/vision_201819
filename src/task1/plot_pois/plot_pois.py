# Author: Abdul. D`
# Purpose: Plot POIs on a file.
import json
import sys
import cv2 as cv
import numpy
import argparse
from scipy import stats
from numpy.polynomial import Polynomial as poly
from datetime import datetime as dt

# https://docs.python.org/2/howto/argparse.html
_p = argparse.ArgumentParser()
_p.add_argument("-im", '--inputmap', type=str, help="The location/filename of the input map json file. Default = map.json", default="map.json");
_p.add_argument('-id', '--inputdamaged', type=str, help="The location/filanem of the damaged panels JSON file. Default = damaged.json", default="damaged.json");
_p.add_argument("-o", '--output', type=str, help="The output file name. Default = usc_utataero_YYYYMMDD_HHMMSS.jpg", default="usc_utataero_" + dt.now().strftime('%Y%m%d_%H%M%S') + ".jpg");
_p.add_argument("-pi", '--pinimage', type=str, help="The file name of the marker image. Default = pinpoint.png", default="pinpoint.png");
_p.add_argument("-ps", '--pinscale', type=float, help="The scale you'd like for the pin image. Default = 0.05", default=0.05);
_p.add_argument("-fs", '--fontscale', type=float, help="The font size you'd like. Default = 1.0 ", default=1);
_p.add_argument("-ft", '--fontthickness', type=int, help="The font thickness you'd like. Default = 1 (integers only!)", default=1);
# TODO: font-positions
_a = _p.parse_args();

# Terminology:
# im is the input map, id is the input damaged (json files)...

try:
	im_file = _a.inputmap;
	im_json = None;
	with open(im_file, 'r') as f:
		im_json = json.load(f);
except Exception as e:
	print('Could not open input JSON file.');
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
except Exception as e:
	print('Could not load and manipulate pin image.');
	print(e);
	exit();

print('Plot POIs (v2) Configuration Setup:');
print('-------------------------');
print('Map file:', im_file);
print('Damaged file:', id_file);
print('Output file:',output_file);

# Read the file into
im_img = cv.imread(im_json['filename']);
im_imgsize = im_img.shape
im_width = im_imgsize[1]
im_height = im_imgsize[0]

# Construct a fit using the given points
# The region we are dealing with is small, each dimension is 6.65 millionth of the total radius @ 45deg latitude
# So assume that a linear fit is accurate, but our points have some error
# Thus, we do a linear regression
given_lats = []
given_x = []
given_longs = []
given_y = []
for point in im_json['points']:
	given_lats.append(point['lat']);
	given_x.append(point['x']);
	given_longs.append(point['long']);
	given_y.append(point['y']);
slope_x, intercept_x, r_value_x, p_value_x, std_err_x = stats.linregress(given_longs,given_x);
slope_y, intercept_y, r_value_y, p_value_y, std_err_y = stats.linregress(given_lats,given_y);
print(given_longs,given_x)
print(given_lats,given_y)
long2x = poly([intercept_x, slope_x])
lat2y = poly([intercept_y,slope_y])

# Now take thse GPs coordinates of the damaged panels and
for coords in id_json['damaged']:
	lat = coords['lat'];
	long = coords['long'];
	msg = coords['message'];

	# Convert them to their pixel values
	px = long2x(long)
	py = lat2y(lat)

	# at x,y the image is drawn to the right and then bottom
	# So we go -width/2 and -height
	pxd = max(0, int(px - pin_image_width/2));
	pxd2 = max(0, int(pxd + pin_image_width));
	pyd = max(0, int(py - pin_image_height));
	pyd2 = max(0, int(pyd + pin_image_height));

	for chan in range(0,3):
		# we replace channels on the destination image..
		im_img[pyd:pyd2,pxd:pxd2,chan] = (pin_image_alpha
										  *pin_image[:, :, chan]
										  +im_image_alpha
										  *im_img[pyd:pyd2,pxd:pxd2,chan])
		_size = cv.getTextSize(msg, cv.FONT_HERSHEY_PLAIN, _a.fontscale, _a.fontthickness);

	text_width = _size[0][0]
	text_x = int(px - text_width/2)
	text_y = pyd - 10

	# Center and place message
	cv.putText(im_img, msg, (text_x,text_y), cv.FONT_HERSHEY_PLAIN, _a.fontscale, (0,0,255),2, 8);

# output new image
cv.imwrite(output_file, im_img);
