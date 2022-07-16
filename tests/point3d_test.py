# coding=utf-8
import pytest

from ladybug_geometry.geometry3d import Point3D, Vector3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug.color import Color
from ladybug_display.geometry3d.point import DisplayPoint3D


def test_display_point3d_init():
    """Test the initialization of DisplayPoint3D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = DisplayPoint3D(Point3D(0, 2, 0), grey)
    str(pt)  # test the string representation of the point

    assert pt.x == 0
    assert pt.y == 2
    assert pt.z == 0
    assert pt.color == grey
    assert pt[0] == 0
    assert pt[1] == 2
    assert pt[2] == 0

    pt_tuple = tuple(i for i in pt)
    assert pt_tuple == (0, 2, 0)


def test_display_point3d_to_from_dict():
    """Test the initialization of DisplayPoint3D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = DisplayPoint3D(Point3D(0, 2, 0), grey)
    pt_dict = pt.to_dict()
    new_pt = DisplayPoint3D.from_dict(pt_dict)
    assert isinstance(new_pt, DisplayPoint3D)
    assert new_pt.to_dict() == pt_dict


def test_move():
    """Test the DisplayPoint3D move method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint3D(Point3D(2, 2, 0), grey)
    vec_1 = Vector3D(0, 2, 2)
    pt_1.move(vec_1)
    assert pt_1.geometry == Point3D(2, 4, 2)


def test_scale():
    """Test the DisplayPoint3D scale method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint3D(Point3D(2, 2, 2), grey)
    origin_1 = Point3D(0, 2, 2)
    pt_1.scale(2, origin_1)
    assert pt_1.geometry == Point3D(4, 2, 2)


def test_scale_world_origin():
    """Test the DisplayPoint3D scale method with None origin."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint3D(Point3D(2, 2, 2), grey)
    pt_2 = DisplayPoint3D(Point3D(-2, -2, -2), grey)
    pt_1.scale(2)
    assert pt_1.geometry == Point3D(4, 4, 4)
    pt_2.scale(-2)
    assert pt_2.geometry == Point3D(4, 4, 4)


def test_rotate():
    """Test the DisplayPoint3D rotate method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint3D(Point3D(2, 2, 2), grey)
    axis_1 = Vector3D(-1, 0, 0)
    origin_1 = Point3D(0, 2, 0)

    pt_1.rotate(axis_1, 180, origin_1)
    assert pt_1.x == pytest.approx(2, rel=1e-3)
    assert pt_1.y == pytest.approx(2, rel=1e-3)
    assert pt_1.z == pytest.approx(-2, rel=1e-3)


def test_rotate_xy():
    """Test the Point3D rotate_xy method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint3D(Point3D(2, 2, -2), grey)
    origin_1 = Point3D(0, 2, 0)

    pt_1.rotate_xy(180, origin_1)
    assert pt_1.x == pytest.approx(-2, rel=1e-3)
    assert pt_1.y == pytest.approx(2, rel=1e-3)
    assert pt_1.z == -2


def test_reflect():
    """Test the Point3D reflect method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint3D(Point3D(2, 2, 2), grey)
    origin_1 = Point3D(0, 1, 0)
    normal_1 = Vector3D(0, 1, 0)
    plane = Plane(normal_1, origin_1)

    pt_1.reflect(plane)
    assert pt_1.geometry == Point3D(2, 0, 2)
