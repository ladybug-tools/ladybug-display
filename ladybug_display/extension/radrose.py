"""Method to draw a RadiationRose as a VisualizationSet."""
from ladybug_geometry.geometry3d import Point3D

from ladybug_display.geometry3d import DisplayLineSegment3D, DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def radiation_rose_to_vis_set(
        radiation_rose, max_rad=None, show_components=False, include_title=True):
    """Translate radiation rose geometry into a format suitable for Rhino.

    Args:
        radiation_rose: A Ladybug-Radiance RadiationRose object.
        max_rad: An optional number to set the level of radiation or irradiance
            associated with the full radius of the rose. If None, this is
            determined by the maximum level of radiation in the input data
            but a number can be specified here to fix this at a specific value.
            This is particularly useful when comparing different roses to one
            another. (Default: None).
        show_components: Boolean to indicate whether only one rose with total radiation
            should be displayed (False) or three roses with the solar radiation
            components (total, direct, and diffuse) should be shown. (Default: False).
        include_title: Boolean to note whether the title should be included
            in the output visualization. (Default: True).

    Returns:
        A VisualizationSet with the radiation rose represented as ContextGeometries
        and an AnalysisGeometry. This includes these objects in the following order.

        -   Compass -- A ContextGeometry for the Compass at the base of the rose.

        -   Orientation_Lines -- A ContextGeometry with lines representing the
                edges (or "spokes") of the wind rose directions.

        -   Title -- A ContextGeometry with text for the title of the rose.
                This layer will be excluded if include_title is False.

        -   Radiation_Data -- An AnalysisGeometry for the radiation rose data.
    """
    # extract properties relevant for the Compass
    cent_pt = radiation_rose.center_point
    radius = radiation_rose.radius
    d_count = radiation_rose.direction_count

    # create the rose visualization
    if not show_components:  # only create the total rose mesh
        mesh, orient, compass_obj, rose_graphic, title_txt = \
            radiation_rose.draw(max_rad=max_rad)
        compass, orient_lines, title = _translate_context(
            compass_obj, orient, rose_graphic, title_txt, cent_pt, d_count)
        mesh, title = [mesh], [title]
        mesh_values = radiation_rose.total_values
    else:  # create roses for total, direct and diffuse
        # loop through the 3 radiation types and produce a rose
        mesh, orient_lines, compass, title, mesh_values = [], [], [], [], []
        rad_types = ('total', 'direct', 'diffuse')
        for rose_i in range(3):
            c_pt = Point3D(cent_pt.x + radius * 3 * rose_i, cent_pt.y, cent_pt.z)
            rose_mesh, orient, rose_compass, rose_graphic, rose_title = \
                radiation_rose.draw(rad_types[rose_i], c_pt, max_rad=max_rad)
            compass_con, orient_con, title_con = _translate_context(
                rose_compass, orient, rose_graphic, rose_title, cent_pt, d_count)
            mesh.append(rose_mesh)
            orient_lines.extend(orient_con)
            compass.extend(compass_con)
            title.append(title_con)
            mesh_values.extend(
                getattr(radiation_rose, '{}_values'.format(rad_types[rose_i])))

    # create the visualization set object
    vis_set = VisualizationSet('RadiationRose', ())
    vis_set.display_name = 'Radiation Rose'

    # create all of the ContextGeometries
    compass_geo = ContextGeometry('Compass', compass) \
        if isinstance(compass, list) else compass
    vis_set.add_geometry(compass_geo)
    orient_geo = ContextGeometry('Orientation_Lines', orient_lines)
    vis_set.display_name = 'Orientation Lines'
    vis_set.add_geometry(orient_geo)
    if include_title:
        title_geo = ContextGeometry('Title', title)
        vis_set.add_geometry(title_geo)

    # create the AnalysisGeometry
    vis_data = VisualizationData(
        mesh_values, radiation_rose.legend_parameters,
        rose_graphic.data_type, rose_graphic.unit)
    mesh_geo = AnalysisGeometry(
        'Radiation_Data', mesh, [vis_data])
    mesh_geo.display_name = rose_graphic.data_type.name
    mesh_geo.display_mode = 'Surface'
    vis_set.add_geometry(mesh_geo)

    return vis_set


def _translate_context(compass, dir_lines, graphic, title_txt, cent_pt, dir_count):
    """Translate radiation rose geometry into Display geometry objects.

    Args:
        compass: A ladybug Compass object.
        dir_lines: Line segments for each of the directions plotted on the rose.
        graphic: A GraphicContainer for the rose.
        title_txt: Text for title of the rose.
        cent_pt: The center point of the sky rose.
        dir_count: The number of directions in the rose.

    Returns:
        rose_compass: A ContextGeometry for the rose compass.
        rose_lines: DisplayLineSegment3D for the directions of the rose.
        rose_title: DisplayText3D for the title for the rose.
    """
    rose_angles = list(range(0, 360, int(360 / dir_count)))
    start, stop, step, rose_angles = 0, 360, 360 / dir_count, []
    while start < stop:
        rose_angles.append(start)
        start += step
    rose_angles = [int(n) for n in rose_angles]
    if len(rose_angles) > 36:
        rose_angles = rose_angles[::2]
    rose_compass = compass.to_vis_set(
        cent_pt.z, rose_angles, None, graphic.legend_parameters.font)[0]
    rose_lines = [DisplayLineSegment3D(lin, line_width=1, line_type='Dotted')
                  for lin in dir_lines]
    rose_title = DisplayText3D(
        title_txt, graphic.lower_title_location,
        graphic.legend_parameters.text_height, None,
        graphic.legend_parameters.font, 'Left', 'Top')
    return rose_compass, rose_lines, rose_title
