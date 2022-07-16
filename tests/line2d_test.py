# coding=utf-8
from ladybug_geometry.geometry2d.pointvector import Point2D, Vector2D
from ladybug_geometry.geometry2d.line import LineSegment2D
from ladybug.color import Color
from ladybug_display.geometry2d.line import DisplayLineSegment2D
from ladybug_display.altnumber import default


def test_display_linesegment3d_init():
    """Test the initialization of LineSegment2D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point2D(2, 0)
    vec = Vector2D(0, 2)
    seg = DisplayLineSegment2D(LineSegment2D(pt, vec), grey)
    str(seg)  # test the string representation of the line segment

    assert seg.color == grey
    assert seg.line_width == default
    assert seg.line_type == 'Continuous'
    assert seg.p == Point2D(2, 0)
    assert seg.v == Vector2D(0, 2)
    assert seg.p1 == Point2D(2, 0)
    assert seg.p2 == Point2D(2, 2)
    assert seg.length == 2

    blue = Color(0, 0, 100)
    seg.color = blue
    seg.line_width = 2
    seg.line_type = 'Dashed'
    assert seg.color == blue
    assert seg.line_width == 2
    assert seg.line_type == 'Dashed'


def test_linesegment3_to_from_dict():
    """Test the to/from dict of DisplayLineSegment2D objects."""
    grey = Color(100, 100, 100)
    pt = Point2D(2, 0)
    vec = Vector2D(0, 2)
    seg = DisplayLineSegment2D(LineSegment2D(pt, vec), grey)
    seg.line_type = 'Dashed'
    seg_dict = seg.to_dict()
    new_seg = DisplayLineSegment2D.from_dict(seg_dict)
    assert isinstance(new_seg, DisplayLineSegment2D)
    assert new_seg.to_dict() == seg_dict
