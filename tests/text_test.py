# coding=utf-8
from ladybug_geometry.geometry3d import Point3D, Plane
from ladybug.color import Color
from ladybug_display.geometry3d.text import DisplayText3D


def test_display_text3d_init():
    """Test the initialization of DisplayText3D objects and basic properties."""
    grey = Color(100, 100, 100)
    text = DisplayText3D('Hello World!', Plane(o=Point3D(0, 2, 0)), 1, grey)
    str(text)  # test the string representation of the point

    assert text.plane.o.x == 0
    assert text.plane.o.y == 2
    assert text.plane.o.z == 0
    assert text.color == grey
    assert text.height == 1
    assert text.font == 'Arial'
    assert text.horizontal_alignment == 'Left'
    assert text.vertical_alignment == 'Bottom'


def test_display_text3d_to_svg():
    """Test the initialization of DisplayPoint3D objects and basic properties."""
    red = Color(255, 0, 0)
    pt1 = Point3D(200, -100)
    text = DisplayText3D('Hello World!', Plane(o=pt1), 12, red)
    svg_data = text.to_svg()
    assert len(str(svg_data)) > 30

    import ladybug_display.svg as svg
    canvas = svg.SVG(width=800, height=600)
    canvas.elements = [svg_data]
    print(canvas)
