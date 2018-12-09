"""This is the code to read and write .json files for this module
Input json should be formatted like this
{
    "focal_length": 50,
    "resolution": 200,
    "px_size": 40.0,
    "px_x": 57,
    "px_y": 81,
    "yaw": 89,
    "pitch": 50,
    "roll": 12,
    "lat": 37.0,
    "long": 124.561,
    "alt": 1000
}


focal_length (int): the focal length in mm.
sensor_resolution (int): the sensor resolution in pixels assumes
the sensor is square.
pixel_size (float): the pixel size of the camera in micrometers.

px_x, px_y (floats): the coordinates of the pixel from the top left in
the camera's reference frame.
yaw (floats): The yaw angle in degrees, for axis 3
pitch (float): The pitch angle in degrees, for axis 2
roll (float): The roll angle in degrees, for axis 1
lat (float): the latitude of the drone in degrees
long (float): the longditude of the drone in degrees
alt (float): the altitude of the drone above ground level in meters

Output jason will look like:
{
    "lat": 37.003745870740666,
    "long": 124.57474371010775
}

"""

import json
import sys
from projection import ImageProjection

command_line_args = sys.argv
print("writing data to" + command_line_args[1])

with open(command_line_args[1], 'r') as inputfile:
    input = json.load(inputfile)

if not (isinstance(input['focal_length'], int)
    and isinstance(input['resolution'], int)
    and isinstance(input['px_size'], float)
    and isinstance(input['px_x'], int)
    and isinstance(input['px_y'], int)
    and isinstance(input['yaw'], float)
    and isinstance(input['pitch'], float)
    and isinstance(input['roll'], float)
    and isinstance(input['lat'], float)
    and isinstance(input['long'], float)
    and isinstance(input['alt'], float)):
    raise TypeError

projector = ImageProjection(input['focal_length'], input['resolution'],
                            input['px_size'])

cords = projector.get_pixel_coords((input['px_x'],
                                   input['px_y']),
                                   input['yaw'], input['pitch'],
                                   input['roll'], input['lat'],
                                   input['long'],
                                   input['alt'])
output = dict()
output['lat'] = cords[0]
output['long'] = cords[1]
with open(command_line_args[2], 'w') as outfile:
    json.dump(output, outfile)
