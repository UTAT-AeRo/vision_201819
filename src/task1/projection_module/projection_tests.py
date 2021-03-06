"""This is a few tests for the projection code. It currently only includes unit test for project to ned.
"""

import pytest
from projection import ImageProjection, AltitudeError, OrientationError
import math as m
from unittest import TestCase


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

    fov = 2 * m.atan((sensor_size / 2) / focal_length)

    assert m.degrees(fov) == projector._calculate_fov(focal_length, sensor_size)

    pitch_r = m.radians(pitch)

    # Here we test 4 points in the image to make sure they give the right
    # result.

    bottom_center_px = (100, 200)
    point_ned_bottom_center = project_ned(projector, bottom_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_bottom_center[0], 0, tol)  # North
    assert about(point_ned_bottom_center[1], altdrone * m.tan(pitch_r - fov / 2), tol)  # East
    assert about(point_ned_bottom_center[2], altdrone, tol)  # Down

    top_center_px = (100, 0)
    point_ned_top_center = project_ned(projector, top_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_top_center[0], 0, tol)  # North
    assert about(point_ned_top_center[1], altdrone*m.tan(pitch_r + fov / 2), tol)  # East
    assert about(point_ned_top_center[2], altdrone, tol)  # Down

    right_center_px = (200, 100)
    point_ned_right_center = project_ned(projector, right_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_right_center[0], -(altdrone / m.cos(pitch_r)) * m.tan(fov / 2), tol)  # North
    assert about(point_ned_right_center[1], altdrone * m.tan(pitch_r), tol)  # East
    assert about(point_ned_right_center[2], altdrone, tol)  # Down

    left_center_px = (0, 100)
    point_ned_left_center = project_ned(projector, left_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_left_center[0], (altdrone / m.cos(pitch_r)) * m.tan(fov / 2), tol)   # North
    assert about(point_ned_left_center[1], altdrone * m.tan(pitch_r), tol)  # East
    assert about(point_ned_left_center[2], altdrone, tol)  # Down


def test_out_of_bounds():
    projector = ImageProjection()
    with pytest.raises(OrientationError):
        projector.get_pixel_coords((0, 0), 0, 0, 180, 0, 0, 10)
    with pytest.raises(AltitudeError):
        projector.get_pixel_coords((0, 0), 0, 0, 0, 0, 0, -10)



if __name__ == '__main__':
    pytest.main(['projection_tests.py'])
