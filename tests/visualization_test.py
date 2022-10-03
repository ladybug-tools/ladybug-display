# coding=utf-8
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry2d.mesh import Mesh2D
from ladybug_geometry.geometry3d.mesh import Mesh3D
from ladybug_geometry.geometry3d.polyface import Polyface3D

from ladybug.graphic import GraphicContainer
from ladybug.legend import Legend, LegendParameters

from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData


def test_init_visualization_set():
    """Test the initialization of VisualizationSet objects."""
    context = Polyface3D.from_box(2, 4, 2, base_plane=Plane(o=Point3D(0, 2, 0)))
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    data = VisualizationData([0, 1, 2, 3])
    a_geo = AnalysisGeometry([mesh3d], [data])
    vis_set = VisualizationSet([a_geo], [context])

    str(vis_set)  # Test the GraphicContainer representation

    assert a_geo.matching_method == 'faces'
    assert len(data) == 4
    assert data[0] == 0
    assert data[-1] == 3
    for item in data:
        assert isinstance(item, (float, int))

    graphic_con = vis_set.graphic_container()
    assert isinstance(graphic_con, GraphicContainer)
    assert len(graphic_con.values) == 4
    assert isinstance(graphic_con.legend, Legend)
    assert graphic_con.value_colors == graphic_con.legend.value_colors

    assert graphic_con.legend_parameters.is_base_plane_default
    assert graphic_con.legend_parameters.is_segment_height_default
    assert graphic_con.legend_parameters.is_segment_width_default
    assert graphic_con.legend_parameters.is_text_height_default
    assert graphic_con.legend_parameters.base_plane != Plane()

    assert isinstance(graphic_con.lower_title_location, Plane)
    assert isinstance(graphic_con.upper_title_location, Plane)
    assert graphic_con.lower_title_location != Plane()
    assert graphic_con.upper_title_location != Plane()


def test_init_visualization_set_legend_parameters():
    """Test the initialization of VisualizationSet objects with a LegendParameters."""
    context = Polyface3D.from_box(2, 4, 2, base_plane=Plane(o=Point3D(0, 2, 0)))
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    legend_par = LegendParameters(base_plane=Plane(o=Point3D(2, 2, 0)))
    legend_par.vertical = False
    legend_par.segment_height = 0.25
    legend_par.segment_width = 0.5
    legend_par.text_height = 0.15
    data = VisualizationData([-1, 0, 1, 2], legend_par)
    a_geo = AnalysisGeometry([mesh3d], [data])
    vis_set = VisualizationSet([a_geo], [context])

    graphic_con = vis_set.graphic_container()
    assert not graphic_con.legend_parameters.is_base_plane_default
    assert not graphic_con.legend_parameters.is_segment_height_default
    assert not graphic_con.legend_parameters.is_segment_width_default
    assert not graphic_con.legend_parameters.is_text_height_default
    assert not graphic_con.legend_parameters.vertical
    assert graphic_con.legend_parameters.base_plane.o == Point3D(2, 2, 0)
    assert graphic_con.legend_parameters.segment_height == 0.25
    assert graphic_con.legend_parameters.segment_width == 0.5
    assert graphic_con.legend_parameters.text_height == 0.15


def test_to_from_dict():
    """Test the to/from dict methods."""
    context = Polyface3D.from_box(2, 4, 2, base_plane=Plane(o=Point3D(0, 2, 0)))
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    data = VisualizationData([0, 1, 2, 3])
    a_geo = AnalysisGeometry([mesh3d], [data])
    vis_set = VisualizationSet([a_geo], [context])

    vis_set_dict = vis_set.to_dict()
    new_vis_set = VisualizationSet.from_dict(vis_set_dict)
    assert new_vis_set.to_dict() == vis_set_dict
