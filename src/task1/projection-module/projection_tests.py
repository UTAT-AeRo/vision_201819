"""This is a few tests for the projection code. I includes both property and unit test.
This is not intended to judge accurey just make sure nothing is
really broken"""

import pytest
from hypothesis import given
from hypothesis.strategies import floats
from projection import ImageProjection
import math as m
import numpy as np


def about(num1, num2, range) -> bool:
    """Return true if num1 is range close to num2"""
    return abs(num1 - num2) < range


def project_ned(projector: ImageProjection, pimg: tuple, yaw, pitch, roll, altdrone):
    """gets position of pixle on the ground in ned"""
    pdrone = projector._imgref_to_droneref(pimg)
    pearth = projector._droneref_to_earthref(pdrone, yaw, pitch, roll)
    return projector._project_to_ground(pearth, altdrone)


def test_due_east() -> None:
    """This test assumes that the drone is pointing due east.
    It checks 4 points: bottom_center, top-center, right_center and left_center
    """
    focal_length = 60.0  # mm
    resolution = 200.0  # px (the program assumes a square sensor)
    px_size = 50.0  # micrometers
    yaw = 90  # degrees
    pitch = 60  # degrees
    roll = 0  # degrees (since pitch and roll trade
    # functions after a 90 degree rotation)
    altdrone = 100  # meters

    tol = 0.00001   # This is the tolerance for the test. It is in place simply to avoid problems with rounding errors.

    projector = ImageProjection(focal_length, resolution, px_size)

    sensor_size = resolution * (px_size / 1000)

    assert sensor_size == projector._calculate_sensor_size(resolution, px_size)

    fov = 2 * m.atan((sensor_size/2) / focal_length)

    assert m.degrees(fov) == projector._calculate_fov(focal_length, sensor_size)

    pitch_r = m.radians(pitch)

    # Here we test 4 points in the image to make sure they give the right
    # result.

    bottom_center_px = (100, 200)
    point_ned_bottom_center = project_ned(projector, bottom_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_bottom_center[0], 0, tol)                            # North
    assert about(point_ned_bottom_center[1], altdrone*m.tan(pitch_r - fov / 2), tol)  # East
    assert about(point_ned_bottom_center[2], altdrone, tol)                     # Down

    top_center_px = (100, 0)
    point_ned_top_center = project_ned(projector, top_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_top_center[0], 0, tol)                            # North
    assert about(point_ned_top_center[1], altdrone*m.tan(pitch_r + fov / 2), tol)  # East
    assert about(point_ned_top_center[2], altdrone, tol)                     # Down

    right_center_px = (200, 100)
    point_ned_right_center = project_ned(projector, right_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_right_center[0], -(altdrone / m.cos(pitch_r)) * m.tan(fov / 2), tol)  # North
    assert about(point_ned_right_center[1], altdrone * m.tan(pitch_r), tol)                  # East
    assert about(point_ned_right_center[2], altdrone, tol)                                 # Down

    left_center_px = (0, 100)
    point_ned_left_center = project_ned(projector, left_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_left_center[0], (altdrone / m.cos(pitch_r)) * m.tan(fov / 2), tol)   # North
    assert about(point_ned_left_center[1], altdrone * m.tan(pitch_r), tol)                  # East
    assert about(point_ned_left_center[2], altdrone, tol)                                      # Down


# @given(floats(min_value=1500, max_value=2000),  # north
#        floats(min_value=1500, max_value=2000),  # east
#        floats(min_value=13, max_value=2000),  # alt
#        floats(min_value=34, max_value=40),  # lat
#        floats(min_value=135, max_value=136))  # lon
# def test_ned_to_geodetic(north, east, alt, lat, lon) -> None:
#     """Here we make sure that for a given ned cords both versions of this function give the same result.
#     """
#     if about(lat, 0, 0.2) or about(lon, 0, 0.2):
#         return
#
#     projector = ImageProjection()
#     cords_pymap = projector._ned_to_geodetic((north, east, -alt), lat, lon, alt)
#     cords_home = projector._ned_to_geodetic((north, east, -alt), lat, lon, alt, usepymap=False)
#
#     assert about(cords_home[0], cords_pymap[0], 0.001)  # lat
#     assert about(cords_home[1], cords_pymap[1], 0.001)  # lon
#     assert about(cords_home[2], cords_pymap[2], 0.001)  # alt

if __name__ == '__main__':
    import pytest
    pytest.main(['projection_tests.py'])
