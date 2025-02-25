# coding=utf-8
from ladybug.datatype.temperature import Temperature
from ladybug.legend import LegendParameters
from ladybug_display.analysis import VisualizationData


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
