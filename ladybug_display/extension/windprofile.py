"""Method to draw a WindProfile as a VisualizationSet."""
from ladybug_geometry.geometry3d import Point3D

from ladybug.datatype.speed import WindSpeed
from ladybug.legend import LegendParameters

from ladybug_display.geometry3d import DisplayLineSegment3D, DisplayPolyline3D, \
    DisplayMesh3D, DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry


def wind_profile_to_vis_set(
        profile, meteorological_wind_speed=5, direction=None,
        legend_parameters=None, base_point=Point3D(0, 0, 0),
        max_height=30, vector_spacing=2,
        vector_length_dimension=5, vector_height_dimension=1,
        max_speed=None, scale_factor=1, feet_labels=False):
    """Get a Ladybug WindProfile represented as a VisualizationSet.

    Args:
        profile: A Ladybug WindProfile object.
        meteorological_wind_speed: A number for the meteorological wind speed [m/s].
            This is usually for a point in time or it is the average wind speed
            over a range of times. (Default: 5).
        direction: An optional number between 0 and 360 that represents the
            cardinal direction that the wind profile is facing in the XY
            plane. 0 = North, 90 = East, 180 = South, 270 = West. Note that this
            should already account for any difference between true North and
            project North, which simply involves subtracting the counterclockwise
            north angle from the wind direction. If None, the wind profile will
            simply be placed in the XY plane. (Default: None).
        legend_parameters: Optional LegendParameters to change the display of the
            wind profile arrows.
        base_point: A ladybug-geometry Point3D that represents the ground
            location of the wind profile. (Default, (0, 0, 0)).
        max_height: A number in meters to specify the maximum height of the
            wind profile curve. (Default: 30 meters).
        vector_spacing: A number in meters to specify the difference in height
            between each of the mesh arrows. (Default 2 meters).
        vector_length_dimension: A number to denote the length dimension of a 1 m/s
            wind vector in meters. (Default: 5).
        vector_height_dimension: A number to denote the height dimension of the
            wind vector in meters. (Default: 1).
        max_speed: A number for the maximum wind speed along the speed axis
            in [m/s]. If None, it will be set automatically by the wind profile
            maximum value. (Default: None).
        scale_factor: An optional number that will be multiplied by all dimensions
            to account for the fact that the wind profile may be displaying in
            a units system other than meters. (Default: 1).
        feet_labels: A boolean to note whether the text labels on the height axis
            should be in feet (True) or meters (False). (Default: False).

    Returns:
        A VisualizationSet with the wind profile represented several ContextGeometries
        and an AnalysisGeometry. This includes these objects in the following order.

        -   Arrows -- An AnalysisGeometry of colored mesh objects that represent
                the wind speeds along the height of the wind profile.

        -   Profile -- A Polyline outlining the wind speed as it changes
                with height.

        -   Speed_Axis -- A ContextGeometry of line segments and text objects
                that mark the X axis, which relates to the wind speed in (m/s).

        -   Height_Axis -- A ContextGeometry of line segments and text objects
                that mark the Y axis, which relates to the the height above the ground.
    """
    # establish the VisualizationSet object
    vis_set = VisualizationSet(
        'WindProfile_{}'.format(int(meteorological_wind_speed)), ())
    vis_set.display_name = 'Wind Profile'

    # shorten the names of the inputs to make them easier to work with
    met_ws = meteorological_wind_speed
    bp, len_d, height_d = base_point, vector_length_dimension, vector_height_dimension

    # generate the arrow geometries of the visualization
    _, mesh_arrows, wind_speeds, wind_vectors, anchor_pts = \
        profile.mesh_arrow_profile(
            met_ws, max_height, vector_spacing, direction, bp,
            len_d, height_d, scale_factor)

    # customize the legend parameters to ensure the default legend looks good
    legend_par = legend_parameters.duplicate() if legend_parameters is not None \
        else LegendParameters()
    max_speed = round(wind_speeds[-1]) if max_speed is None else max_speed
    max_pt = Point3D(bp.x + ((max_speed + 2) * len_d * scale_factor),
                     bp.y + (30 * scale_factor), bp.z)
    # set the default segment_height
    if legend_par.is_segment_height_default:
        s_count = legend_par.segment_count
        denom = s_count if s_count >= 8 else 8
        if legend_par.vertical:
            seg_height = float((max_pt.y - bp.y) / denom)
            if seg_height == 0:
                seg_height = float((max_pt.x - bp.x) / denom)
        else:
            seg_height = float((max_pt.x - bp.x) / (denom * 2))
            if seg_height == 0:
                seg_height = float((max_pt.y - bp.y) / denom)
        legend_par.properties_3d.segment_height = seg_height
    # set the default segment_width
    if legend_par.is_segment_width_default:
        if legend_par.vertical:
            seg_width = legend_par.segment_height / 2
        else:
            seg_width = legend_par.text_height * \
                (len(str(int(legend_par.max))) + legend_par.decimal_count + 2)
        legend_par.properties_3d.segment_width = seg_width
    # set the default base_plane
    if legend_par.is_base_plane_default:
        legend_par.base_plane = \
            profile.legend_plane(max_speed, direction, bp, len_d, scale_factor)

    # create an AnalysisGeometry for the colored arrows
    vis_data = VisualizationData(wind_speeds, legend_par, WindSpeed(), 'm/s')
    a_geo = AnalysisGeometry('Arrows', mesh_arrows, [vis_data])
    vis_set.add_geometry(a_geo)

    # create a ContextGeometry for the profile line
    pl, _, _ = profile.profile_polyline3d(
        met_ws, max_height, 0.1, direction, bp, len_d, scale_factor)
    dis_profile_line = DisplayPolyline3D(pl, line_width=1)
    profile_geo = ContextGeometry('Profile', [dis_profile_line])
    vis_set.add_geometry(profile_geo)

    # create a ContextGeometry for the speed axis
    txt_h = legend_par.text_height
    axis_line, axis_arrow, axis_ticks, text_planes, text = \
        profile.speed_axis(max_speed, direction, bp, len_d, scale_factor, txt_h)
    speed_axis = [DisplayLineSegment3D(axis_line), DisplayMesh3D(axis_arrow)]
    for tic in axis_ticks:
        speed_axis.append(DisplayLineSegment3D(tic))
    for i, (pl, txt) in enumerate(zip(text_planes, text)):
        txt_i_h = txt_h if i != len(text) - 1 else txt_h * 1.25
        txt_obj = DisplayText3D(txt, pl, txt_i_h, None, legend_par.font, 'Center', 'Top')
        speed_axis.append(txt_obj)
    speed_axis_geo = ContextGeometry('Speed_Axis', speed_axis)
    speed_axis_geo.display_name = 'Speed Axis'
    vis_set.add_geometry(speed_axis_geo)

    # create a ContextGeometry for the height axis
    axis_line, axis_arrow, axis_ticks, text_planes, text = \
        profile.height_axis(max_height, vector_spacing * 2, direction, bp,
                            scale_factor, txt_h, feet_labels)
    height_axis = [DisplayLineSegment3D(axis_line), DisplayMesh3D(axis_arrow)]
    for tic in axis_ticks:
        height_axis.append(DisplayLineSegment3D(tic))
    for i, (pl, txt) in enumerate(zip(text_planes, text)):
        if i != len(text) - 1:
            txt_i_h, ha, va = txt_h, 'Right', 'Middle'
        else:
            txt_i_h, ha, va = txt_h * 1.25, 'Center', 'Bottom'
        txt_obj = DisplayText3D(txt, pl, txt_i_h, None, legend_par.font, ha, va)
        height_axis.append(txt_obj)
    height_axis_geo = ContextGeometry('Height_Axis', height_axis)
    height_axis_geo.display_name = 'Height Axis'
    vis_set.add_geometry(height_axis_geo)

    return vis_set
