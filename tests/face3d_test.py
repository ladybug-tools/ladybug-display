# coding=utf-8
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.face import Face3D
from ladybug.color import Color
from ladybug_display.geometry3d.face import DisplayFace3D


def test_display_face3d_init():
    """Test the initialization of DisplayFace3D objects and basic properties."""
    grey = Color(100, 100, 100)
    pts = (Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2))
    plane = Plane(Vector3D(0, 0, 1), Point3D(0, 0, 2))
    face = DisplayFace3D(Face3D(pts, plane), grey)
    str(face)  # test the string representation of the face

    assert face.color == grey
    assert face.display_mode == 'Surface'
    assert isinstance(face.vertices, tuple)
    assert len(face.vertices) == 4
    for point in face.vertices:
        assert isinstance(point, Point3D)
    assert face.area == 4
    assert face.perimeter == 8
    assert round(face.altitude, 3) == round(90, 3)
    assert round(face.azimuth, 3) == 0

    blue = Color(0, 0, 100)
    face.color = blue
    face.display_mode = 'Wireframe'
    assert face.color == blue
    assert face.display_mode == 'Wireframe'


def test_face3d_to_from_dict():
    """Test the to/from dict of Face3D objects."""
    grey = Color(100, 100, 100)
    pts = (Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2))
    plane = Plane(Vector3D(0, 0, 1), Point3D(0, 0, 2))
    face = DisplayFace3D(Face3D(pts, plane), grey)
    face.display_mode = 'Wireframe'
    face_dict = face.to_dict()
    new_face = DisplayFace3D.from_dict(face_dict)
    assert isinstance(new_face, DisplayFace3D)
    assert new_face.to_dict() == face_dict

    bound_pts = [Point3D(0, 0), Point3D(4, 0), Point3D(4, 4), Point3D(0, 4)]
    hole_pts = [Point3D(1, 1), Point3D(3, 1), Point3D(3, 3), Point3D(1, 3)]
    face = DisplayFace3D(Face3D(bound_pts, None, [hole_pts]), grey)
    face_dict = face.to_dict()
    new_face = DisplayFace3D.from_dict(face_dict)
    assert isinstance(new_face, DisplayFace3D)
    assert new_face.to_dict() == face_dict
