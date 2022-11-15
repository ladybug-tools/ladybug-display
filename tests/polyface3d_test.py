# coding=utf-8
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.polyface import Polyface3D
from ladybug.color import Color
from ladybug_display.geometry3d.polyface import DisplayPolyface3D


def test_polyface3d_init_solid():
    """Test the initialization of Polyface3D and basic properties of solid objects."""
    grey = Color(100, 100, 100)
    pts = [Point3D(0, 0, 0), Point3D(0, 2, 0), Point3D(2, 2, 0), Point3D(2, 0, 0),
           Point3D(0, 0, 2), Point3D(0, 2, 2), Point3D(2, 2, 2), Point3D(2, 0, 2)]
    face_indices = [[(0, 1, 2, 3)], [(0, 4, 5, 1)], [(0, 3, 7, 4)],
                    [(2, 1, 5, 6)], [(2, 3, 7, 6)], [(4, 5, 6, 7)]]
    polyface = DisplayPolyface3D(Polyface3D(pts, face_indices), grey)

    assert polyface.color == grey
    assert polyface.display_mode == 'Surface'
    assert len(polyface.vertices) == 8
    assert len(polyface.face_indices) == 6
    assert len(polyface.faces) == 6
    assert len(polyface.edge_indices) == 12
    assert len(polyface.edges) == 12
    assert len(polyface.naked_edges) == 0
    assert len(polyface.non_manifold_edges) == 0
    assert len(polyface.internal_edges) == 12
    assert polyface.area == 24
    assert polyface.volume == 8
    assert polyface.is_solid
    for face in polyface.faces:
        assert face.area == 4

    blue = Color(0, 0, 100)
    polyface.color = blue
    polyface.display_mode = 'Wireframe'
    assert polyface.color == blue
    assert polyface.display_mode == 'Wireframe'


def test_polyface3d_to_from_dict():
    """Test the to/from dict of Polyface3D objects."""
    grey = Color(100, 100, 100)
    polyface = DisplayPolyface3D(Polyface3D.from_box(2, 4, 2), grey)
    polyface.display_mode = 'Wireframe'
    polyface_dict = polyface.to_dict()
    new_polyface = DisplayPolyface3D.from_dict(polyface_dict)
    assert isinstance(new_polyface, DisplayPolyface3D)
    assert new_polyface.to_dict() == polyface_dict

    assert len(new_polyface.vertices) == 8
    assert len(new_polyface.face_indices) == 6
    assert len(new_polyface.faces) == 6
    assert len(new_polyface.edge_indices) == 12
    assert len(new_polyface.edges) == 12
    assert len(new_polyface.naked_edges) == 0
    assert len(new_polyface.non_manifold_edges) == 0
    assert len(new_polyface.internal_edges) == 12
    assert new_polyface.area == 40
    assert new_polyface.volume == 16
    assert new_polyface.is_solid
    assert new_polyface.color == grey
    assert new_polyface.display_mode == 'Wireframe'
