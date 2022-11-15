# coding=utf-8
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.mesh import Mesh3D
from ladybug.color import Color
from ladybug_display.geometry3d.mesh import DisplayMesh3D


def test_display_mesh3d_init():
    """Test the initialization of DisplayMesh3D objects with two faces."""
    grey = Color(100, 100, 100)
    pts = (Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2),
           Point3D(2, 0, 2), Point3D(4, 0, 2))
    mesh = DisplayMesh3D(Mesh3D(pts, [(0, 1, 2, 3), (2, 3, 4)]), grey)

    assert mesh.color == grey
    assert mesh.display_mode == 'Surface'
    assert len(mesh.vertices) == 5
    assert len(mesh.faces) == 2
    assert mesh.area == 6
    assert mesh.min == Point3D(0, 0, 2)
    assert mesh.max == Point3D(4, 2, 2)
    assert mesh.center == Point3D(2, 1, 2)
    assert len(mesh.face_areas) == 2
    assert mesh.face_areas[0] == 4
    assert mesh.face_areas[1] == 2
    assert len(mesh.face_centroids) == 2
    assert mesh.face_centroids[0] == Point3D(1, 1, 2)

    blue = Color(0, 0, 100)
    mesh.color = blue
    mesh.display_mode = 'Wireframe'
    assert mesh.color == blue
    assert mesh.display_mode == 'Wireframe'


def test_mesh3d_to_from_dict():
    """Test the to/from dict of Mesh3D objects."""
    grey = Color(100, 100, 100)
    pts = (Point3D(0, 0), Point3D(0, 2), Point3D(2, 2), Point3D(2, 0))
    mesh = DisplayMesh3D(Mesh3D(pts, [(0, 1, 2, 3)]), grey)
    mesh.display_mode = 'Wireframe'
    mesh_dict = mesh.to_dict()
    new_mesh = DisplayMesh3D.from_dict(mesh_dict)
    assert isinstance(new_mesh, DisplayMesh3D)
    assert new_mesh.to_dict() == mesh_dict
