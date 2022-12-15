"""Method to draw an MonthlyChart as a VisualizationSet."""
from ladybug_geometry.geometry3d import Point3D, Plane, LineSegment3D, Polyline3D, \
    Mesh3D

from ladybug_display.geometry3d import DisplayLineSegment3D, DisplayPolyline3D, \
    DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def monthly_chart_to_vis_set(
        monthly_chart, z=0, time_marks=False, global_title=None, y_axis_title=None):
    """Get a Ladybug MonthlyChart represented as a VisualizationSet.

    Args:
        monthly_chart: A Ladybug MonthlyChart object.
        z: A number for the Z-coordinate to be used in translation. (Default: 0).
        time_marks: Boolean to note whether the month labels should be replaced with
            marks for the time of day in each month. This is useful for displaying
            hourly data, particularly when the input data is only for a month
            and not the whole year.
        global_title: A text string to label the entire entire chart.  It will be
            displayed in the lower left of the output chart. If None, the
            default is to display the metadata of the chart data.
        y_axis_title: A text string to label the Y-axis of the chart. This can
            also be a list of 2 Y-axis titles if there are two different types
            of data plotted on the chart and there are two axes labels on either
            side of the chart.  The default will display the data type and
            units of the plotted data.

    Returns:
        A VisualizationSet with the monthly chart represented several ContextGeometries
        (and an AnalysisGeometry). This includes these objects in the following order.

        -   X_Axis -- A ContextGeometry with lines and text for the X axis of
                the monthly chart.

        -   Y_Axis -- A ContextGeometry with lines and text for the Y axis of
                the monthly chart.

        -   Y_Axis2 -- A ContextGeometry with lines and text for the second Y axis
                of the monthly chart.

        -   Title -- A ContextGeometry with text for the title of the monthly chart.

        -   Data_Outlines -- A ContextGeometry with a list of polylines that outline
                the input data. These will represent the average or total at
                each hour whenever the input data is hourly or monthly-per-hour data.

        -   Analysis_Data -- An AnalysisGeometry for the data on the monthly chart.
    """
    # establish the VisualizationSet object
    data_header = monthly_chart.data_collections[0].header
    data_type = data_header.data_type
    set_id = 'Monthly_Chart_{}'.format(data_type.name.replace(' ', '_'))
    vis_set = VisualizationSet(set_id, ())

    # get values used througout the translation
    txt_hgt = monthly_chart.legend_parameters.text_height
    font = monthly_chart.legend_parameters.font
    x_dim = monthly_chart.x_dim
    bp = Plane(o=Point3D(0, 0, z))

    # add the X axis
    border = Polyline3D.from_polyline2d(monthly_chart.chart_border, bp)
    x_geo = [DisplayPolyline3D(border, line_width=2)]
    for line in monthly_chart.month_lines:
        line3d = LineSegment3D.from_line_segment2d(line, z)
        x_geo.append(DisplayLineSegment3D(line3d))
    if time_marks:
        txt_h = x_dim / 20 if x_dim / 20 < txt_hgt * 0.75 else txt_hgt * 0.75
        for txt, pt in zip(monthly_chart.time_labels, monthly_chart.time_label_points):
            t_pln = Plane(o=Point3D(pt.x, pt.y, z))
            txt_obj = DisplayText3D(txt, t_pln, txt_h, None, font, 'Center', 'Top')
            x_geo.append(txt_obj)
        for line in monthly_chart.time_ticks:
            line3d = LineSegment3D.from_line_segment2d(line, z)
            x_geo.append(DisplayLineSegment3D(line3d))
    else:
        for txt, pt in zip(monthly_chart.month_labels, monthly_chart.month_label_points):
            t_pln = Plane(o=Point3D(pt.x, pt.y, z))
            txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Center', 'Top')
            x_geo.append(txt_obj)
    x_axis = ContextGeometry('X_Axis', x_geo)
    x_axis.display_name = 'X Axis'
    vis_set.add_geometry(x_axis)

    # add the y axis
    y_geo = []
    for line in monthly_chart.y_axis_lines:
        line3d = LineSegment3D.from_line_segment2d(line, z)
        y_geo.append(DisplayLineSegment3D(line3d, line_type='Dashed'))
    if y_axis_title is None or len(y_axis_title) == 0:
        y1_txt = monthly_chart.y_axis_title_text1
    else:
        y1_txt = y_axis_title if isinstance(y_axis_title, str) else y_axis_title[0]
    y_pl = monthly_chart.y_axis_title_location1
    if z != 0:
        y_pl = Plane(n=y_pl.n, o=Point3D(y_pl.o.x, y_pl.o.y, z), x=y_pl.x)
    y_title = DisplayText3D(y1_txt, y_pl, txt_hgt, None, font)
    y_geo.append(y_title)
    for txt, pt in zip(monthly_chart.y_axis_labels1, monthly_chart.y_axis_label_points1):
        t_pln = Plane(o=Point3D(pt.x, pt.y, z))
        txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Right', 'Middle')
        y_geo.append(txt_obj)
    y_axis = ContextGeometry('Y_Axis', y_geo)
    y_axis.display_name = y1_txt
    vis_set.add_geometry(y_axis)

    # add the second y axis if it exists
    if monthly_chart.y_axis_title_text2 is not None:
        y2_geo = []
        if y_axis_title is None or len(y_axis_title) <= 1:
            y2_txt = monthly_chart.y_axis_title_text2
        else:
            y2_txt = monthly_chart.y_axis_title_text2 \
                if isinstance(y_axis_title, str) else y_axis_title[1]
        y2_pl = monthly_chart.y_axis_title_location2
        if z != 0:
            y2_pl = Plane(n=y2_pl.n, o=Point3D(y2_pl.o.x, y2_pl.o.y, z), x=y2_pl.x)
        y_title2 = DisplayText3D(y2_txt, y2_pl, txt_hgt, None, font)
        y2_geo.append(y_title2)
        y2_label_pts = monthly_chart.y_axis_label_points2
        for txt, pt in zip(monthly_chart.y_axis_labels2, y2_label_pts):
            t_pln = Plane(o=Point3D(pt.x, pt.y, z))
            txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Left', 'Middle')
            y2_geo.append(txt_obj)
        y2_axis = ContextGeometry('Y_Axis2', y2_geo)
        y2_axis.display_name = y2_txt
        vis_set.add_geometry(y2_axis)

    # add the title
    title_txt = monthly_chart.title_text if global_title is None else global_title
    ttl_pl = monthly_chart.lower_title_location
    if z != 0:
        ttl_pl = Plane(n=ttl_pl.n, o=Point3D(ttl_pl.o.x, ttl_pl.o.y, z), x=ttl_pl.x)
    title = DisplayText3D(title_txt, ttl_pl, txt_hgt, None, font)
    title_obj = ContextGeometry('Title', [title])
    vis_set.add_geometry(title_obj)

    # add the analysis geometry
    legend = monthly_chart.legend
    if monthly_chart.time_interval == 'MonthlyPerHour':
        data_lines = [Polyline3D.from_polyline2d(line, bp)
                      for line in monthly_chart.data_polylines]
        month_count = len(data_lines) / len(monthly_chart.data_collections)
        data_vals = [int(i / month_count) for i, pline in enumerate(data_lines)]
        vis_data = VisualizationData(data_vals, legend.legend_parameters)
        a_geo = AnalysisGeometry('Analysis_Data', data_lines, [vis_data])
    else:
        d_meshes = monthly_chart.data_meshes
        data_mesh = [Mesh3D.from_mesh2d(msh, bp) for msh in d_meshes]
        vis_data = VisualizationData(legend.values, legend.legend_parameters)
        a_geo = AnalysisGeometry('Analysis_Data', data_mesh, [vis_data])
        if monthly_chart.time_interval == 'Monthly':
            a_geo.display_mode = 'SurfaceWithEdges'
        elif monthly_chart.time_interval == 'Daily':
            a_geo.display_mode = 'Surface'
        else:
            out_geo = []
            for line in monthly_chart.data_polylines:
                line3d = Polyline3D.from_polyline2d(line, bp)
                out_geo.append(DisplayPolyline3D(line3d))
            data_outline = ContextGeometry('Data_Outlines', out_geo)
            data_outline.display_name = 'Data Outlines'
            vis_set.add_geometry(data_outline)
    vis_set.add_geometry(a_geo)

    return vis_set
