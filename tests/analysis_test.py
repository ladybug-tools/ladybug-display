# coding=utf-8
from ladybug.datatype.temperature import Temperature
from ladybug_display.analysis import VisualizationData


def test_init_visualization_data_to_svg():
    """Test the translation of VisualizationData to SVG."""
    data = VisualizationData([0, 1, 2, 3], data_type=Temperature())
    svg_data = data.to_svg()
    print(svg_data)
