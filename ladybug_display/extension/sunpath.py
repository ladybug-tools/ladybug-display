"""Method to draw a Sunpath as a VisualizationSet."""
from ladybug_geometry.geometry2d.pointvector import Point2D
from ladybug_geometry.geometry3d import Point3D, Plane, Polyline3D, Sphere
from ladybug.dt import Date
from ladybug.color import Color
from ladybug.legend import LegendParameters
from ladybug.compass import Compass

from ..geometry3d import DisplayPoint3D, DisplayArc3D, DisplayPolyline3D, DisplaySphere
from ..visualization import VisualizationSet, \
    ContextGeometry, AnalysisGeometry, VisualizationData
from .compass import compass_to_vis_set


def sunpath_to_vis_set(
        sunpath, hoys=None, data=None, legend_parameters=None,
        radius=100, center_point=Point3D(0, 0, 0),
        solar_time=False, daily=False, projection=None, sun_spheres=False):
    """Get a Ladybug Sunpath represented as a VisualizationSet.

    Args:
        sunpath: A Ladybug Sunpath object.
        hoys: An optional list of numbers between 0 and 8760 that represent the
            hours of the year at which the sun position will be displayed.
            The Ladybug AnalysisPeriod class can output a list of HOYs within
            a certain hour or date range. (Default: None).
        data: An optional list of hourly data collection objects, which will
            generate colored sun positions for each of the hoys.
        legend_parameters: An optional LegendParameter object or list of LegendParameter
            objects to customize the display of the data on the sun path. If a
            list is used, these should align with the input data (one legend
            parameter per data collection).
        radius: Number for the radius of the sun path. (Default: 100).
        center_point: Point3D for the center of the sun path. (Default: (0, 0, 0)).
        solar_time: A boolean to indicate if the sunpath should be drawn with solar
             time hours instead of standard or daylight time. (Default: False)
        daily: Boolean to note whether the sunpath should display only one daily
            arc for each unique day in the input hoys_ (True) or whether the
            output sun path geometry should be for the entire year, complete
            with analemmas for all sun-up hours and a daily arc for each
            month (False). (Default: False)
        projection: Optional text for the name of a projection to use from the sky
            dome hemisphere to the 2D plane. If None, a 3D sun path will be drawn
            instead of a 2D one. (Default: None) Choose from the following:
                * Orthographic
                * Stereographic
        sun_spheres: Boolean to note whether sun positions should be drawn as points
            or as fully-detailed spheres. Note that this option should only be
            used when there are relatively few hoys input. Anything more than
            100 hoys can make the display very slow. (Default: False).

    Returns:
        A VisualizationSet with the Sunpath represented several ContextGeometries
        (and optionally an AnalysisGeometry if data is input). This includes these
        objects in the following order.

        -   Compass -- A ContextGeometry for the Compass at the base of the sunpath.

        -   Analemmas -- A ContextGeometry for the analemmas of the sunpath (if
                the daily input is False).

        -   Daily_Arcs -- A ContextGeometry for the daily arcs across the sunpath.

        -   Sun_Positions -- Either a ContextGeometry or an AnalysisGeometry for
                the sun positions (if hoys are input). The object will be an
                AnalysisGeometry if data is input, indicating that suns are colored
                with this data.
    """
    # establish the VisualizationSet object
    vis_set = VisualizationSet(
        'Sunpath_{}_{}'.format(int(sunpath.latitude), int(sunpath.longitude)), ())
    vis_set.display_name = 'Sunpath'

    # add the compass to the bottom of the path
    center_2d = Point2D(center_point.x, center_point.y)
    compass = Compass(radius, center_2d, sunpath.north_angle)
    compass_vis = compass_to_vis_set(compass, z=center_point.z, projection=projection)
    vis_set.add_geometry(compass_vis[0])

    # create a intersection of the input hoys and the data hoys (if provided)
    if data is not None and len(data) > 0 and hoys is not None and len(hoys) > 0:
        all_aligned = all(data[0].is_collection_aligned(d) for d in data[1:])
        assert all_aligned, 'All collections input to data must be aligned for ' \
            'each Sunpath.\nGrafting the data and supplying multiple grafted ' \
            '_center_pt_ can be used to view each data on its own path.'
        data_hoys = set(dt.hoy for dt in data[0].datetimes)
        hoys = list(data_hoys.intersection(set(hoys)))

    # get the relevant sus and datetimes
    suns, datetimes, moys = [], [], []
    if hoys is not None and len(hoys) > 0:
        for hoy in hoys:
            sun = sunpath.calculate_sun_from_hoy(hoy, solar_time)
            if sun.is_during_day:
                suns.append(sun)
                datetimes.append(sun.datetime)
                moys.append(sun.datetime.moy)

    # add the daily arcs and analemmas to the visualization set
    original_dls = sunpath.daylight_saving_period
    sunpath.daylight_saving_period = None  # set here so analemmas aren't messed up
    center_pt, z = Point2D(center_point.x, center_point.y), center_point.z
    if not daily:
        if projection is None:
            # draw arcs and analemmas in 3D
            ana_plin_1 = sunpath.hourly_analemma_polyline3d(
                center_point, radius, True, solar_time, 1, 6, 4)
            ana_plin_2 = sunpath.hourly_analemma_polyline3d(
                center_point, radius, True, solar_time, 7, 12, 4)
            analemma = [DisplayPolyline3D(pl, line_width=1) for pl in ana_plin_1] + \
                [DisplayPolyline3D(pl, line_width=1, line_type='Dashed')
                 for pl in ana_plin_2]
            daily_arc = sunpath.monthly_day_arc3d(center_point, radius)
            daily = []
            for i, arc in enumerate(daily_arc):
                lw = 2 if (i + 1) % 6 == 0 else 1
                lt = 'Continuous' if i <= 5 else 'Dashed'
                daily.append(DisplayArc3D(arc, line_width=lw, line_type=lt))
        else:
            # draw arcs and analemmas in the requested projection
            bp = Plane(o=Point3D(0, 0, z))
            ana_plin_1 = sunpath.hourly_analemma_polyline2d(
                projection, center_point, radius, True, solar_time, 1, 6, 4)
            ana_plin_2 = sunpath.hourly_analemma_polyline2d(
                projection, center_point, radius, True, solar_time, 7, 12, 4)
            analemma = \
                [DisplayPolyline3D(Polyline3D.from_polyline2d(p, bp), line_width=1)
                 for p in ana_plin_1] + \
                [DisplayPolyline3D(
                    Polyline3D.from_polyline2d(p, bp), line_width=1, line_type='Dashed')
                 for p in ana_plin_2]
            daily_arc = sunpath.monthly_day_polyline2d(
                projection, center_point, radius, divisions=30)
            daily = []
            for i, arc in enumerate(daily_arc):
                lw = 2 if (i + 1) % 6 == 0 else 1
                lt = 'Continuous' if i <= 5 else 'Dashed'
                pline = Polyline3D.from_polyline2d(arc, bp)
                daily.append(DisplayPolyline3D(pline, line_width=lw, line_type=lt))
        analemma_geo = ContextGeometry('Analemmas', analemma)
        vis_set.add_geometry(analemma_geo)
    else:
        # just draw daily arcs without the analemmas
        doys = set(dt.doy for dt in datetimes)
        dates = [Date.from_doy(doy) for doy in doys]
        if projection is None:
            daily = []
            for dat in dates:
                d_arc = sunpath.day_arc3d(dat.month, dat.day, center_point, radius)
                daily.append(DisplayArc3D(d_arc, line_width=1))
        else:
            bp = Plane(o=Point3D(0, 0, z))
            daily = []
            for dat in dates:
                d_arc = sunpath.day_polyline2d(
                    dat.month, dat.day, projection, center_pt, radius, divisions=30)
                daily.append(DisplayPolyline3D(
                    Polyline3D.from_polyline2d(d_arc, bp), line_width=1))
    if len(daily) != 0:
        daily_geo = ContextGeometry('Daily_Arcs', daily)
        daily_geo.display_name = 'Daily Arcs'
        vis_set.add_geometry(daily_geo)
    sunpath.daylight_saving_period = original_dls  # put back to avoid mutation

    # plot the sun positions as points on the sunpath
    if hoys is not None and len(hoys) > 0:
        # get Point3Ds for all of the sun positions
        if projection is None:
            sun_pts = [sun.position_3d(center_point, radius) for sun in suns]
        else:
            sun_pts = []
            for sun in suns:
                pt2d = sun.position_2d(projection, center_point, radius)
                sun_pts.append(Point3D.from_point2d(pt2d, z))
        if sun_spheres:
            sun_pts = [Sphere(pt, radius / 30) for pt in sun_pts]
        # plot the sun positions as either context or analysis geometry
        if data is not None and len(data) > 0:
            # plot points as context or analysis geometry (if data is connected)
            if isinstance(legend_parameters, LegendParameters):
                legend_parameters = [legend_parameters] * len(data)
            all_data = []
            for i, dat_c in enumerate(data):
                l_par = legend_parameters[i] if legend_parameters is not None else None
                n_data = dat_c.filter_by_moys(moys)  # filter data by sun-up hours
                v_data = VisualizationData(
                    n_data.values, l_par, dat_c.header.data_type, dat_c.header.unit)
                all_data.append(v_data)
            sun_geo = AnalysisGeometry('Sun_Positions', sun_pts, all_data)
        else:  # otherwise, plot the suns as context geometry
            orange = Color(255, 165, 0)
            if sun_spheres:
                dis_pts = [DisplaySphere(pt, color=orange) for pt in sun_pts]
            else:
                dis_pts = [DisplayPoint3D(pt, color=orange, radius=5) for pt in sun_pts]
            sun_geo = ContextGeometry('Sun_Positions', dis_pts)
        sun_geo.display_name = 'Sun Positions'
        vis_set.add_geometry(sun_geo)

    return vis_set
