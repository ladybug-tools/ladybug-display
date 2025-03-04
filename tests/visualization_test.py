# coding=utf-8
import os
import pytest

from ladybug_geometry.geometry2d import Mesh2D
from ladybug_geometry.geometry3d import Point3D, Plane, Mesh3D, Polyface3D

from ladybug.futil import nukedir
from ladybug.graphic import GraphicContainer
from ladybug.legend import Legend, LegendParameters
from ladybug.color import Colorset
from ladybug.dt import DateTime
from ladybug.epw import EPW
from ladybug.hourlyplot import HourlyPlot
from ladybug.sunpath import Sunpath
from ladybug.windrose import WindRose
from ladybug.psychchart import PsychrometricChart

from ladybug_display.visualization import VisualizationSet, ContextGeometry, \
    AnalysisGeometry, VisualizationData
from ladybug_display.extension.hourlyplot import hourly_plot_to_vis_set
from ladybug_display.extension.sunpath import sunpath_to_vis_set
from ladybug_display.extension.windrose import wind_rose_to_vis_set
from ladybug_display.extension.psychchart import psychrometric_chart_to_vis_set


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


def test_convert_to_units():
    """Test the VisualizationSet convert_to_units method."""
    room = Polyface3D.from_box(120, 240, 96)
    context = ContextGeometry('Building_Massing', [room])
    mesh2d = Mesh2D.from_grid(num_x=2, num_y=2)
    mesh3d = Mesh3D.from_mesh2d(mesh2d)
    data = VisualizationData([-1, 0, 1, 2])
    a_geo = AnalysisGeometry('Test_Results', [mesh3d], [data])

    vis_set = VisualizationSet('Test_Set', [a_geo, context], units='Inches')
    inches_conversion = vis_set._conversion_factor_to_meters('Inches')
    vis_set.convert_to_units('Meters')

    assert vis_set[1][0].volume == \
        pytest.approx(120 * 240 * 96 * (inches_conversion ** 3), rel=1e-3)
    assert vis_set.units == 'Meters'


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


def test_hourly_plot_to_svg():
    """Test the translation of an HourlyPlot VisualizationSet to SVG."""
    path = './tests/epw/chicago.epw'
    epw = EPW(path)
    dbt = epw.dry_bulb_temperature
    l_par = LegendParameters()
    l_par.text_height = 4
    hourly_plot = HourlyPlot(dbt, legend_parameters=l_par)
    vis_set = hourly_plot_to_vis_set(hourly_plot)

    svg_data = vis_set.to_svg(1300, 500, render_3d_legend=True)
    svg_file = svg_data.to_file(name='HourlyPlot', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)


def test_sunpath_to_svg():
    """Test the translation of an Sunpath VisualizationSet to SVG."""
    path = './tests/epw/chicago.epw'
    epw = EPW(path)
    sunpath = Sunpath.from_location(epw.location)
    hoys = [DateTime(3, 2, i).hoy for i in range(24)]
    vis_set = sunpath_to_vis_set(sunpath, hoys=hoys, projection='Stereographic')

    svg_data = vis_set.to_svg(900, 900)
    svg_file = svg_data.to_file(name='Sunpath', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)


def test_interactive_sunpath_to_svg():
    """Test the translation of an Sunpath VisualizationSet to interactive SVG."""
    path = './tests/epw/chicago.epw'
    epw = EPW(path)
    dbt = epw.dry_bulb_temperature
    sunpath = Sunpath.from_location(epw.location)
    hoys = [DateTime(3, 2, i).hoy for i in range(24)]
    vis_set = sunpath_to_vis_set(sunpath, hoys=hoys, data=[dbt],
                                 projection='Stereographic')

    svg_data = vis_set.to_svg(900, 900, interactive=True, render_3d_legend=True)
    svg_file = svg_data.to_file(name='Sunpath_Interact', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)


def test_wind_rose_to_svg():
    """Test the translation of an WindRose VisualizationSet to SVG."""
    path = './tests/epw/chicago.epw'
    epw = EPW(path)
    speed, direction = epw.wind_speed, epw.wind_direction
    wind_rose = WindRose(direction, speed, 36)
    wind_rose.frequency_hours = 50
    wind_rose.show_zeros = True
    l_par = LegendParameters(min=0, max=10, colors=Colorset.parula())
    wind_rose.legend_parameters = l_par
    vis_set = wind_rose_to_vis_set(wind_rose)

    svg_data = vis_set.to_svg(900, 750, render_3d_legend=True)
    svg_file = svg_data.to_file(name='WindRose', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)


def test_psych_chart_to_svg():
    """Test the translation of an Psy VisualizationSet to SVG."""
    path = './tests/epw/chicago.epw'
    epw = EPW(path)
    dbt, rh = epw.dry_bulb_temperature, epw.relative_humidity
    psych_chart = PsychrometricChart(
        dbt, rh, max_temperature=40, max_humidity_ratio=0.025)
    vis_set = psychrometric_chart_to_vis_set(psych_chart)

    svg_data = vis_set.to_svg(1200, 700, interactive=True, render_3d_legend=True)
    svg_file = svg_data.to_file(name='PsychChart', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)


def test_sunpath_axon_to_svg():
    """Test the translation of an Sunpath VisualizationSet to SVG with an Axon view."""
    path = './tests/epw/chicago.epw'
    epw = EPW(path)
    sunpath = Sunpath.from_location(epw.location)
    hoys = [DateTime(3, 2, i).hoy for i in range(24)]
    vis_set = sunpath_to_vis_set(sunpath, hoys=hoys)

    svg_data = vis_set.to_svg(1200, 1000, view='SE')
    svg_file = svg_data.to_file(name='Sunpath_Axon', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)


def test_daylight_study_to_svg():
    """Test the translation of an a daylight VisualizationSet to SVG with an Axon view."""
    path = './tests/vsf/classroom.vsf'
    vis_set = VisualizationSet.from_file(path)
    vis_set.geometry = (vis_set[-1],) + vis_set[:-1]
    data_i = vis_set.geometry[-1].active_data
    vis_set.geometry[-1][data_i].legend_parameters.vertical = False
    vis_set.geometry[-1][data_i].legend_parameters.decimal_count = 0
    vis_set.geometry[-1][data_i].legend_parameters.title = \
        'Useful Daylight Illuminance (%)'

    svg_data = vis_set.to_svg(1200, 1000, interactive=True,
                              view='SE', render_2d_legend=True)
    svg_file = svg_data.to_file(name='Daylight_Study', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)
