"""This is a few tests for the projection code. I includes both property and unit test.
This is not intended to judge accurey just make sure nothing is
really broken"""

import pytest
from hypothesis import given
from hypothesis.strategies import floats
from projection import ImageProjection


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

    projector = ImageProjection(focal_length, resolution, px_size)
    # Here we test 4 points in the image to make sure they give the right
    # result.

    bottom_center_px = (100, 200)
    point_ned_bottom_center = project_ned(projector, bottom_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_bottom_center[0], 0, 0.01)            # North
    assert about(point_ned_bottom_center[1], 144.0761469, 0.01)  # East
    assert about(point_ned_bottom_center[2], 100, 0.01)          # Down

    top_center_px = (100, 0)
    point_ned_top_center = project_ned(projector, top_center_px, yaw, pitch, roll, altdrone)

    assert about(point_ned_top_center[0], 0, 0.01)         # North
    assert about(point_ned_top_center[1], 212.1612, 0.01)  # East
    assert about(point_ned_top_center[2], 100, 0.01)       # Down

    right_center_px = (200, 100)
    point_ned_right_center = project_ned(projector, right_center_px, yaw, pitch, roll, altdrone)

    # assert about(point_ned_right_center[0], -14.43375, 0.01)    # North
    assert about(point_ned_right_center[1], 173.2050808, 0.01)  # East
    assert about(point_ned_right_center[2], 100, 0.01)          # Down

    left_center_px = (0, 100)
    point_ned_left_center = project_ned(projector, left_center_px, yaw, pitch, roll, altdrone)

    # assert about(point_ned_left_center[0], 14.43375, 0.01)     # North
    assert about(point_ned_left_center[1], 173.2050808, 0.01)  # East
    assert about(point_ned_left_center[2], 100, 0.01)          # Down


@given(floats(min_value=-2000, max_value=2000), floats(min_value=-2000, max_value=2000),
       floats(min_value=0, max_value=2000), floats(min_value=-89, max_value=89), floats(min_value=-180, max_value=180))
def test_ned_to_geodetic(north, east, alt, lat, lon) -> None:
    """Here we make sure that for a given ned cords both versions of this function give the same result.
    """
    projector = ImageProjection()
    assert projector._ned_to_geodetic((north, east, -alt), lat, lon, alt) == \
           projector._ned_to_geodetic((north, east, -alt), lat, lon, alt, usepymap=False)


if __name__ == '__main__':
    import pytest
    pytest.main(['projection_tests.py'])
