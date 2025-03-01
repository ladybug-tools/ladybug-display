# coding=utf-8
import os
import pytest

from ladybug_geometry.geometry2d import Mesh2D
from ladybug_geometry.geometry3d import Point3D, Plane, Mesh3D
from ladybug.datatype.temperature import Temperature
from ladybug.datatype.thermalcondition import PredictedMeanVote
from ladybug.legend import Legend, LegendParameters
from ladybug.epw import EPW
from ladybug.hourlyplot import HourlyPlot

from ladybug_display.analysis import VisualizationData, AnalysisGeometry


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


def test_init_visualization_data_to_svg():
    """Test the translation of VisualizationData to SVG."""
    l_par = LegendParameters()
    data = VisualizationData([0, 1, 2, 3], l_par, data_type=Temperature())
    svg_data = data.to_svg()
    assert len(str(svg_data)) > 300
    l_par = LegendParameters(0, 10)
    l_par.vertical = False
    l_par.continuous_legend = True
    l_par.decimal_count = 0
    data = VisualizationData([0, 1, 2, 3], l_par, data_type=Temperature())
    svg_data = data.to_svg()
    assert len(str(svg_data)) > 300


def test_analysis_geometry_to_svg():
    """Test the translation of an AnalysisGeometry to SVG."""
    path = './tests/epw/chicago.epw'
    epw = EPW(path)

    dbt = epw.dry_bulb_temperature
    data_type, unit = dbt.header.data_type, dbt.header.unit
    base_pt = Point3D(20, -300)
    hourly_plot = HourlyPlot(dbt, base_point=base_pt, x_dim=2, y_dim=8)
    vis_data = VisualizationData(
        hourly_plot.values, hourly_plot.legend_parameters, data_type, unit)
    mesh_geo = AnalysisGeometry(
        'Analysis_Data', [hourly_plot.colored_mesh3d], [vis_data])
    mesh_geo.display_name = data_type.name
    mesh_geo.display_mode = 'Surface'

    svg_data = mesh_geo.to_svg()
    assert len(str(svg_data)) > 3000
    svg_file = svg_data.to_file(name='DryBulb', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)
