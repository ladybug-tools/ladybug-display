from ladybug_geometry.geometry2d import Polyline2D
from ladybug_geometry.geometry3d import Point3D, Plane, LineSegment3D, \
    Polyline3D, Mesh3D

from ladybug_display.geometry3d import DisplayLineSegment3D, DisplayPolyline3D
from ladybug_display.visualization import VisualizationSet, AnalysisGeometry, \
    VisualizationData, ContextGeometry
from ladybug_display.extension.compass import compass_to_vis_set


def wind_rose_to_vis_set(windrose, z=0):
    """Get a Ladybug WindRose represented as a VisualizationSet.

    Args:
        windrose: A Ladybug WindRose object.
        z: A number for the Z-coordinate to be used in translation. (Default: 0)

    Returns:
        A VisualizationSet with the wind rose represented several ContextGeometries
        (and optionally an AnalysisGeometry if data is input). This includes these
        objects in the following order.

        -   Compass -- A ContextGeometry for the Compass at the base of the wind rose.

        -   Orientation_Lines -- Line geometries representing the edges (or "spokes")
                of the wind rose directions.

        -   Frequency_Lines -- Polygon geometries representing the frequency intervals
                of the wind rose.

        -   Analysis_Data -- An AnalysisGeometry for representing the wind rose
                derived from the input data.
    """
    # establish the VisualizationSet object
    wr_metadata = windrose.analysis_data_collection.header.metadata
    set_id = 'Wind_Rose_{}'.format(wr_metadata['city'].replace(' ', '_')) \
        if wr_metadata is not None \
        and 'city' in wr_metadata else 'Wind_Rose'
    vis_set = VisualizationSet(set_id, ())

    # add the compass to the bottom of the path
    vis_set.add_geometry(compass_to_vis_set(windrose.compass, z=z)[0])

    # add the orientation lines
    orient_line = [LineSegment3D.from_line_segment2d(seg, z) for seg in
                   windrose.orientation_lines]
    dis_orient = []
    for i, lin in enumerate(orient_line):
        dis_orient.append(DisplayLineSegment3D(lin, line_type='Dotted'))
    orient_geo = ContextGeometry('Orientation_Lines', dis_orient)
    orient_geo.display_name = 'Orientation Lines'
    vis_set.add_geometry(orient_geo)

    # add the frequency lines
    wr_pln = Plane(o=Point3D(windrose.base_point.x, windrose.base_point.y, z))
    freq_line = [Polyline3D.from_polyline2d(Polyline2D.from_polygon(poly), wr_pln)
                 for poly in windrose.frequency_lines[:-1]]
    dis_freq = []
    for i, lin in enumerate(freq_line):
        dis_freq.append(DisplayPolyline3D(lin, line_type='Dotted'))
    freq_geo = ContextGeometry('Frequency_Lines', dis_freq)
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
