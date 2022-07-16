# coding=utf-8
from ladybug_geometry.geometry2d.pointvector import Point2D
from ladybug_geometry.geometry2d.line import LineSegment2D
from ladybug_geometry.geometry2d.polyline import Polyline2D
from ladybug.color import Color
from ladybug_display.geometry2d.polyline import DisplayPolyline2D
from ladybug_display.altnumber import default


def test_display_polyline2d_init():
    """Test the initialization of DisplayPolyline2D objects and basic properties."""
    grey = Color(100, 100, 100)
    pts = (Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(0, 2))
    pline = DisplayPolyline2D(Polyline2D(pts), grey)
    str(pline)  # test the string representation of the polyline

    assert pline.color == grey
    assert pline.line_width == default
    assert pline.line_type == 'Continuous'

    assert isinstance(pline.vertices, tuple)
    assert len(pline.vertices) == 4
    for point in pline.vertices:
        assert isinstance(point, Point2D)

    assert isinstance(pline.segments, tuple)
    assert len(pline.segments) == 3
    for seg in pline.segments:
        assert isinstance(seg, LineSegment2D)
        assert seg.length == 2

    assert pline.p1 == pts[0]
    assert pline.p2 == pts[-1]
    assert pline.length == 6

    blue = Color(0, 0, 100)
    pline.color = blue
    pline.line_width = 2
    pline.line_type = 'Dashed'
    assert pline.color == blue
    assert pline.line_width == 2
    assert pline.line_type == 'Dashed'


def test_polyline2d_to_from_dict():
    """Test the to/from dict of DisplayPolyline2D objects."""
    grey = Color(100, 100, 100)
    pts = (Point2D(0, 0), Point2D(2, 0), Point2D(2, 2), Point2D(0, 2))
    pline = DisplayPolyline2D(Polyline2D(pts), grey)
    pline.line_width = 2
    pline.line_type = 'Dashed'
    pline_dict = pline.to_dict()
    new_pline = DisplayPolyline2D.from_dict(pline_dict)
    assert isinstance(new_pline, DisplayPolyline2D)
    assert new_pline.to_dict() == pline_dict
