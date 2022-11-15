"""Method to draw a Compass as a VisualizationSet."""
import math

from ladybug_geometry.geometry3d import Vector3D, Point3D, Plane, LineSegment3D, Arc3D

from ..geometry3d import DisplayText3D, DisplayArc3D, DisplayLineSegment3D
from ..visualization import VisualizationSet, ContextGeometry


def compass_to_vis_set(compass, z=0, custom_angles=None, projection=None, font='Arial'):
    """Translate a Ladybug Compass object into Display geometry.

    Args:
        compass: A Ladybug Compass object to be converted to display geometry.
        z: A number for the Z-coordinate to be used in translation. (Default: 0)
        custom_angles: An array of numbers between 0 and 360 to be used to
            generate custom angle labels around the compass.
        projection: Text for the name of the projection to use from the sky
            dome hemisphere to the 2D plane. If None, no altitude circles o
            labels will be drawn (Default: None). Choose from the following:

            * Orthographic
            * Stereographic

        font: Optional text for the font to be used in creating the text.
            (Default: 'Arial')

    Returns:
        A VisualizationSet with the Compass represented as a single ContextGeometry.
        This context geometry includes these objects in the following order.

        -   all_boundary_circles -- Three Circle objects for the compass boundary.

        -   major_azimuth_ticks -- Line objects for the major azimuth labels.

        -   major_azimuth_text -- Text objects for the major azimuth labels.

        -   minor_azimuth_ticks -- Line objects for the minor azimuth labels
                (if applicable).

        -   minor_azimuth_text -- Text objects for the minor azimuth
                labels (if applicable).

        -   altitude_circles -- Circle objects for altitude labels (if projection
                is not None).

        -   altitude_text -- Text objects for altitude labels (if projection
                is not None).

     """
    # set default variables based on the compass properties
    maj_txt = compass.radius / 20
    min_txt = maj_txt / 2
    xaxis = Vector3D(1, 0, 0).rotate_xy(math.radians(compass.north_angle))

    result = []  # list to hold all of the returned objects
    for i, circle in enumerate(compass.all_boundary_circles):
        lw = 2 if i == 0 else 1
        result.append(DisplayArc3D(Arc3D.from_arc2d(circle, z), line_width=lw))

    # create a method that translates LineSegment2D into DisplayLineSegment3D
    def from_linesegment2d(line, z, line_width=1):
        pt_array = ((line.p1.x, line.p1.y, z), (line.p2.x, line.p2.y, z))
        ls_3d = LineSegment3D.from_array(pt_array)
        return DisplayLineSegment3D(ls_3d, line_width=line_width)

    # generate the labels and tick marks for the azimuths
    if custom_angles is None:
        for line in compass.major_azimuth_ticks:
            result.append(from_linesegment2d(line, z, 2))
        for txt, pt in zip(compass.MAJOR_TEXT, compass.major_azimuth_points):
            txt_pln = Plane(o=Point3D(pt.x, pt.y, z), x=xaxis)
            result.append(
                DisplayText3D(txt, txt_pln, maj_txt, None, font, 'Center', 'Middle'))
        for line in compass.minor_azimuth_ticks:
            result.append(from_linesegment2d(line, z))
        for txt, pt in zip(compass.MINOR_TEXT, compass.minor_azimuth_points):
            txt_pln = Plane(o=Point3D(pt.x, pt.y, z), x=xaxis)
            result.append(
                DisplayText3D(txt, txt_pln, min_txt, None, font, 'Center', 'Middle'))
    else:
        for line in compass.ticks_from_angles(custom_angles):
            result.append(from_linesegment2d(line, z))
        for txt, pt in zip(
                custom_angles, compass.label_points_from_angles(custom_angles)):
            t_pln = Plane(o=Point3D(pt.x, pt.y, z), x=xaxis)
            d_t = DisplayText3D(str(txt), t_pln, maj_txt, None, font, 'Center', 'Middle')
            result.append(d_t)

    # generate the labels and tick marks for the altitudes
    if projection is not None:
        if projection.title() == 'Orthographic':
            for circle in compass.orthographic_altitude_circles:
                arc_geo = Arc3D.from_arc2d(circle, z)
                result.append(DisplayArc3D(arc_geo, line_width=1, line_type='Dotted'))
            for txt, pt in zip(compass.ALTITUDES, compass.orthographic_altitude_points):
                txt_pln = Plane(o=Point3D(pt.x, pt.y, z), x=xaxis)
                d_txt = DisplayText3D(
                    str(txt), txt_pln, min_txt, None, font, 'Center', 'Top')
                result.append(d_txt)
        elif projection.title() == 'Stereographic':
            for circle in compass.stereographic_altitude_circles:
                arc_geo = Arc3D.from_arc2d(circle, z)
                result.append(DisplayArc3D(arc_geo, line_width=1, line_type='Dotted'))
            for txt, pt in zip(compass.ALTITUDES, compass.stereographic_altitude_points):
                txt_pln = Plane(o=Point3D(pt.x, pt.y, z), x=xaxis)
                d_txt = DisplayText3D(
                    str(txt), txt_pln, min_txt, None, font, 'Center', 'Top')
                result.append(d_txt)

    # assemble everything into a ContextGeometry and VisualizationSet
    con_geo = ContextGeometry('Compass', result)
    return VisualizationSet('Compass', [con_geo])
