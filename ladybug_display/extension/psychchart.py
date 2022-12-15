"""Method to draw an PsychrometricChart as a VisualizationSet."""
from ladybug_geometry.geometry3d import Vector3D, Point3D, Plane, LineSegment3D, \
    Polyline3D, Mesh3D
from ladybug.datatype.time import Time
from ladybug.datacollection import BaseCollection
from ladybug.legend import LegendParameters

from ladybug_display.geometry3d import DisplayLineSegment3D, DisplayPolyline3D, \
    DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def psychrometric_chart_to_vis_set(
        psych_chart, data=None, legend_parameters=None, z=0, plot_wet_bulb=False):
    """Get a Ladybug PsychrometricChart represented as a VisualizationSet.

    Args:
        psych_chart: A Ladybug PsychrometricChart object.
        data: An optional list of data collection objects, which are aligned with
            the psychrometric chart temperature and relative_humidity and will
            generate additional colored AnalysisGeometries on the chart.
        legend_parameters: An optional LegendParameter object or list of LegendParameter
            objects to customize the display of the data on the psychrometric
            chart. Note that this relates only to the data supplied as input
            for this method and, to customize the display of the time/frequency
            mesh, the PsychrometricChart's native legend_parameters should be
            edited. If a list is used here, this should align with the input data
            (one legend parameter per data collection).
        z: A number for the Z-coordinate to be used in translation. (Default: 0).
        plot_wet_bulb: Boolean to note whether the psychrometric chart should be
            plotted with lines of constant enthalpy (False) or lines of constant
            wet bulb temperature (True). (Default: False).

    Returns:
        A VisualizationSet with the psychrometric chart represented several
        ContextGeometries and an AnalysisGeometry. This includes these objects
        in the following order.

        -   Title -- A ContextGeometry for the title and border around the
                psychrometric chart.

        -   Temperature_Axis -- A ContextGeometry with lines and text for the
                Temperature (X) axis of the psychrometric chart.

        -   Humidity_Axis -- A ContextGeometry with lines and text for the
                Humidity (Y) axis of the psychrometric chart.

        -   Relative_Humidity_Lines -- A ContextGeometry with lines and text
                for the relative humidity of the psychrometric chart.

        -   Enthalpy_Lines -- A ContextGeometry with lines and text for the
                enthalpy of the psychrometric chart. This layer will not be
                included if plot_wet_bulb is True.

        -   Wet_Bulb_Lines -- A ContextGeometry with lines and text for the wet bulb
                temperature of the psychrometric chart. This layer will not be
                included if plot_wet_bulb is FAlse.

        -   Analysis_Data -- An AnalysisGeometry for the data on the psychrometric
                chart. This will include multiple data sets if the data input
                is provided.
    """
    # establish the VisualizationSet object
    vis_set = VisualizationSet('Psychrometric_Chart', ())
    vis_set.display_name = 'Psychrometric Chart'

    # get values used throughout the translation
    txt_hgt = psych_chart.legend_parameters.text_height
    font = psych_chart.legend_parameters.font
    bp = Plane(o=Point3D(0, 0, z))

    # add the title and border
    if isinstance(psych_chart.temperature, BaseCollection):
        meta_i = psych_chart.temperature.header.metadata.items()
        title_items = ['Time [hr]'] + ['{}: {}'.format(k, v) for k, v in meta_i]
    else:
        title_items = ['Psychrometric Chart']
    ttl_pl = psych_chart.container.upper_title_location
    if z != 0:
        ttl_pl = Plane(n=ttl_pl.n, o=Point3D(ttl_pl.o.x, ttl_pl.o.y, z), x=ttl_pl.x)
    ttl_txt = DisplayText3D(
        '\n'.join(title_items), ttl_pl, txt_hgt * 1.5, None, font, 'Left', 'Top')
    border_geo = Polyline3D.from_polyline2d(psych_chart.chart_border, bp)
    sat_geo = Polyline3D.from_polyline2d(psych_chart.saturation_line, bp)
    title_objs = [ttl_txt, DisplayPolyline3D(sat_geo, line_width=2),
                  DisplayPolyline3D(border_geo, line_width=2)]
    title = ContextGeometry('Title', title_objs)
    vis_set.add_geometry(title)

    # add the temperature axis
    tm_pl = _plane_from_point(psych_chart.x_axis_location, z)
    temp_txt = DisplayText3D(
        psych_chart.x_axis_text, tm_pl, txt_hgt * 1.5, None, font, 'Left', 'Top')
    temp_geo = [temp_txt]
    for tl in psych_chart.temperature_lines:
        tl_geo = LineSegment3D.from_line_segment2d(tl, z)
        temp_geo.append(DisplayLineSegment3D(tl_geo))
    tl_pts = psych_chart.temperature_label_points
    for txt, pt in zip(psych_chart.temperature_labels, tl_pts):
        t_pln = Plane(o=Point3D(pt.x, pt.y, z))
        txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Center', 'Top')
        temp_geo.append(txt_obj)
    temp_axis = ContextGeometry('Temperature_Axis', temp_geo)
    temp_axis.display_name = 'Temperature Axis'
    vis_set.add_geometry(temp_axis)

    # add the humidity axis
    hr_pl = _plane_from_point(psych_chart.y_axis_location, z, Vector3D(0, 1))
    hr_txt = DisplayText3D(
        psych_chart.y_axis_text, hr_pl, txt_hgt * 1.5, None, font, 'Right', 'Top')
    hr_geo = [hr_txt]
    for hl in psych_chart.hr_lines:
        hl_geo = LineSegment3D.from_line_segment2d(hl, z)
        hr_geo.append(DisplayLineSegment3D(hl_geo))
    for txt, pt in zip(psych_chart.hr_labels, psych_chart.hr_label_points):
        t_pln = Plane(o=Point3D(pt.x, pt.y, z))
        txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Left', 'Middle')
        hr_geo.append(txt_obj)
    hr_axis = ContextGeometry('Humidity_Axis', hr_geo)
    hr_axis.display_name = 'Humidity Axis'
    vis_set.add_geometry(hr_axis)

    # add the relative humidity lines
    rh_geo = []
    for rl in psych_chart.rh_lines:
        rl_geo = Polyline3D.from_polyline2d(rl, bp)
        rh_geo.append(DisplayPolyline3D(rl_geo))
    for txt, pt in zip(psych_chart.rh_labels[:-1], psych_chart.rh_label_points[:-1]):
        t_pln = Plane(o=Point3D(pt.x, pt.y, z))
        txt_obj = DisplayText3D(txt, t_pln, txt_hgt * 0.8, None, font, 'Right', 'Middle')
        rh_geo.append(txt_obj)
    rh_axis = ContextGeometry('Relative_Humidity_Lines', rh_geo)
    rh_axis.display_name = 'Relative Humidity Lines'
    vis_set.add_geometry(rh_axis)

    # add enthalpy or wet bulb lines
    if plot_wet_bulb:
        wb_geo = []
        for wl in psych_chart.wb_lines:
            wl_geo = LineSegment3D.from_line_segment2d(wl, z)
            wb_geo.append(DisplayLineSegment3D(wl_geo, line_type='Dotted'))
        for txt, pt in zip(psych_chart.wb_labels, psych_chart.wb_label_points):
            t_pln = Plane(o=Point3D(pt.x, pt.y, z))
            txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Right', 'Middle')
            wb_geo.append(txt_obj)
        wb_axis = ContextGeometry('Wet_Bulb_Lines', wb_geo)
        wb_axis.display_name = 'Wet Bulb Lines'
        vis_set.add_geometry(wb_axis)
    else:
        enth_geo = []
        for wl in psych_chart.enthalpy_lines:
            wl_geo = LineSegment3D.from_line_segment2d(wl, z)
            enth_geo.append(DisplayLineSegment3D(wl_geo, line_type='Dotted'))
        enth_pts = psych_chart.enthalpy_label_points
        for txt, pt in zip(psych_chart.enthalpy_labels, enth_pts):
            t_pln = Plane(o=Point3D(pt.x, pt.y, z))
            txt_obj = DisplayText3D(txt, t_pln, txt_hgt, None, font, 'Right', 'Middle')
            enth_geo.append(txt_obj)
        enth_axis = ContextGeometry('Enthalpy_Lines', enth_geo)
        enth_axis.display_name = 'Enthalpy Lines'
        vis_set.add_geometry(enth_axis)

    # add the analysis geometry
    # ensure 3D legend defaults are overridden to make the data readable
    l_par = psych_chart.legend.legend_parameters.duplicate()
    l_par.base_plane = l_par.base_plane
    l_par.segment_height = l_par.segment_height
    l_par.segment_width = l_par.segment_width
    # gather all of the visualization data sets
    vis_data = [VisualizationData(psych_chart.hour_values, l_par, Time(), 'hr')]
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
            assert len(d_vals) == psych_chart._calc_length, \
                'Number of data collection values ' \
                'must match those of the psychometric chart temperature and humidity.'
            # create a matrix with a tally of the hours for all the data
            base_mtx = [[[] for val in psych_chart._t_category]
                        for rh in psych_chart._rh_category]
            for t, rh, v in zip(psych_chart._t_values, psych_chart._rh_values, d_vals):
                if t < psych_chart._min_temperature or t > psych_chart._max_temperature:
                    continue  # temperature value does not currently fit on the chart
                for y, rh_cat in enumerate(psych_chart._rh_category):
                    if rh < rh_cat:
                        break
                for x, t_cat in enumerate(psych_chart._t_category):
                    if t < t_cat:
                        break
                base_mtx[y][x].append(v)
            # compute average values
            avg_values = [sum(val_list) / len(val_list) for rh_l in base_mtx
                          for val_list in rh_l if len(val_list) != 0]
            hd = dat.header
            vd = VisualizationData(avg_values, lp, hd.data_type, hd.unit)
            vis_data.append(vd)
    # create the analysis geometry
    mesh_3d = Mesh3D.from_mesh2d(psych_chart.colored_mesh, bp)
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
