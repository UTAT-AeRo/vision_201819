Projection Module
---
# Description
This module is intended to be used as an API for any program that needs to get the GPS coordinates of a pixel in an image taken by the drone

# Prerequisites
- Python 3 with following modules (just use pip install):
  - numpy
  - pymap3d

# Usage
The following will detail an example usage of the projection module:

First, create an ImageProjection object by calling the class in the code. It requires the camera extrinsics, specifically focal length in mm, sensor resolution in pixels, and pixel size in micrometers of the camera; if nothing is given it will assume the extrinsics of the Teledyne Dalsa Genie Nano XL C5100 Color camera and Nikon AF NIKKOR 50mm lens.

```python 
projectionCalculator = ImageProjection(focal_length=50, sensor_resolution=5120, pixel_size=4.5) 
```

Then, whenever the GPS coordinates of a specific pixel is needed, call the `get_pixel_coords` function with drone intrinsics such as location and angle, and the pixel that you want to find the location of. 

For example, to find the coordinates of the pixel at `x=2000` and `y=3000` in the image, while the drone has latitude `57.2837 degrees`, longditude `103.2817364 degrees`, altitude `50m`, and yaw, pitch, and roll of `5`, `21`, and `13` degrees respectively (btw I completely made up these numbers they're probably not realistic at all):

```python
imageCoords = projectionCalculator.get_pixel_coords(pimg=(2000, 3000), yawangle=5, pitchangle=21, rollangle=13, latdrone=57.2837, longdrone=57.2837, altdrone=50)
```

`imageCoords` would then be a 3-tuple of the GPS coordinates of the pixel given.
