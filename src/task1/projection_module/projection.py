"""A package for UTAT Aero Vision Subsystem's Projection code

This module is based off of the slides from that UTATPayloadProcessing workshop,
and is aimed to provide a fully documented and easily usable package to handle all
the image projection code. Currently the processing pipeline is taken straight from
the slides, so if there are any errors it's likely because I made a mistake when copying
the code from the slides. This conforms to Python Style guidelines because maintainability
for future iterations of AeRo is a priority.
"""

import math as m
import numpy as np
import pymap3d as pymap


class ImageProjection:
    """The class to handle image and pixel conversions to GPS coordinates

    To use this class, first initialize it with the details of the camera (focal length, sensor resolution,
    pixel size). Note that it assumes the aspect ratio of the camera is square. Then, call get_pixel_coords with
    the angle and GPS coordinates of the drone and the pixel that you want to find the coordinates of.
    If it works as intended, it will find the coordinates of the pixel using the algorithm specified in the
    UTATPayloadProcessing workshop slides.

    I've split up the algorithm into multiple helper functions for ease of readability and also so that
    when someone (inevitably) finds a mistake it's easier to fix it.

    Attributes:
        GIVEN ATTRIBUTES
        focal_length (int): the focal length of the lens used in mm. Set to 50 by default for the
            Nikon AF NIKKOR 50mm lens
        sensor_resolution (int): the sensor resolution of the camera used in pixels. Set to 5120 by default for the
            Teledyne Dalsa Genie Nano XL C5100 Color
        pixel_size (int): the pixel size of the camera used in micrometers. Set to 4.5 by default for the
            Teledyne Dalsa Genie Nano XL C5100 Color

        CALCULATED ATTRIBUTES
        FOV (float): the FOV of the camera in degrees calculated using the arctan formula
        sensor_size (float): the sensor size of the camera in mm

    """

    def get_pixel_coords(self, pimg, yawangle, pitchangle, rollangle, latdrone, longdrone, altdrone):
        """Finds the coordinates of the specified pixel

        Given the angle and coordinates of the drone, the function finds the GPS coordinates
        of an arbitrary pixel in the image.

        Attributes:
            pimg (tuple of 2 floats): the coordinates of the pixel from the top left in the camera's reference frame.
            yawangle (float): The yaw angle in degrees, for axis 3
            pitchangle (float): The pitch angle in degrees, for axis 2
            rollangle (float): The roll angle in degrees, for axis 1
            latdrone (float): the latitude of the drone in degrees
            longdrone (float): the longditude of the drone in degrees
            altdrone (float): the altitude of the drone above ground level in meters

        Returns:
            3-tuple of GPS coords in the form (lat, long, alt)
        """
        if altdrone < 0:
            raise AltitudeError("Altitude should be positive")
        # Find coords of pixel in drone reference frame
        pdrone = self._imgref_to_droneref(pimg)
        # Find coords if pixel in earth reference frame
        pearth = self._droneref_to_earthref(pdrone, yawangle, pitchangle,
                                            rollangle)
        if pearth[2] < -altdrone: #TODO this needs more verification but seems alright
            raise OrientationError("Point is in the sky")

        # take the position of the pixel in the camera and project it to the ground.
        point_ned = self._project_to_ground(pearth, altdrone)

        # Get coords of pixel from vector in earth reference frame
        coords = self._ned_to_geodetic(point_ned, latdrone, longdrone, altdrone)
        return coords

    def _imgref_to_droneref(self, pimg):
        """Converts a pixel from the camera's reference frame to the drone's reference frame

        Given a pixel of the form [x, y], returns another pixel [x, y] but in the drones reference frame.
        This assumes that the relation between the camera coords and the drone coords are as described in
        slide 24

        Attributes:
             pimg (tuple of 2 floats): the coordinates of the pixel in the camera's reference frame

        Returns:
            A numpy array object representing the 3D vector of the pixel in the drone's reference frame,
            with attributes px, py, and fz
        """
        # Convert the given pixel to an array-like object for array operations
        pimg_vector = np.array(pimg)

        # The rotation matrix to convert the camera ref to the drone ref
        camera_rotation_array = np.array([[0, -1], [1, 0]])

        # The vector that will transform the image vector (taking it from the corner to the center)
        transform_vector = np.array([self.sensor_resolution / 2, self.sensor_resolution / 2])

        # First subtract the transform vector from the given pixel
        pimg_vector = np.subtract(pimg_vector, transform_vector)

        # Then multiply by the rotation matrix to rotate from camera coords to drone coords
        pdrone = camera_rotation_array.dot(pimg_vector)

        # Finally, calculate the 'vertical distance' using the focal length and pixel size
        # NOTE: I am converting everything to meters first to keep the units consistent
        fz = ((self.focal_length * 0.001) / (self.pixel_size * 0.000001))

        pdrone = np.append(pdrone, fz)

        return pdrone

    def _droneref_to_earthref(self, pdrone, yaw, pitch, roll):
        """Converts a vector representing a pixel in the drone reference frame to the earth reference frame

        Given pdrone, a numpy 3D array representing a pixel in the drone reference frame,
        this functiin will use the rotation matrix derived from the Euler angles to find and
        return the vector in the earth reference frame. Note that in this case the earth reference frame
        is considered to be the NED inertial frame.

        Attributes:
            pdrone (numpy array object): The vector to the pixel in the drone reference frame
            yaw (float): The yaw angle in degrees, for axis 3
            pitch (float): The pitch angle in degrees, for axis 2
            roll (float): The roll angle in degrees, for axis 1

        Returns:
            The numpy array object representing the same vector in the earth reference frame
        """

        # Convert angles to radians because math module uses radians
        yaw = m.radians(yaw)
        pitch = m.radians(pitch)
        roll = m.radians(roll)

        # Attempt to copy the rotation matrix to convert from drone reference to earth reference on slide 25
        # This is actualy the earth to drone rotation matrix we need to transpose it to get what we want.
        earth_drone_rotation = np.array([[m.cos(pitch) * m.cos(yaw),
                                         m.cos(pitch) * m.sin(yaw),
                                         -1 * m.sin(pitch)
                                         ],
                                        [m.sin(roll) * m.sin(pitch) * m.cos(yaw) - m.cos(roll) * m.sin(yaw),
                                         m.sin(roll) * m.sin(pitch) * m.sin(yaw) + m.cos(roll) * m.cos(yaw),
                                         m.cos(pitch) * m.sin(roll)
                                         ],
                                        [m.cos(roll) * m.sin(pitch) * m.cos(yaw) + m.sin(roll) * m.sin(yaw),
                                         m.cos(roll) * m.sin(pitch) * m.sin(yaw) - m.sin(roll) * m.cos(yaw),
                                         m.cos(pitch) * m.cos(roll)
                                         ]]
                                       )

        drone_earth_rotation = np.transpose(earth_drone_rotation)

        # Uncomment for error checking
        # if np.linalg.det(drone_earthrotation) != 1:
        #     print("ERROR - THE ROTATION MATRIX IS INCORRECT - DETERMINANT SHOULD BE 1 BUT IT IS" +
        # np.linalg.det(drone_earthrotation))

        return drone_earth_rotation.dot(pdrone)

    def _project_to_ground(self, pearth, altdrone):
        """Takes position of pixel within the 'camera' in earths frame of
        refrence and projects in to ground as described in slide 26.

        Attributes
            pearth (numpy array object): the vector to the pixel in the earth reference frame
            altdrone (float): the altitude of the drone in meters

        Returns
            A numpy array containing the position of the point on the ground in
            NED cordenats relative to the drone.

        """

        # Find scaled vector to project to ground
        scaling_factor = altdrone / pearth[2]
        point_pos_ned = scaling_factor * pearth

        return point_pos_ned

    def _ned_to_geodetic(self, point_ned, latdrone, longdrone, altdrone):
        """Find the GPS coordinates of the point on the ground in (NED)

        Given the vector to the point on in the ground in earth reference frame (NED), this finds and returns the
        GPS coordinates (geodetic coordinate system). I added the ability to either use the built in method
        from pymap3d or to use the formula and the method given on slide 28 and the formula from the GPS
        website.

        Attributes:
            point_ned (numpy array object): the vector to the point in the earth reference frame
            latdrone (float): the latitude of the drone in degrees
            longdrone (float): the longditude of the drone in degrees
            altdrone (float): the altitude of the drone in meters
            usepymap (bool): whether to calculate using the pymap3d library or with the formula

        Returns:
            3-tuple of GPS coords in the form (lat, long, alt). NOTE: alt should always be 0
            if the function works correctly since the point is projected onto the ground
        """

        return pymap.ned2geodetic(point_ned[0], point_ned[1], point_ned[2], latdrone, longdrone, altdrone)

    def _calculate_fov(self, focal_length, sensor_size):
        """Calculates the fov of a camera given its focal length and sensor size

        This uses the formula on slide 11, stating that
            FOV = 2*arctan((0.5*sensor_size)/(focal_length))

        Args:
            focal_length (float): the focal length of the lens
            sensor_size (float): the sensor size of the camera

        Returns:
            An float corresponding to the fov in degrees
        """

        # Calulates with the formula and converts the result to degrees
        return m.degrees(2 * m.atan((0.5 * sensor_size) / focal_length))

    def _calculate_sensor_size(self, sensor_resolution, pixel_size):
        """Calculates the sensor size of a camera from its resultion and pixel size

        Uses the formula on slide 11, stating that
            sensor_size = sensor_resolution*pixel_size

        Attributes:
            sensor_resolution (float): the sensor resolution in pixels
            pixel_size (float): the pixel size of the camera in micrometers

        Returns:
            the sensor size of the camera in mm
        """

        # Divide by 1000 to convert from micrometers to mm
        return sensor_resolution * (pixel_size / 1000)

    def __init__(self, focal_length=35, sensor_resolution=5120, pixel_size=4.5):
        """initializes all relevant variables by calculating using the given variables

        Args:
            focal_length (int): the focal length in mm if using a different lens than the Nikon AF NIKKOR 50mm
            sensor_resolution (int): the sensor resolution in pixels if using a different camera than
                the Teledyne Dalsa Genie Nano XL C5100 Color. Also assumes the sensor is square.
            pixel_size (float): the pixel size of the camera in micrometers if using a different camera than
                the Teledyne Dalsa Genie Nano XL C5100 Color
        """
        # Sets the given focal length and sensor size variables
        self.focal_length = focal_length
        self.sensor_resolution = sensor_resolution
        self.pixel_size = pixel_size

        self.sensor_size = self._calculate_sensor_size(self.sensor_resolution, self.pixel_size)
        self.FOV = self._calculate_fov(self.focal_length, self.sensor_size)

class AltitudeError(ValueError):
    pass

class OrientationError(ValueError):
    pass
