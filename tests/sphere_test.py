# coding=utf-8
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.sphere import Sphere
from ladybug.color import Color
from ladybug_display.geometry3d.sphere import DisplaySphere


def test_display_sphere_init():
    """Test the initialization of Sphere objects and basic properties."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    r = 3
    sp = DisplaySphere(Sphere(pt, r), grey)
    str(sp)  # test the string representation of the line segment

    assert sp.color == grey
    assert sp.display_mode == 'Surface'
    assert sp.center == Point3D(2, 0, 2)
    assert sp.radius == 3
    assert sp.min.z == -1
    assert sp.max.z == 5
    assert sp.diameter == 6
    assert isinstance(sp.circumference, float)
    assert isinstance(sp.area, float)
    assert isinstance(sp.volume, float)

    blue = Color(0, 0, 100)
    sp.color = blue
    sp.display_mode = 'Wireframe'
    assert sp.color == blue
    assert sp.display_mode == 'Wireframe'


def test_sphere_to_from_dict():
    """Test the Sphere to_dict and from_dict methods."""
    grey = Color(100, 100, 100)
    pt = Point3D(2, 0, 2)
    r = 3
    sp = DisplaySphere(Sphere(pt, r), grey)

    sp_d = sp.to_dict()
    new_sp = DisplaySphere.from_dict(sp_d)
    assert isinstance(new_sp, DisplaySphere)
    assert new_sp.to_dict() == sp_d
