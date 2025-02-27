# coding=utf-8
from ladybug_geometry.geometry2d.pointvector import Point2D, Vector2D
from ladybug_geometry.geometry2d.ray import Ray2D
from ladybug.color import Color
from ladybug_display.geometry2d.ray import DisplayRay2D


def test_display_ray2d_init():
    """Test the initialization of Ray2D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point2D(2, 0)
    vec = Vector2D(0, 2)
    ray = DisplayRay2D(Ray2D(pt, vec), grey)
    str(ray)  # test the string representation of the ray

    assert ray.color == grey
    assert ray.p == Point2D(2, 0)
    assert ray.v == Vector2D(0, 2)

    ray.reverse()
    assert ray.p == Point2D(2, 0)
    assert ray.v == Vector2D(0, -2)


def test_display_ray2d_to_from_dict():
    """Test the to/from dict of Ray2D objects."""
    grey = Color(100, 100, 100)
    pt = Point2D(2, 0)
    vec = Vector2D(0, 2)
    ray = DisplayRay2D(Ray2D(pt, vec), grey)
    ray_dict = ray.to_dict()
    new_ray = DisplayRay2D.from_dict(ray_dict)
    assert isinstance(new_ray, DisplayRay2D)
    assert new_ray.to_dict() == ray_dict


def test_display_ray2d_to_svg():
    """Test the translation of Ray2D objects to SVG."""
    pt = Point2D(200, -100)
    v = Point2D(-100, 50)
    ray = Ray2D(pt, v)
    svg_data = DisplayRay2D.ray2d_to_svg(ray)
    assert len(str(svg_data)) > 30

    red = Color(255, 0, 0, 125)
    ray = DisplayRay2D(ray, red)
    svg_data = ray.to_svg()
    assert len(str(svg_data)) > 30
