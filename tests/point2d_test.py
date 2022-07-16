# coding=utf-8
import pytest

from ladybug_geometry.geometry2d import Point2D, Vector2D
from ladybug.color import Color
from ladybug_display.geometry2d.point import DisplayPoint2D


def test_display_point2d_init():
    """Test the initialization of DisplayPoint2D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = DisplayPoint2D(Point2D(0, 2), grey)
    str(pt)  # test the string representation of the point

    assert pt.x == 0
    assert pt.y == 2
    assert pt.color == grey
    assert pt[0] == 0
    assert pt[1] == 2

    pt_tuple = tuple(i for i in pt)
    assert pt_tuple == (0, 2)


def test_display_point2d_to_from_dict():
    """Test the initialization of DisplayPoint2D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = DisplayPoint2D(Point2D(0, 2), grey)
    pt_dict = pt.to_dict()
    new_pt = DisplayPoint2D.from_dict(pt_dict)
    assert isinstance(new_pt, DisplayPoint2D)
    assert new_pt.to_dict() == pt_dict


def test_move():
    """Test the DisplayPoint2D move method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint2D(Point2D(2, 2), grey)
    vec_1 = Vector2D(0, 2)
    pt_1.move(vec_1)
    assert pt_1.geometry == Point2D(2, 4)


def test_scale():
    """Test the DisplayPoint2D scale method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint2D(Point2D(2, 2), grey)
    origin_1 = Point2D(0, 2)
    pt_1.scale(2, origin_1)
    assert pt_1.geometry == Point2D(4, 2)


def test_scale_world_origin():
    """Test the DisplayPoint2D scale method with None origin."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint2D(Point2D(2, 2), grey)
    pt_2 = DisplayPoint2D(Point2D(-2, -2), grey)
    pt_1.scale(2)
    assert pt_1.geometry == Point2D(4, 4)
    pt_2.scale(-2)
    assert pt_2.geometry == Point2D(4, 4)


def test_rotate():
    """Test the Point2D rotate_xy method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint2D(Point2D(2, 2), grey)
    origin_1 = Point2D(0, 2)

    pt_1.rotate(180, origin_1)
    assert pt_1.x == pytest.approx(-2, rel=1e-3)
    assert pt_1.y == pytest.approx(2, rel=1e-3)


def test_reflect():
    """Test the Point2D reflect method."""
    grey = Color(100, 100, 100)
    pt_1 = DisplayPoint2D(Point2D(2, 2), grey)
    origin_1 = Point2D(0, 1)
    normal_1 = Vector2D(0, 1)

    pt_1.reflect(normal_1, origin_1)
    assert pt_1.geometry == Point2D(2, 0)
