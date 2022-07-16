# coding=utf-8
import pytest

from ladybug_geometry.geometry3d import Vector3D
from ladybug.color import Color
from ladybug_display.geometry3d.vector import DisplayVector3D


def test_display_vector3d_init():
    """Test the initialization of DisplayVector3D objects and basic properties."""
    grey = Color(100, 100, 100)
    vec = DisplayVector3D(Vector3D(0, 2, 0), grey)
    str(vec)  # test the string representation of the vector

    assert vec.x == 0
    assert vec.y == 2
    assert vec.z == 0
    assert vec.color == grey
    assert vec[0] == 0
    assert vec[1] == 2
    assert vec[2] == 0
    assert vec.magnitude == 2

    pt_tuple = tuple(i for i in vec)
    assert pt_tuple == (0, 2, 0)

    vec.normalize()
    assert vec.x == 0
    assert vec.z == 0
    assert vec.magnitude == 1

    norm_vec = vec * 3
    assert norm_vec.magnitude == 3


def test_display_vector3d_to_from_dict():
    """Test the initialization of DisplayVector3D objects and basic properties."""
    grey = Color(100, 100, 100)
    vec = DisplayVector3D(Vector3D(0, 2, 0), grey)
    vec_dict = vec.to_dict()
    new_vec = DisplayVector3D.from_dict(vec_dict)
    assert isinstance(new_vec, DisplayVector3D)
    assert new_vec.to_dict() == vec_dict


def test_display_vector3d_angle():
    """Test the methods that get the angle between DisplayVector3D objects."""
    grey = Color(100, 100, 100)
    vec_1 = DisplayVector3D(Vector3D(0, 2, 0), grey)
    vec_2 = DisplayVector3D(Vector3D(2, 0, 0), grey)
    vec_3 = DisplayVector3D(Vector3D(0, -2, 0), grey)
    vec_4 = DisplayVector3D(Vector3D(-2, 0, 0), grey)
    vec_5 = DisplayVector3D(Vector3D(0, 0, 2), grey)
    vec_6 = DisplayVector3D(Vector3D(0, 0, -2), grey)
    assert vec_1.angle(vec_2) == pytest.approx(90, rel=1e-3)
    assert vec_1.angle(vec_3) == pytest.approx(180, rel=1e-3)
    assert vec_1.angle(vec_4) == pytest.approx(90, rel=1e-3)
    assert vec_1.angle(vec_5) == pytest.approx(90, rel=1e-3)
    assert vec_5.angle(vec_6) == pytest.approx(180, rel=1e-3)
    assert vec_1.angle(vec_1) == pytest.approx(0, rel=1e-3)
