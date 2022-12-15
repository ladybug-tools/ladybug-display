"""Method to draw an HourlyPlot as a VisualizationSet."""
from ladybug_geometry.geometry3d import Plane

from ladybug_display.geometry3d import DisplayLineSegment3D, DisplayPolyline3D, \
    DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def hourly_plot_to_vis_set(
        hourly_plot, z=0, custom_hours=(0, 3, 6, 9, 12, 15, 18, 21, 24),
        include_title=True):
    """Get a Ladybug HourlyPlot represented as a VisualizationSet.

    Args:
        hourly_plot: A Ladybug HourlyPlot object.
        z: A number for the Z-coordinate to be used in translation. (Default: 0).
        custom_hours: A tuple of integers from 0 to 24 to indicate which hours
            of the day should appear in the Hour_Axis of the visualization.
            The default is (0, 3, 6, 9, 12, 15, 18, 21, 24).
        include_title: Boolean to note whether the title should be included
            in the output visualization. (Default: True).

    Returns:
        A VisualizationSet with the hourly plot represented several ContextGeometries
        (and an AnalysisGeometry). This includes these objects in the following order.

        -   Hour_Axis -- A ContextGeometry with lines and text for the hour-of-the-day
                axis of the hourly plot.

        -   Month_Axis -- A ContextGeometry with lines and text for the month-of-the-year
                axis of the hourly plot.

        -   Title -- A ContextGeometry with text for the title of the hourly plot.
                This layer will be excluded if include_title is False.

        -   Analysis_Data -- An AnalysisGeometry for the data on the hourly plot.
    """
    # establish the VisualizationSet object
    data_header = hourly_plot.data_collection.header
    data_type, unit = data_header.data_type, data_header.unit
    set_id = 'Hourly_Plot_{}'.format(data_type.name.replace(' ', '_'))
    vis_set = VisualizationSet(set_id, ())

    # get global variables used in other places
    chart_border = DisplayPolyline3D(hourly_plot.chart_border3d, line_width=2)
    txt_h = hourly_plot.legend_parameters.text_height
    font = hourly_plot.legend_parameters.font
    major_hr = hourly_plot.HOUR_LABELS

    # add the hour axis
    dis_hour, dis_hour_text = [], []
    h_lines = hourly_plot.custom_hour_lines3d(custom_hours)
    h_pts = hourly_plot.custom_hour_label_points3d(custom_hours)
    h_text = hourly_plot.custom_hour_labels(custom_hours)
    for hr, lin, pt, txt in zip(custom_hours, h_lines, h_pts, h_text):
        if hr in major_hr:
            lt, t_sz = 'Continuous', txt_h
        else:
            lt, t_sz = 'Dotted', txt_h * 0.8
        dis_hour.append(DisplayLineSegment3D(lin, line_width=1, line_type=lt))
        d_txt = DisplayText3D(txt, Plane(o=pt), t_sz, None, font, 'Right', 'Middle')
        dis_hour_text.append(d_txt)
    hour_axis = ContextGeometry('Hour_Axis', [chart_border] + dis_hour + dis_hour_text)
    hour_axis.display_name = 'Hour Axis'
    vis_set.add_geometry(hour_axis)

    # add the month axis
    dis_month, dis_month_text = [], []
    m_lines = hourly_plot.month_lines3d
    m_pts = hourly_plot.month_label_points3d
    m_text = hourly_plot.month_labels
    for lin in m_lines:
        dis_month.append(DisplayLineSegment3D(lin, line_width=1))
    for pt, txt in zip(m_pts, m_text):
        d_txt = DisplayText3D(txt, Plane(o=pt), t_sz, None, font, 'Center', 'Top')
        dis_month_text.append(d_txt)
    month_axis = ContextGeometry(
        'Month_Axis', [chart_border] + dis_month + dis_month_text)
    month_axis.display_name = 'Month Axis'
    vis_set.add_geometry(month_axis)

    if include_title:
        tit_txt = DisplayText3D(
            hourly_plot.title_text, hourly_plot.lower_title_location, txt_h,
            None, font, 'Left', 'Bottom')
        title = ContextGeometry('Title', [tit_txt])
        title.display_name = 'Title'
        vis_set.add_geometry(title)

    # add the colored mesh
    vis_data = VisualizationData(
        hourly_plot.values, hourly_plot.legend_parameters, data_type, unit)
    mesh_geo = AnalysisGeometry(
        'Analysis_Data', [hourly_plot.colored_mesh3d], [vis_data])
    mesh_geo.display_name = data_type.name
    mesh_geo.display_mode = 'Surface'
    vis_set.add_geometry(mesh_geo)

    return vis_set
