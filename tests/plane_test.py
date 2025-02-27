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


def test_display_plane_to_svg():
    """Test the translation of Plane objects to SVG."""
    pt = Point3D(200, -100)
    v = Point3D(-100, 50)
    plane = Plane(o=pt, x=v)
    svg_data = DisplayPlane.plane_to_svg(plane)
    assert len(str(svg_data)) > 30

    red = Color(255, 0, 0, 125)
    plane = DisplayPlane(plane, red)
    svg_data = plane.to_svg()
    assert len(str(svg_data)) > 30

    import ladybug_display.svg as svg
    canvas = svg.SVG(width=800, height=600)
    canvas.elements = [svg_data]
    print(canvas)
