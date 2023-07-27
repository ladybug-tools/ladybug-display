"""Method to draw a RadiationDome as a VisualizationSet."""
from ladybug_geometry.bounding import bounding_box
from ladybug_geometry.geometry3d import Mesh3D
from ladybug.color import Colorset, Color
from ladybug.legend import LegendParameters
from ladybug.graphic import GraphicContainer
from ladybug.datatype.time import Time

from ladybug_display.geometry3d import DisplayText3D, DisplayMesh3D, DisplayFace3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def direct_sun_study_to_vis_set(
        direct_sun_study, legend_parameters=None,
        include_title=True, include_context=False):
    """Translate direct sun study into a VisualizationSet.

    Args:
        direct_sun_study: A Ladybug-Radiance DirectSunStudy object.
        legend_parameters: An optional LegendParameter object to change the display
            of the direct sun study. If None, default legend parameters will be
            used. (Default: None).
        include_title: Boolean to note whether the title should be included
            in the output visualization. (Default: True).
        include_context: Boolean to note whether the context geometry should be
            included in the output visualization. (Default: False).

    Returns:
        A VisualizationSet with the direct sun study represented as an
        AnalysisGeometry. This includes these objects in the following order.

        -   Direct_Sun_Data -- An AnalysisGeometry for the direct sun data.

        -   Title -- A ContextGeometry with text for the title of the study.
                This layer will be excluded if include_title is False.
        
        -   Context_Geometry -- A ContextGeometry with the shading context used
                in the study. This layer will be excluded when include_context is False.
    """
    # process the legend parameters and override the legend colors
    if legend_parameters is not None:
        assert isinstance(legend_parameters, LegendParameters), \
            'Expected LegendParameters. Got {}.'.format(type(legend_parameters))
        l_par = legend_parameters.duplicate()
    else:
        l_par = LegendParameters()
    if l_par.are_colors_default:
        l_par.colors = Colorset.ecotect()

    # create the visualization set object
    vis_set = VisualizationSet('DirectSunStudy', ())
    vis_set.display_name = 'Direct Sun Study'
    d_type, unit = Time(), 'hr'
    sun_data = direct_sun_study.direct_sun_hours

    # create the AnalysisGeometry
    vis_data = VisualizationData(sun_data, l_par, d_type, unit)
    mesh_geo = AnalysisGeometry(
        'Direct_Sun_Data', [direct_sun_study.study_mesh], [vis_data])
    mesh_geo.display_name = 'Direct Sun Data'
    mesh_geo.display_mode = 'Surface'
    vis_set.add_geometry(mesh_geo)

    # create the ContextGeometry for the title
    if include_title:
        all_geo = (direct_sun_study.study_mesh,) + direct_sun_study.context_geometry
        min_pt, max_pt = bounding_box(all_geo)
        graphic = GraphicContainer(
            sun_data, min_pt, max_pt, l_par, d_type, unit)
        study_title = DisplayText3D(
            'Direct Sun Hours', graphic.lower_title_location,
            graphic.legend_parameters.text_height, None,
            graphic.legend_parameters.font, 'Left', 'Top')
        title_geo = ContextGeometry('Title', [study_title])
        vis_set.add_geometry(title_geo)

    # create the ContextGeometry for the context
    if include_context:
        con_color = Color(125, 125, 125, 125)
        con_geos = []
        for geo in direct_sun_study.context_geometry:
            if isinstance(geo, Mesh3D):
                con_geos.append(DisplayMesh3D(geo, con_color))
            else:  # it's a Face3D
                con_geos.append(DisplayFace3D(geo, con_color))
        context_geo = ContextGeometry('Context_Geometry', con_geos)
        context_geo.display_name = 'Context Geometry'
        vis_set.add_geometry(context_geo)

    return vis_set
