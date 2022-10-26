# coding=utf-8
import os
import pytest

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry2d.mesh import Mesh2D
from ladybug_geometry.geometry3d.mesh import Mesh3D
from ladybug_geometry.geometry3d.polyface import Polyface3D

from ladybug.futil import nukedir
from ladybug.datatype.temperature import Temperature
from ladybug.datatype.thermalcondition import PredictedMeanVote
from ladybug.graphic import GraphicContainer
from ladybug.legend import Legend, LegendParameters

from ladybug_display.visualization import VisualizationSet, ContextGeometry, \
    AnalysisGeometry, VisualizationData


def test_init_visualization_set():
    """Test the initialization of VisualizationSet objects."""
    con_geo = Polyface3D.from_box(2, 4, 2, base_plane=Plane(o=Point3D(0, 2, 0)))
    context = ContextGeometry('Building_Massing', [con_geo])
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    data = VisualizationData([0, 1, 2, 3])
    a_geo = AnalysisGeometry('Test_Results', [mesh3d], [data])
    vis_set = VisualizationSet('Test_Set', [a_geo, context])
    str(vis_set)

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
    con_geo = Polyface3D.from_box(2, 4, 2, base_plane=Plane(o=Point3D(0, 2, 0)))
    context = ContextGeometry('Building_Massing', [con_geo])
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    legend_par = LegendParameters(base_plane=Plane(o=Point3D(2, 2, 0)))
    legend_par.vertical = False
    legend_par.segment_height = 0.25
    legend_par.segment_width = 0.5
    legend_par.text_height = 0.15
    data = VisualizationData([-1, 0, 1, 2], legend_par)
    a_geo = AnalysisGeometry('Test_Results', [mesh3d], [data])
    vis_set = VisualizationSet('Test_Set', [a_geo, context])

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
    con_geo = Polyface3D.from_box(2, 4, 2, base_plane=Plane(o=Point3D(0, 2, 0)))
    context = ContextGeometry('Building_Massing', [con_geo])
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    data = VisualizationData([0, 1, 2, 3])
    a_geo = AnalysisGeometry('Test_Results', [mesh3d], [data])
    vis_set = VisualizationSet('Test_Set', [a_geo, context])

    vis_set_dict = vis_set.to_dict()
    new_vis_set = VisualizationSet.from_dict(vis_set_dict)
    assert new_vis_set.to_dict() == vis_set_dict


def test_to_from_json():
    """Test the to/from json methods."""
    con_geo = Polyface3D.from_box(2, 4, 2, base_plane=Plane(o=Point3D(0, 2, 0)))
    context = ContextGeometry('Building_Massing', [con_geo])
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    data = VisualizationData([0, 1, 2, 3])
    a_geo = AnalysisGeometry('Test_Results', [mesh3d], [data])
    vis_set = VisualizationSet('Test_Set', [a_geo, context])

    path = './tests/json'
    vis_set_json = vis_set.to_json('test', path)
    assert os.path.isfile(vis_set_json)
    new_vis_set = VisualizationSet.from_file(vis_set_json)
    assert isinstance(new_vis_set, VisualizationSet)
    nukedir(path)


def test_to_from_pkl():
    """Test the to/from pkl methods."""
    con_geo = Polyface3D.from_box(2, 4, 2, base_plane=Plane(o=Point3D(0, 2, 0)))
    context = ContextGeometry('Building_Massing', [con_geo])
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    data = VisualizationData([0, 1, 2, 3])
    a_geo = AnalysisGeometry('Test_Results', [mesh3d], [data])
    vis_set = VisualizationSet('Test_Set', [a_geo, context])

    path = './tests/pkl'
    vis_set_pkl = vis_set.to_pkl('test', path)
    assert os.path.isfile(vis_set_pkl)
    new_vis_set = VisualizationSet.from_file(vis_set_pkl)
    assert new_vis_set.to_dict() == vis_set.to_dict()
    nukedir(path)


