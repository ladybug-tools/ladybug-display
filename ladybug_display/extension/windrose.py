"""Method to draw a WindRose as a VisualizationSet."""
from ladybug_geometry.geometry2d import Polyline2D
from ladybug_geometry.geometry3d import Point3D, Plane, LineSegment3D, \
    Polyline3D, Mesh3D

from ladybug_display.geometry3d import DisplayLineSegment3D, DisplayPolyline3D, \
    DisplayText3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry
from ladybug_display.extension.compass import compass_to_vis_set


def wind_rose_to_vis_set(windrose, z=0, frequency_labels=True):
    """Get a Ladybug WindRose represented as a VisualizationSet.

    Args:
        windrose: A Ladybug WindRose object.
        z: A number for the Z-coordinate to be used in translation. (Default: 0).
        frequency_labels: A boolean to note whether frequency labels should be
            included in the output visualization. (Default: True).

    Returns:
        A VisualizationSet with the wind rose represented several ContextGeometries
        and an AnalysisGeometry. This includes these objects in the following order.

        -   Compass -- A ContextGeometry for the Compass at the base of the wind rose.

        -   Orientation_Lines -- A ContextGeometry with lines representing the
                edges (or "spokes") of the wind rose directions.

        -   Frequency_Lines -- A ContextGeometry with polygons representing
                the frequency intervals of the wind rose.

        -   Analysis_Data -- An AnalysisGeometry for the wind rose data.
    """
    # establish the VisualizationSet object
    wr_metadata = windrose.analysis_data_collection.header.metadata
    set_id = 'Wind_Rose_{}'.format(wr_metadata['city'].replace(' ', '_')) \
        if wr_metadata is not None \
        and 'city' in wr_metadata else 'Wind_Rose'
    vis_set = VisualizationSet(set_id, ())

    # add the compass to the bottom of the path
    legend_par = windrose.legend.legend_parameters
    font, txt_h = legend_par.font, legend_par.text_height
    vis_set.add_geometry(compass_to_vis_set(windrose.compass, z=z, font=font)[0])

    # add the orientation lines
    orient_line = [LineSegment3D.from_line_segment2d(seg, z) for seg in
                   windrose.orientation_lines]
    dis_orient = []
    for lin in orient_line:
        dis_orient.append(DisplayLineSegment3D(lin, line_width=1, line_type='Dotted'))
    orient_geo = ContextGeometry('Orientation_Lines', dis_orient)
    orient_geo.display_name = 'Orientation Lines'
    vis_set.add_geometry(orient_geo)

    # add the frequency lines
    wr_pln = Plane(o=Point3D(0, 0, z))
    freq_line = [Polyline3D.from_polyline2d(Polyline2D.from_polygon(poly), wr_pln)
                 for poly in windrose.frequency_lines[:-1]]
    dis_freq, freq_text = [], []
    for lin in freq_line:
        dis_freq.append(DisplayPolyline3D(lin, line_width=1, line_type='Dotted'))
    if frequency_labels:
        f_int = windrose.frequency_hours
        txt_h = min((windrose.frequency_spacing_distance / 4, txt_h))
        freqs = range(0, f_int * windrose.frequency_intervals_compass, f_int)
        for i, (lin, val) in enumerate(zip(freq_line, freqs)):
            if i % 2 == 0 and i != 0:
                b_pln = Plane(o=lin.segments[0].midpoint)
                d_txt = DisplayText3D(str(val), b_pln, txt_h, None, font,
                                      'Center', 'Bottom')
                freq_text.append(d_txt)
    freq_geo = ContextGeometry('Frequency_Lines', dis_freq + freq_text)
    freq_geo.display_name = 'Frequency Lines'
    vis_set.add_geometry(freq_geo)

    # add the colored mesh
    msh = Mesh3D.from_mesh2d(windrose.colored_mesh, wr_pln)
    data_header = windrose.analysis_data_collection.header
    data_type, unit = data_header.data_type, data_header.unit
    vis_data = VisualizationData(
        windrose._color_array, windrose.legend_parameters, data_type, unit)
    mesh_geo = AnalysisGeometry('Analysis_Data', [msh], [vis_data])
    mesh_geo.display_name = data_type.name
    mesh_geo.display_mode = 'SurfaceWithEdges'
    vis_set.add_geometry(mesh_geo)

    return vis_set
