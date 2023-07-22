"""Method to draw a RadiationDome as a VisualizationSet."""
from ladybug_geometry.geometry3d import Vector3D, Point3D, Plane

from ladybug_display.geometry3d import DisplayPoint3D, DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def radiation_dome_to_vis_set(radiation_dome, show_components=False, include_title=True):
    """Translate radiation dome geometry into a VisualizationSet.

    Args:
        radiation_dome: A Ladybug-Radiance RadiationDome object.
        show_components: Boolean to indicate whether only one dome with total radiation
            should be displayed (False) or three domes with the solar radiation
            components (total, direct, and diffuse) should be shown. (Default: False).
        include_title: Boolean to note whether the title should be included
            in the output visualization. (Default: True).

    Returns:
        A VisualizationSet with the radiation dome represented as ContextGeometries
        and an AnalysisGeometry. This includes these objects in the following order.

        -   Compass -- A ContextGeometry for the Compass at the base of the dome.

        -   Max_Info -- A ContextGeometry with a Point and text for the maximum
                radiation occurring on the dome.

        -   Title -- A ContextGeometry with text for the title of the dome.
                This layer will be excluded if include_title is False.

        -   Radiation_Data -- An AnalysisGeometry for the radiation dome data.
    """
    # extract properties relevant for the Compass
    cent_pt = radiation_dome.center_point
    radius = radiation_dome.radius
    proj = radiation_dome.projection
    az = radiation_dome.azimuth_count

    # create the dome visualization
    if not show_components:  # only create the total dome mesh
        mesh, compass_obj, dome_graphic, title_txt = radiation_dome.draw()
        compass, title = _translate_context(
            compass_obj, dome_graphic, title_txt, cent_pt, proj, az)
        mesh, title = [mesh], [title]
        mesh_values = radiation_dome.total_values
    else:  # create domes for total, direct and diffuse
        # loop through the 3 radiation types and produce a dome
        mesh, compass, title, mesh_values = [], [], [], []
        rad_types = ('total', 'direct', 'diffuse')
        for dome_i in range(3):
            c_pt = Point3D(cent_pt.x + radius * 3 * dome_i, cent_pt.y, cent_pt.z)
            dome_mesh, dome_compass, dome_graphic, dome_title = \
                radiation_dome.draw(rad_types[dome_i], c_pt)
            compass_con, title_con = _translate_context(
                dome_compass, dome_graphic, dome_title, cent_pt, proj, az)
            mesh.append(dome_mesh)
            compass.extend(compass_con)
            title.append(title_con)
            mesh_values.extend(
                getattr(radiation_dome, '{}_values'.format(rad_types[dome_i])))

    # create the visualization set object
    vis_set = VisualizationSet('RadiationDome', ())
    vis_set.display_name = 'Radiation Dome'

    # create all of the ContextGeometries
    compass_geo = ContextGeometry('Compass', compass) \
        if isinstance(compass, list) else compass
    vis_set.add_geometry(compass_geo)
    if include_title:
        title_geo = ContextGeometry('Title', title)
        vis_set.add_geometry(title_geo)
    m_pt = radiation_dome.max_point
    txt_hgt = dome_graphic.legend_parameters.text_height * 0.5
    max_pt = DisplayPoint3D(m_pt, radius=3)
    m_pl = Plane(o=Point3D(m_pt.x, m_pt.y - txt_hgt * 1.5, m_pt.z + 0.01),
                 n=Vector3D(0, 0, 1))
    max_info = DisplayText3D(
        radiation_dome.max_info, m_pl, txt_hgt, None,
        dome_graphic.legend_parameters.font, 'Center', 'Top')
    max_geo = ContextGeometry('Max_Info', (max_pt, max_info))
    max_geo.display_name = 'Max Info'
    vis_set.add_geometry(max_geo)

    # create the AnalysisGeometry
    vis_data = VisualizationData(
        mesh_values, radiation_dome.legend_parameters,
        dome_graphic.data_type, dome_graphic.unit)
    mesh_geo = AnalysisGeometry(
        'Radiation_Data', mesh, [vis_data])
    mesh_geo.display_name = dome_graphic.data_type.name
    mesh_geo.display_mode = 'Surface'
    vis_set.add_geometry(mesh_geo)

    return vis_set


def _translate_context(compass, graphic, title_txt, cent_pt, projection, az_count):
    """Translate radiation dome geometry into Display geometry objects.

    Args:
        compass: A ladybug Compass object.
        graphic: A GraphicContainer for the dome.
        title_txt: Text for title of the dome.
        cent_pt: The center point of the dome.
        project: Text for the projection of the radiation dome.
        az_count: The number of azimuth directions in the dome.

    Returns:
        dome_compass: A ContextGeometry for the dome compass.
        dome_title: DisplayText3D for the title for the dome.
    """
    dome_angles = list(range(0, 360, int(360 / az_count)))
    start, stop, step, dome_angles = 0, 360, 360 / az_count, []
    while start < stop:
        dome_angles.append(start)
        start += step
    dome_angles = [int(n) for n in dome_angles]
    if len(dome_angles) > 36:
        dome_angles = dome_angles[::2]
    dome_compass = compass.to_vis_set(
        cent_pt.z, dome_angles, projection, graphic.legend_parameters.font)[0]
    dome_title = DisplayText3D(
        title_txt, graphic.lower_title_location,
        graphic.legend_parameters.text_height, None,
        graphic.legend_parameters.font, 'Left', 'Top')
    return dome_compass, dome_title
