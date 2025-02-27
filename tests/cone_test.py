# coding=utf-8
import math
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.cone import Cone
from ladybug.color import Color
from ladybug_display.geometry3d.cone import DisplayCone


def test_cone_init():
    """Test the initialization of Cone objects and basic properties."""
    grey = Color(100, 100, 100)
    vertex = Point3D(2, 0, 2)
    axis = Vector3D(0, 2, 2)
    angle = 0.7
    c = DisplayCone(Cone(vertex, axis, angle), grey)
    str(c)  # test the string representation of the cone

    assert c.color == grey
    assert c.display_mode == 'Surface'
    assert c.vertex == Point3D(2, 0, 2)
    assert c.axis == Vector3D(0, 2, 2)
    assert c.height == c.axis.magnitude
    assert isinstance(c.area, float)
    assert isinstance(c.volume, float)

    blue = Color(0, 0, 100)
    c.color = blue
    c.display_mode = 'Wireframe'
    assert c.color == blue
    assert c.display_mode == 'Wireframe'


def test_cone_to_from_dict():
    """Test the Cone to_dict and from_dict methods."""
    grey = Color(100, 100, 100)
    c = DisplayCone(Cone(Point3D(4, 0.5, 2), Vector3D(1, 0, 2.5), 0.7), grey)
    con_d = c.to_dict()
    new_c = DisplayCone.from_dict(con_d)
    assert isinstance(new_c, DisplayCone)
    assert new_c.to_dict() == con_d


def test_display_cone_to_svg():
    """Test the translation of Cone objects to SVG."""
    pt1 = Point3D(200, -400)
    axis = Vector3D(200, 200, 200)
    cone = Cone(pt1, axis, math.radians(30))
    svg_data = DisplayCone.cone_to_svg(cone)
    assert len(str(svg_data)) > 30

    red = Color(255, 0, 0, 125)
    cone = DisplayCone(cone, red, 'SurfaceWithEdges')
    svg_data = cone.to_svg()
    assert len(str(svg_data)) > 30
