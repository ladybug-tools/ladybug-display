# coding=utf-8
from ladybug_geometry.geometry2d.pointvector import Point2D
from ladybug_geometry.geometry2d.mesh import Mesh2D
from ladybug.color import Color
from ladybug_display.geometry2d.mesh import DisplayMesh2D


def test_display_mesh2d_init():
    """Test the initialization of DisplayMesh2D objects with two faces."""
    grey = Color(100, 100, 100)
    pts = (Point2D(0, 0), Point2D(0, 2), Point2D(2, 2),
           Point2D(2, 0), Point2D(4, 0))
    mesh = DisplayMesh2D(Mesh2D(pts, [(0, 1, 2, 3), (2, 3, 4)]), grey)

    assert mesh.color == grey
    assert mesh.display_mode == 'Surface'
    assert len(mesh.vertices) == 5
    assert len(mesh.faces) == 2
    assert mesh.area == 6
    assert mesh.min == Point2D(0, 0)
    assert mesh.max == Point2D(4, 2)
    assert mesh.center == Point2D(2, 1)
    assert len(mesh.face_areas) == 2
    assert mesh.face_areas[0] == 4
    assert mesh.face_areas[1] == 2
    assert len(mesh.face_centroids) == 2
    assert mesh.face_centroids[0] == Point2D(1, 1)

    blue = Color(0, 0, 100)
    mesh.color = blue
    mesh.display_mode = 'Wireframe'
    assert mesh.color == blue
    assert mesh.display_mode == 'Wireframe'


def test_mesh2d_to_from_dict():
    """Test the to/from dict of Mesh2D objects."""
    grey = Color(100, 100, 100)
    pts = (Point2D(0, 0), Point2D(0, 2), Point2D(2, 2), Point2D(2, 0))
    mesh = DisplayMesh2D(Mesh2D(pts, [(0, 1, 2, 3)]), grey)
    mesh.display_mode = 'Wireframe'
    mesh_dict = mesh.to_dict()
    new_mesh = DisplayMesh2D.from_dict(mesh_dict)
    assert isinstance(new_mesh, DisplayMesh2D)
    assert new_mesh.to_dict() == mesh_dict


def test_mesh2d_to_svg():
    """Test the translation of Mesh2D objects to SVG."""
    pts = (Point2D(200, -50), Point2D(100, -50), Point2D(100, -100), Point2D(200, -100),
           Point2D(150, -200))
    mesh = Mesh2D(pts, [(0, 1, 2, 3), (2, 3, 4)])
    mesh.colors = [Color(255, 0, 0), Color(0, 0, 255)]
    svg_data = DisplayMesh2D.mesh2d_to_svg(mesh)
    assert len(str(svg_data)) > 30

    grey = Color(100, 100, 100, 125)
    p_gon = DisplayMesh2D(mesh, grey, 'SurfaceWithEdges')
    svg_data = p_gon.to_svg()
    assert len(str(svg_data)) > 30
