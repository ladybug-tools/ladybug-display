# coding=utf-8
import pytest

from ladybug_geometry.geometry3d.arc import Arc3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug.color import Color
from ladybug_display.geometry3d.arc import DisplayArc3D
from ladybug_display.altnumber import default

import math


def test_display_arc3d_init():
    """Test the initialization of Arc3D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    arc = DisplayArc3D(Arc3D(Plane(o=pt), 1, 0, math.pi), grey)
    str(arc)  # test the string representation of the arc

    assert arc.color == grey
    assert arc.line_width == default
    assert arc.line_type == 'Continuous'
    assert arc.c == pt
    assert arc.radius == 1
    assert arc.p1 == Point3D(3, 0, 2)
    assert arc.p2.x == pytest.approx(1, rel=1e-3)
    assert arc.p2.y == pytest.approx(0, rel=1e-3)
    assert arc.p2.z == pytest.approx(2, rel=1e-3)
    assert arc.length == pytest.approx(math.pi, rel=1e-3)
    assert arc.angle == pytest.approx(180, rel=1e-3)
    assert arc.is_circle is False

    blue = Color(0, 0, 100)
    arc.color = blue
    arc.line_width = 2
    arc.line_type = 'Dashed'
    assert arc.color == blue
    assert arc.line_width == 2
    assert arc.line_type == 'Dashed'


def test_display_arc3d_to_from_dict():
    """Test the initialization of Arc3D objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    arc = DisplayArc3D(Arc3D(Plane(o=pt), 1, 0, math.pi), grey)
    arc_dict = arc.to_dict()
    new_arc = DisplayArc3D.from_dict(arc_dict)
    assert isinstance(new_arc, DisplayArc3D)
    assert new_arc.to_dict() == arc_dict


def test_display_arc2d_to_svg():
    """Test the translation of Arc3D objects to SVG."""
    pt = Plane(o=Point3D(200, -100))
    circle = Arc3D(pt, 50, 0, math.pi * 2)
    svg_data = DisplayArc3D.arc3d_to_svg(circle)
    assert len(str(svg_data)) > 30

    arc = Arc3D(pt, 50, 0, math.pi)
    svg_data = DisplayArc3D.arc3d_to_svg(arc)
    assert len(str(svg_data)) > 30

    arc = Arc3D(pt, 50, math.pi / 4, math.pi * 1.5)
    svg_data = DisplayArc3D.arc3d_to_svg(arc)
    assert len(str(svg_data)) > 30

    grey = Color(100, 100, 100)
    arc = Arc3D(pt, 50, math.pi / 4, math.pi * 1.5)
    arc = DisplayArc3D(arc, grey, line_width=2, line_type='Dashed')
    svg_data = arc.to_svg()
    assert len(str(svg_data)) > 30
