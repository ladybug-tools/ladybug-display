# coding=utf-8
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.plane import Plane

from ladybug.color import Color
from ladybug_display.geometry3d.plane import DisplayPlane


def test_plane_init():
    """Test the initialization of Plane objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    vec = Vector3D(0, 2, 0)
    plane = DisplayPlane(Plane(vec, pt), grey)
    str(plane)  # test the string representation

    assert not plane.show_axes
    assert not plane.show_grid
    assert plane.o == Point3D(2, 0, 2)
    assert plane.n == Vector3D(0, 1, 0)
    assert plane.x == Vector3D(1, 0, 0)
    assert plane.y == Vector3D(0, 0, -1)
    assert plane.k == 0

    blue = Color(0, 0, 100)
    plane.color = blue
    plane.show_axes = True
    plane.show_grid = True
    assert plane.color == blue
    assert plane.show_axes
    assert plane.show_grid


def test_plane_to_from_dict():
    """Test the initialization of Plane objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    vec = Vector3D(0, 2, 0)
    plane = DisplayPlane(Plane(vec, pt), grey)
    plane.show_axes = True
    plane.show_grid = True
    plane_dict = plane.to_dict()
    new_plane = DisplayPlane.from_dict(plane_dict)
    assert isinstance(new_plane, DisplayPlane)
    assert new_plane.to_dict() == plane_dict