def test_init_analysis_geometry():
    """Test the initialization of AnalysisGeometry objects."""
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    values = [0, 1, 2, 3]
    data = VisualizationData(values)
    analysis_geo = AnalysisGeometry('test_analysis', [mesh3d], [data])
    str(analysis_geo)  # test the string representation
    assert analysis_geo.matching_method == 'faces'

    assert len(analysis_geo[0]) == 4
    assert analysis_geo[0][0] == 0
    assert analysis_geo[0][-1] == 3
    for item in analysis_geo[0]:
        assert isinstance(item, (float, int))

    assert len(analysis_geo[0].values) == 4
    assert isinstance(analysis_geo[0].legend, Legend)
    assert analysis_geo[0].value_colors == analysis_geo[0].legend.value_colors

    assert analysis_geo[0].legend_parameters.is_base_plane_default
    assert analysis_geo[0].legend_parameters.is_segment_height_default
    assert analysis_geo[0].legend_parameters.is_segment_width_default
    assert analysis_geo[0].legend_parameters.is_text_height_default

    graphic_con = analysis_geo.graphic_container()
    assert graphic_con.legend_parameters.base_plane != Plane()
    assert isinstance(graphic_con.lower_title_location, Plane)
    assert isinstance(graphic_con.upper_title_location, Plane)
    assert graphic_con.lower_title_location != Plane()
    assert graphic_con.upper_title_location != Plane()


def test_init_analysis_geometry_invalid():
    """Test the initialization of AnalysisGeometry objects with invalid inputs."""
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    values = [0, 1, 2, 3, 4]
    data = VisualizationData(values)

    with pytest.raises(Exception):
        AnalysisGeometry('test_analysis', [mesh3d], [data])


def test_init_analysis_geometry_vertex_based():
    """Test the initialization of AnalysisGeometry objects with vertex-based input."""
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    data = VisualizationData(values)
    analysis_geo = AnalysisGeometry('test_analysis', [mesh3d], [data])
    assert analysis_geo.matching_method == 'vertices'

    assert len(analysis_geo[0].values) == 9
    assert isinstance(analysis_geo[0].legend_parameters, LegendParameters)
    assert isinstance(analysis_geo[0].legend, Legend)
    assert analysis_geo[0].value_colors == analysis_geo[0].legend.value_colors


def test_init_analysis_geometry_legend_parameters():
    """Test the initialization of AnalysisGeometry objects with a LegendParameters."""
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    values = [-1, 0, 1, 2]
    legend_par = LegendParameters(base_plane=Plane(o=Point3D(2, 2, 0)))
    legend_par.vertical = False
    legend_par.segment_height = 0.25
    legend_par.segment_width = 0.5
    legend_par.text_height = 0.15
    data = VisualizationData(values, legend_par)
    analysis_geo = AnalysisGeometry('test_analysis', [mesh3d], [data])

    assert not analysis_geo[0].legend_parameters.is_base_plane_default
    assert not analysis_geo[0].legend_parameters.is_segment_height_default
    assert not analysis_geo[0].legend_parameters.is_segment_width_default
    assert not analysis_geo[0].legend_parameters.is_text_height_default
    assert not analysis_geo[0].legend_parameters.vertical
    assert analysis_geo[0].legend_parameters.base_plane.o == Point3D(2, 2, 0)
    assert analysis_geo[0].legend_parameters.segment_height == 0.25
    assert analysis_geo[0].legend_parameters.segment_width == 0.5
    assert analysis_geo[0].legend_parameters.text_height == 0.15


def test_init_analysis_geometry_data_type():
    """Test the initialization of AnalysisGeometry objects with a DataType."""
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    values = [-1, 0, 1, 2]
    data = VisualizationData(values, data_type=Temperature())
    analysis_geo = AnalysisGeometry('test_analysis', [mesh3d], [data])

    assert not analysis_geo[0].legend_parameters.is_title_default
    assert analysis_geo[0].legend_parameters.title == 'C'

    legend_par = LegendParameters()
    legend_par.vertical = False
    data = VisualizationData(values, legend_par, data_type=Temperature())
    analysis_geo = AnalysisGeometry('test_analysis', [mesh3d], [data])

    assert not analysis_geo[0].legend_parameters.is_title_default
    assert analysis_geo[0].legend_parameters.title == 'Temperature (C)'


def test_init_analysis_geometry_data_type_ordinal():
    """Test the AnalysisGeometry objects with a DataType with unit_descr."""
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    values = [-1, 0, 1, 2]
    data = VisualizationData(values, data_type=PredictedMeanVote(), unit='PMV')
    analysis_geo = AnalysisGeometry('test_analysis', [mesh3d], [data])

    assert analysis_geo[0].legend_parameters.min == -3
    assert analysis_geo[0].legend_parameters.max == 3
    assert analysis_geo[0].legend_parameters.segment_count == 7
    assert not analysis_geo[0].legend_parameters.is_title_default
    assert analysis_geo[0].legend_parameters.title == 'PMV'
    assert analysis_geo[0].legend.segment_text == \
        ['Cold', 'Cool', 'Slightly Cool', 'Neutral', 'Slightly Warm', 'Warm', 'Hot']
