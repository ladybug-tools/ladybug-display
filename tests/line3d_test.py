# coding=utf-8
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.line import LineSegment3D
from ladybug.color import Color
from ladybug_display.geometry3d.line import DisplayLineSegment3D
from ladybug_display.altnumber import default


def test_display_linesegment3d_init():
    """Test the initialization of LineSegment3D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    vec = Vector3D(0, 2, 0)
    seg = DisplayLineSegment3D(LineSegment3D(pt, vec), grey)
    str(seg)  # test the string representation of the line segment

    assert seg.color == grey
    assert seg.line_width == default
    assert seg.line_type == 'Continuous'
    assert seg.p == Point3D(2, 0, 2)
    assert seg.v == Vector3D(0, 2, 0)
    assert seg.p1 == Point3D(2, 0, 2)
    assert seg.p2 == Point3D(2, 2, 2)
    assert seg.length == 2

    blue = Color(0, 0, 100)
    seg.color = blue
    seg.line_width = 2
    seg.line_type = 'Dashed'
    assert seg.color == blue
    assert seg.line_width == 2
    assert seg.line_type == 'Dashed'


def test_linesegment3_to_from_dict():
    """Test the to/from dict of DisplayLineSegment3D objects."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    vec = Vector3D(0, 2, 0)
    seg = DisplayLineSegment3D(LineSegment3D(pt, vec), grey)
    seg.line_type = 'Dashed'
    seg_dict = seg.to_dict()
    new_seg = DisplayLineSegment3D.from_dict(seg_dict)
    assert isinstance(new_seg, DisplayLineSegment3D)
    assert new_seg.to_dict() == seg_dict


def test_display_linesegment3d_to_svg():
    """Test the translation of LineSegment2D objects to SVG."""
    pt1 = Point3D(200, -100)
    pt2 = Point3D(100, -50)
    line = LineSegment3D.from_end_points(pt1, pt2)
    svg_data = DisplayLineSegment3D.linesegment3d_to_svg(line)
    assert len(str(svg_data)) > 30

    red = Color(255, 0, 0, 125)
    line = DisplayLineSegment3D(line, red, line_width=2, line_type='Dashed')
    svg_data = line.to_svg()
    assert len(str(svg_data)) > 30
