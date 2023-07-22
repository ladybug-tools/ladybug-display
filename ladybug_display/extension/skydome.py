"""Method to draw a SkyDome as a VisualizationSet."""
from ladybug_geometry.geometry3d.pointvector import Point3D

from ladybug_display.geometry3d import DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def sky_dome_to_vis_set(sky_dome, show_components=False, include_title=True):
    """Translate sky dome geometry into a VisualizationSet.

    Args:
        sky_dome: A Ladybug-Radiance SkyDome object.
        show_components: Boolean to indicate whether only one dome with total radiation
            should be displayed (False) or three domes with the solar radiation
            components (total, direct, and diffuse) should be shown. (Default: False).
        include_title: Boolean to note whether the title should be included
            in the output visualization. (Default: True).

    Returns:
        A VisualizationSet with the sky dome represented as ContextGeometries
        and an AnalysisGeometry. This includes these objects in the following order.

        -   Compass -- A ContextGeometry for the Compass at the base of the sky dome.

        -   Title -- A ContextGeometry with text for the title of the sky dome.
                This layer will be excluded if include_title is False.

        -   Radiation_Data -- An AnalysisGeometry for the sky dome data.
    """
    # extract properties relevant for the Compass
    cent_pt, radius, proj = sky_dome.center_point, sky_dome.radius, sky_dome.projection

    # create the dome visualization
    if not show_components:  # only create the total dome mesh
        mesh, compass_obj, dome_graphic, title_txt, mesh_values = sky_dome.draw()
        compass, title = _translate_context(
            compass_obj, dome_graphic, title_txt, cent_pt, proj)
        mesh, title = [mesh], [title]
    else:  # create domes for total, direct and diffuse
        # loop through the 3 radiation types and produce a dome
        mesh, compass, title, mesh_values = [], [], [], []
        rad_types = ('total', 'direct', 'diffuse')
        for dome_i in range(3):
            c_pt = Point3D(cent_pt.x + radius * 3 * dome_i, cent_pt.y, cent_pt.z)
            dome_mesh, dome_compass, dome_graphic, dome_title, dome_values = \
                sky_dome.draw(rad_types[dome_i], c_pt)
            compass_con, title_con = _translate_context(
                dome_compass, dome_graphic, dome_title, cent_pt, proj)
            mesh.append(dome_mesh)
            compass.extend(compass_con)
            title.append(title_con)
            mesh_values.extend(dome_values)

    # create the visualization set object
    vis_set = VisualizationSet('SkyDome', ())
    vis_set.display_name = 'Sky Dome'

    # merge all of the ContextGeometries
    compass_geo = ContextGeometry('Compass', compass) \
        if isinstance(compass, list) else compass
    vis_set.add_geometry(compass_geo)
    if include_title:
        title_geo = ContextGeometry('Title', title)
        vis_set.add_geometry(title_geo)

    # create the AnalysisGeometry
    vis_data = VisualizationData(
        mesh_values, sky_dome.legend_parameters,
        dome_graphic.data_type, dome_graphic.unit)
    mesh_geo = AnalysisGeometry(
        'Radiation_Data', mesh, [vis_data])
    mesh_geo.display_name = dome_graphic.data_type.name
    mesh_geo.display_mode = 'Surface'
    vis_set.add_geometry(mesh_geo)

    return vis_set


def _translate_context(compass, graphic, title_txt, cent_pt, projection):
    """Translate sky dome geometry into Display geometry objects.

    Args:
        compass: A ladybug Compass object.
        graphic: A GraphicContainer for the dome.
        title_txt: Text for title of the dome.
        cent_pt: The center point of the sky dome.
        project: Text for the projection of the sky dome.

    Returns:
        dome_compass: A ContextGeometry for the dome compass.
        dome_title: DisplayText3D for the title for the dome.
    """
    dome_compass = compass.to_vis_set(
        cent_pt.z, None, projection, graphic.legend_parameters.font)[0]
    dome_title = DisplayText3D(
        title_txt, graphic.lower_title_location,
        graphic.legend_parameters.text_height, None,
        graphic.legend_parameters.font, 'Left', 'Top')
    return dome_compass, dome_title
