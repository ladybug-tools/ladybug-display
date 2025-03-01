# coding=utf-8
import os

from ladybug_geometry.geometry3d import Point3D
from ladybug.epw import EPW
from ladybug.sunpath import Sunpath

from ladybug_display.geometry3d import DisplayPolyline3D
from ladybug_display.context import ContextGeometry


def test_context_geometry_to_svg():
    """Test the translation of ContextGeometry to SVG."""
    path = './tests/epw/chicago.epw'
    epw = EPW(path)
    sunpath = Sunpath.from_location(epw.location)

    center_point = Point3D(300, -300)
    radius = 250
    ana_plin_1 = sunpath.hourly_analemma_polyline3d(
        center_point, radius, True, False, 1, 6, 4)
    ana_plin_2 = sunpath.hourly_analemma_polyline3d(
        center_point, radius, True, False, 7, 12, 4)
    analemma = [DisplayPolyline3D(pl, line_width=1) for pl in ana_plin_1] + \
        [DisplayPolyline3D(pl, line_width=1, line_type='Dashed')
            for pl in ana_plin_2]
    analemma_geo = ContextGeometry('Analemmas', analemma)

    svg_data = analemma_geo.to_svg()
    assert len(str(svg_data)) > 3000
    svg_file = svg_data.to_file(name='Analemmas', folder='./tests/svg')
    assert os.path.isfile(svg_file)
    os.remove(svg_file)
