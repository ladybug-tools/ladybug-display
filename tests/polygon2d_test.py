# coding=utf-8
from ladybug_geometry.geometry2d.pointvector import Point2D
from ladybug_geometry.geometry2d.polygon import Polygon2D
from ladybug.color import Color
from ladybug_display.geometry2d.polygon import DisplayPolygon2D
from ladybug_display.altnumber import default


def test_display_p_gon2d_init():
    """Test the initialization of DisplayFace2D objects and basic properties."""
    grey = Color(100, 100, 100)
    pts = (Point2D(0, 0), Point2D(0, 2), Point2D(2, 2), Point2D(2, 0))
    p_gon = DisplayPolygon2D(Polygon2D(pts), grey)
    str(p_gon)  # test the string representation of the p_gon

    assert p_gon.color == grey
    assert p_gon.line_width == default
    assert p_gon.line_type == 'Continuous'
    assert isinstance(p_gon.vertices, tuple)
    assert len(p_gon.vertices) == 4
    for point in p_gon.vertices:
        assert isinstance(point, Point2D)
    assert p_gon.area == 4
    assert p_gon.perimeter == 8

    blue = Color(0, 0, 100)
    p_gon.color = blue
    p_gon.line_width = 2
    p_gon.line_type = 'Dashed'
    assert p_gon.color == blue
    assert p_gon.line_width == 2
    assert p_gon.line_type == 'Dashed'


def test_p_gon2d_to_from_dict():
    """Test the to/from dict of Face2D objects."""
    grey = Color(100, 100, 100)
    pts = (Point2D(0, 0), Point2D(0, 2), Point2D(2, 2), Point2D(2, 0))
    p_gon = DisplayPolygon2D(Polygon2D(pts), grey)
    p_gon.line_width = 2
    p_gon.line_type = 'Dashed'
    p_gon_dict = p_gon.to_dict()
    new_p_gon = DisplayPolygon2D.from_dict(p_gon_dict)
    assert isinstance(new_p_gon, DisplayPolygon2D)
    assert new_p_gon.to_dict() == p_gon_dict
