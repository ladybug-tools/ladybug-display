# coding=utf-8
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.ray import Ray3D
from ladybug.color import Color
from ladybug_display.geometry3d.ray import DisplayRay3D


def test_display_ray3d_init():
    """Test the initialization of Ray3D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    vec = Vector3D(0, 2, 0)
    ray = DisplayRay3D(Ray3D(pt, vec), grey)
    str(ray)  # test the string representation of the ray

    assert ray.color == grey
    assert ray.p == Point3D(2, 0, 2)
    assert ray.v == Vector3D(0, 2, 0)

    ray.reverse()
    assert ray.p == Point3D(2, 0, 2)
    assert ray.v == Vector3D(0, -2, 0)


def test_ray3_to_from_dict():
    """Test the to/from dict of Ray3D objects."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    vec = Vector3D(0, 2, 0)
    ray = DisplayRay3D(Ray3D(pt, vec), grey)
    ray_dict = ray.to_dict()
    new_ray = DisplayRay3D.from_dict(ray_dict)
    assert isinstance(new_ray, DisplayRay3D)
    assert new_ray.to_dict() == ray_dict
