# coding=utf-8
import pytest
import math

from ladybug_geometry.geometry2d.arc import Arc2D
from ladybug_geometry.geometry2d.pointvector import Point2D
from ladybug.color import Color
from ladybug_display.geometry2d.arc import DisplayArc2D
from ladybug_display.altnumber import default


def test_display_arc2d_init():
    """Test the initialization of Arc2D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point2D(2, 0)
    arc = DisplayArc2D(Arc2D(pt, 1, 0, math.pi), grey)
    str(arc)  # test the string representation of the arc

    assert arc.color == grey
    assert arc.line_width == default
    assert arc.line_type == 'Continuous'
    assert arc.c == pt
    assert arc.r == 1
    assert arc.p1 == Point2D(3, 0)
    assert arc.p2.x == pytest.approx(1, rel=1e-3)
    assert arc.p2.y == pytest.approx(0, rel=1e-3)
    assert arc.length == pytest.approx(math.pi, rel=1e-3)
    assert arc.is_circle is False

    blue = Color(0, 0, 100)
    arc.color = blue
    arc.line_width = 2
    arc.line_type = 'Dashed'
    assert arc.color == blue
    assert arc.line_width == 2
    assert arc.line_type == 'Dashed'


def test_display_arc2d_to_from_dict():
    """Test the initialization of Arc2D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point2D(2, 0)
    arc = DisplayArc2D(Arc2D(pt, 1, 0, math.pi), grey)
    arc_dict = arc.to_dict()
    new_arc = DisplayArc2D.from_dict(arc_dict)
    assert isinstance(new_arc, DisplayArc2D)
    assert new_arc.to_dict() == arc_dict


def test_display_arc2d_to_svg():
    """Test the translation of Arc2D objects to SVG."""
    pt = Point2D(200, -100)
    circle = Arc2D(pt, 50, 0, math.pi * 2)
    svg_data = DisplayArc2D.arc2d_to_svg(circle)
    assert len(str(svg_data)) > 30

    pt = Point2D(200, -100)
    arc = Arc2D(pt, 50, 0, math.pi)
    svg_data = DisplayArc2D.arc2d_to_svg(arc)
    assert len(str(svg_data)) > 30

    pt = Point2D(200, -100)
    arc = Arc2D(pt, 50, math.pi / 4, math.pi * 1.5)
    svg_data = DisplayArc2D.arc2d_to_svg(arc)
    assert len(str(svg_data)) > 30

    grey = Color(100, 100, 100)
    pt = Point2D(200, -100)
    arc = Arc2D(pt, 50, math.pi / 4, math.pi * 1.5)
    arc = DisplayArc2D(arc, grey, line_width=2, line_type='Dashed')
    svg_data = arc.to_svg()
    assert len(str(svg_data)) > 30
