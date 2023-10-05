"""Method to draw an AdaptiveChart as a VisualizationSet."""
from ladybug_geometry.geometry2d import Polyline2D
from ladybug_geometry.geometry3d import Vector3D, Point3D, Plane, LineSegment3D, \
    Polyline3D, Mesh3D
from ladybug.datatype.time import Time
from ladybug.legend import LegendParameters

from ladybug_display.geometry3d import DisplayLineSegment3D, DisplayPolyline3D, \
    DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def adaptive_chart_to_vis_set(
        adaptive_chart, data=None, legend_parameters=None, z=0):
    """Get a Ladybug AdaptiveChart represented as a VisualizationSet.

    Args:
        adaptive_chart: A Ladybug AdaptiveChart object.
        data: An optional list of data collection objects, which are aligned with
            the prevailing and operative temperature values of the chart. and will
            generate additional colored AnalysisGeometries on the chart.
        legend_parameters: An optional LegendParameter object or list of LegendParameter
            objects to customize the display of the data on the adaptive
            chart. Note that this relates only to the data supplied as input
            for this method and, to customize the display of the time/frequency
            mesh, the AdaptiveChart's native legend_parameters should be
            edited. If a list is used here, this should align with the input data
            (one legend parameter per data collection).
        z: A number for the Z-coordinate to be used in translation. (Default: 0).

    Returns:
        A VisualizationSet with the adaptive chart represented several
        ContextGeometries and an AnalysisGeometry. This includes these objects
        in the following order.

        -   Title -- A ContextGeometry for the title and border around the
                adaptive chart.

        -   Prevailing_Axis -- A ContextGeometry with lines and text for the
                Prevailing Outdoor Temperature (X) axis of the adaptive chart.

        -   Operative_Axis -- A ContextGeometry with lines and text for the
                Indoor Operative Temperature (Y) axis of the adaptive chart.

        -   Comfort_Polygon -- A ContextGeometry with lines for the comfort polygon
                and neutral temperature of the adaptive chart.

        -   Analysis_Data -- An AnalysisGeometry for the data on the adaptive
                chart. This will include multiple data sets if the data input
                is provided.
    """
    # establish the VisualizationSet object
    vis_set = VisualizationSet('Adaptive_Chart', ())
    vis_set.display_name = 'Adaptive Chart'

    # get values used throughout the translation
    txt_hgt = adaptive_chart.legend_parameters.text_height
    font = adaptive_chart.legend_parameters.font
    bp = Plane(o=Point3D(0, 0, z))

    # add the title and border
    meta_i = adaptive_chart.operative_temperature.header.metadata.items()
    title_items = ['Adaptive Chart', 'Time [hr]'] + \
        ['{}: {}'.format(k, v) for k, v in meta_i]
    ttl_pl = adaptive_chart.container.lower_title_location.move(
        Vector3D(0, -txt_hgt * 3))
    if z != 0:
        ttl_pl = Plane(n=ttl_pl.n, o=Point3D(ttl_pl.o.x, ttl_pl.o.y, z), x=ttl_pl.x)
    ttl_txt = DisplayText3D(
        '\n'.join(title_items), ttl_pl, txt_hgt * 1.5, None, font, 'Left', 'Top')
    border_geo = Polyline3D.from_polyline2d(
        Polyline2D.from_polygon(adaptive_chart.chart_border), bp)
    title_objs = [ttl_txt, DisplayPolyline3D(border_geo, line_width=2)]
    title = ContextGeometry('Title', title_objs)
    vis_set.add_geometry(title)

    # add the prevailing temperature axis
    tm_pl = _plane_from_point(adaptive_chart.x_axis_location, z)
    temp_txt = DisplayText3D(
        adaptive_chart.x_axis_text, tm_pl, txt_hgt * 1.5, None, font, 'Center', 'Top')
    temp_geo = [temp_txt]
    for tl in adaptive_chart.prevailing_lines:
        tl_geo = LineSegment3D.from_line_segment2d(tl, z)
        temp_geo.append(DisplayLineSegment3D(tl_geo, line_type='Dotted'))
    tl_pts = adaptive_chart.prevailing_label_points
    for txt, pt in zip(adaptive_chart.prevailing_labels, tl_pts):
        t_pln = Plane(o=Point3D(pt.x, pt.y, z))
        txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Center', 'Top')
        temp_geo.append(txt_obj)
    temp_axis = ContextGeometry('Prevailing_Axis', temp_geo)
    temp_axis.display_name = 'Prevailing Axis'
    vis_set.add_geometry(temp_axis)

    # add the operative temperature axis
    op_pl = _plane_from_point(adaptive_chart.y_axis_location, z, Vector3D(0, 1))
    op_txt = DisplayText3D(
        adaptive_chart.y_axis_text, op_pl, txt_hgt * 1.5, None, font, 'Center', 'Top')
    op_geo = [op_txt]
    for hl in adaptive_chart.operative_lines:
        hl_geo = LineSegment3D.from_line_segment2d(hl, z)
        op_geo.append(DisplayLineSegment3D(hl_geo, line_type='Dotted'))
        op_pts = adaptive_chart.operative_label_points
    for txt, pt in zip(adaptive_chart.operative_labels, op_pts):
        t_pln = Plane(o=Point3D(pt.x, pt.y, z))
        txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Left', 'Middle')
        op_geo.append(txt_obj)
    op_axis = ContextGeometry('Operative_Axis', op_geo)
    op_axis.display_name = 'Operative Axis'
    vis_set.add_geometry(op_axis)

    # add the comfort polygon
    poly_geo = []
    neutral_geo = Polyline3D.from_polyline2d(
        Polyline2D.from_polygon(adaptive_chart.comfort_polygon), bp)
    poly_geo.append(DisplayPolyline3D(neutral_geo, line_width=3))
    neutral_geo = Polyline3D.from_polyline2d(adaptive_chart.neutral_polyline, bp)
    poly_geo.append(DisplayPolyline3D(neutral_geo, line_width=1))
    comf_poly = ContextGeometry('Comfort_Polygon', poly_geo)
    comf_poly.display_name = 'Comfort Polygon'
    vis_set.add_geometry(comf_poly)

    # add the analysis geometry
    # ensure 3D legend defaults are overridden to make the data readable
    l_par = adaptive_chart.legend.legend_parameters.duplicate()
    l_par.base_plane = l_par.base_plane
    l_par.segment_height = l_par.segment_height
    l_par.segment_width = l_par.segment_width
    # gather all of the visualization data sets
    vis_data = [VisualizationData(adaptive_chart.hour_values, l_par, Time(), 'hr')]
    if data is not None and len(data) != 0:
        if legend_parameters is None:
            l_pars = [LegendParameters()] * len(data)
        elif isinstance(legend_parameters, LegendParameters):
            l_pars = [legend_parameters] * len(data)
        else:  # assume it's a list that aligns with the data
            l_pars = legend_parameters
        for dat, lp in zip(data, l_pars):
            # process the legend parameters
            lp = lp.duplicate()
            if lp.is_base_plane_default:
                lp.base_plane = l_par.base_plane
            if lp.is_segment_height_default:
                lp.segment_height = l_par.segment_height
            if lp.is_segment_width_default:
                lp.segment_width = l_par.segment_width
            # check to be sure the data collection aligns
            d_vals = dat.values
            _tp_values = adaptive_chart.prevailing_outdoor_temperature.values
            _to_values = adaptive_chart.operative_temperature.values
            # create a matrix with a tally of the hours for all the data
            base_mtx = [[[] for val in adaptive_chart._tp_category]
                        for rh in adaptive_chart._to_category]
            for tp, to, val in zip(_tp_values, _to_values, d_vals):
                if tp < adaptive_chart._min_prevailing or \
                        tp > adaptive_chart._max_prevailing:
                    continue  # temperature value does not currently fit on the chart
                if to < adaptive_chart._min_operative or \
                        to > adaptive_chart._max_operative:
                    continue  # temperature value does not currently fit on the chart
                for y, to_cat in enumerate(adaptive_chart._to_category):
                    if to < to_cat:
                        break
                for x, tp_cat in enumerate(adaptive_chart._tp_category):
                    if tp < tp_cat:
                        break
                base_mtx[y][x].append(val)
            # compute average values
            avg_values = [sum(val_list) / len(val_list) for rh_l in base_mtx
                          for val_list in rh_l if len(val_list) != 0]
            hd = dat.header
            vd = VisualizationData(avg_values, lp, hd.data_type, hd.unit)
            vis_data.append(vd)
    # create the analysis geometry
    mesh_3d = Mesh3D.from_mesh2d(adaptive_chart.colored_mesh, bp)
    mesh_geo = AnalysisGeometry(
        'Analysis_Data', [mesh_3d], vis_data, active_data=len(vis_data) - 1)
    mesh_geo.display_name = 'Analysis Data'
    mesh_geo.display_mode = 'Surface'
    vis_set.add_geometry(mesh_geo)

    return vis_set


def _plane_from_point(point_2d, z, align_vec=Vector3D(1, 0, 0)):
    """Get a Plane from a Point2D.

    Args:
        point_2d: A Point2D to serve as the origin of the plane.
        z: The Z value for the plane origin.
        align_vec: A Vector3D to serve as the X-Axis of the plane.
    """
    return Plane(o=Point3D(point_2d.x, point_2d.y, z), x=align_vec)
