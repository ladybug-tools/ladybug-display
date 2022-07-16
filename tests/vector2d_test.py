# coding=utf-8
import pytest

from ladybug_geometry.geometry2d import Vector2D
from ladybug.color import Color
from ladybug_display.geometry2d.vector import DisplayVector2D


def test_display_vector2d_init():
    """Test the initialization of DisplayVector2D objects and basic properties."""
    grey = Color(100, 100, 100)
    vec = DisplayVector2D(Vector2D(0, 2), grey)
    str(vec)  # test the string representation of the vector

    assert vec.x == 0
    assert vec.y == 2
    assert vec.color == grey
    assert vec[0] == 0
    assert vec[1] == 2
    assert vec.magnitude == 2

    pt_tuple = tuple(i for i in vec)
    assert pt_tuple == (0, 2)

    vec.normalize()
    assert vec.x == 0
    assert vec.magnitude == 1

    norm_vec = vec * 3
    assert norm_vec.magnitude == 3


def test_display_vector2d_to_from_dict():
    """Test the initialization of DisplayVector2D objects and basic properties."""
    grey = Color(100, 100, 100)
    vec = DisplayVector2D(Vector2D(0, 2), grey)
    vec_dict = vec.to_dict()
    new_vec = DisplayVector2D.from_dict(vec_dict)
    assert isinstance(new_vec, DisplayVector2D)
    assert new_vec.to_dict() == vec_dict


def test_display_vector2d_angle():
    """Test the methods that get the angle between DisplayVector2D objects."""
    grey = Color(100, 100, 100)
    vec_1 = DisplayVector2D(Vector2D(0, 2), grey)
    vec_2 = DisplayVector2D(Vector2D(2, 0), grey)
    vec_3 = DisplayVector2D(Vector2D(0, -2), grey)
    vec_4 = DisplayVector2D(Vector2D(-2, 0), grey)
    assert vec_1.angle(vec_2) == pytest.approx(90, rel=1e-3)
    assert vec_1.angle(vec_3) == pytest.approx(180, rel=1e-3)
    assert vec_1.angle(vec_4) == pytest.approx(90, rel=1e-3)
    assert vec_1.angle(vec_1) == pytest.approx(0, rel=1e-3)
