"""Method to draw a RadiationDome as a VisualizationSet."""
from ladybug_geometry.bounding import bounding_box
from ladybug_geometry.geometry3d import Mesh3D
from ladybug.color import Colorset, Color
from ladybug.legend import LegendParameters
from ladybug.graphic import GraphicContainer
from ladybug.datatype.energyintensity import Radiation
from ladybug.datatype.energyflux import Irradiance

from ladybug_display.geometry3d import DisplayText3D, DisplayMesh3D, DisplayFace3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def radiation_study_to_vis_set(
        radiation_study, legend_parameters=None, plot_irradiance=False,
        include_title=True, include_context=False):
    """Translate radiation study into a VisualizationSet.

    Args:
        radiation_study: A Ladybug-Radiance RadiationStudy object.
        legend_parameters: An optional LegendParameter object to change the display
            of the radiation study. If None, default legend parameters will be
            used. (Default: None).
        plot_irradiance: Boolean to note whether the results should be plotted
            with units of total Radiation (kWh/m2) [False] or with units of average
            Irradiance (W/m2) [True]. (Default: False).
        include_title: Boolean to note whether the title should be included
            in the output visualization. (Default: True).
        include_context: Boolean to note whether the context geometry should be
            included in the output visualization. (Default: False).

    Returns:
        A VisualizationSet with the radiation study represented as an
        AnalysisGeometry. This includes these objects in the following order.

        -   Radiation_Data -- An AnalysisGeometry for the radiation data.

        -   Title -- A ContextGeometry with text for the title of the study.
                This layer will be excluded if include_title is False.

        -   Context_Geometry -- A ContextGeometry with the shading context used
                in the study. This layer will be excluded when include_context is False.
    """
    # get the radiation data
    if plot_irradiance:
        d_type, unit, title = Irradiance(), 'W/m2', 'Incident Irradiance'
        rad_data = radiation_study.irradiance_values
    else:
        d_type, unit, title = Radiation(), 'kWh/m2', 'Incident Radiation'
        rad_data = radiation_study.radiation_values
    if radiation_study.is_benefit:
        title = '{} Benefit/Harm'.format(title)

    # process the legend parameters and override the legend colors
    if legend_parameters is not None:
        assert isinstance(legend_parameters, LegendParameters), \
            'Expected LegendParameters. Got {}.'.format(type(legend_parameters))
        l_par = legend_parameters.duplicate()
    else:
        l_par = LegendParameters()
    if radiation_study.is_benefit:
        if l_par.min is None:
            l_par.min = min((min(rad_data), -max(rad_data)))
        if l_par.max is None:
            l_par.max = max((-min(rad_data), max(rad_data)))
        if l_par.are_colors_default:
            l_par.colors = reversed(Colorset.benefit_harm())
    else:
        if l_par.min is None:
            l_par.min = 0
        if l_par.max is None:
            l_par.max = max(rad_data)

    # create the visualization set object
    vis_set = VisualizationSet('RadiationStudy', ())
    vis_set.display_name = 'Radiation Study'

    # create the AnalysisGeometry
    vis_data = VisualizationData(rad_data, l_par, d_type, unit)
    mesh_geo = AnalysisGeometry(
        'Radiation_Data', [radiation_study.study_mesh], [vis_data])
    mesh_geo.display_name = 'Radiation Data'
    mesh_geo.display_mode = 'Surface'
    vis_set.add_geometry(mesh_geo)

    # create the ContextGeometry for the title
    if include_title:
        all_geo = (radiation_study.study_mesh,) + radiation_study.context_geometry
        min_pt, max_pt = bounding_box(all_geo)
        graphic = GraphicContainer(
            rad_data, min_pt, max_pt, l_par, d_type, unit)
        study_title = DisplayText3D(
            title, graphic.lower_title_location,
            graphic.legend_parameters.text_height, None,
            graphic.legend_parameters.font, 'Left', 'Top')
        title_geo = ContextGeometry('Title', [study_title])
        vis_set.add_geometry(title_geo)

    # create the ContextGeometry for the context
    if include_context:
        con_color = Color(125, 125, 125, 125)
        con_geos = []
        for geo in radiation_study.context_geometry:
            if isinstance(geo, Mesh3D):
                con_geos.append(DisplayMesh3D(geo, con_color))
            else:  # it's a Face3D
                con_geos.append(DisplayFace3D(geo, con_color))
        context_geo = ContextGeometry('Context_Geometry', con_geos)
        context_geo.display_name = 'Context Geometry'
        vis_set.add_geometry(context_geo)

    return vis_set
