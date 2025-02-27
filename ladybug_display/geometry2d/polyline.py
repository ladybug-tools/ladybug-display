"""A polyline that can be displayed in 2D space."""
from __future__ import division

from ladybug_geometry.geometry2d.polyline import Polyline2D
from ladybug.color import Color

from ladybug_display.altnumber import default
import ladybug_display.svg as svg
from ladybug_display._base import DASH_ARRAYS
from ._base import _LineCurveBase2D


class DisplayPolyline2D(_LineCurveBase2D):
    """A polyline in 2D space with display properties.

    Args:
        geometry: A ladybug-geometry Polyline2D object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        line_width: Number for line width in pixels (for the screen). For print,
            this will be converted a value in millimeters or inches assuming
            standard web resolution (72 pixels per inch). This can also be the
            Default object to indicate that the default settings of the
            interface should be used (typically one pixel).
        line_type: Get or set text to indicate the type of line to display.
            Choose from the following. (Default: "Continuous")

            * Continuous
            * Dashed
            * Dotted
            * DashDot

    Properties:
        * geometry
        * color
        * line_width
        * line_type
        * vertices
        * segments
        * interpolated
        * p1
        * p2
        * length
        * min
        * max
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, line_width=default, line_type='Continuous'):
        """Initialize base with shade object."""
        assert isinstance(geometry, Polyline2D), '\
            Expected ladybug_geometry Polyline2D. Got {}'.format(type(geometry))
        _LineCurveBase2D.__init__(self, geometry, color, line_width, line_type)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayPolyline2D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayPolyline2D object.
        """
        assert data['type'] == 'DisplayPolyline2D', \
            'Expected DisplayPolyline2D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        lw = default if 'line_width' not in data or \
            data['line_width'] == default.to_dict() else data['line_width']
        lt = data['line_type'] if 'line_type' in data and data['line_type'] \
            is not None else 'Continuous'
        geo = cls(Polyline2D.from_dict(data['geometry']), color, lw, lt)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def vertices(self):
        """Get a tuple of Point2D for the vertices of the polyline."""
        return self._geometry.vertices

    @property
    def segments(self):
        """Get a tuple of LineSegment2D for the segments of the polyline."""
        return self._geometry.segments

    @property
    def interpolated(self):
        """Get a boolean for whether the polyline should be interpreted as interpolated.
        """
        return self._geometry.interpolated

    @property
    def p1(self):
        """Get a Point2D representing the first end point of the polyline."""
        return self._geometry.p1

    @property
    def p2(self):
        """Get a Point2D representing the second end point of the polyline."""
        return self._geometry.p2

    @property
    def length(self):
        """Get a number for the length of the polyline."""
        return self._geometry.length

    @property
    def min(self):
        """Get a Point2D for the minimum of the bounding box around the object."""
        return self._geometry.min

    @property
    def max(self):
        """Get a Point2D for the maximum of the bounding box around the object."""
        return self._geometry.max

    def to_dict(self):
        """Return DisplayPolyline2D as a dictionary."""
        base = {'type': 'DisplayPolyline2D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['line_width'] = default.to_dict() if \
            self.line_width == default else self.line_width
        base['line_type'] = self.line_type
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def to_svg(self):
        """Return DisplayPolyline2D as an SVG Element."""
        element = self.polyline2d_to_svg(self.geometry)
        element.stroke = self.color.to_hex()
        if self.color.a != 255:
            element.opacity = self.color.a / 255
        if self.line_width != default:
            element.stroke_width = self.line_width
        if self.line_type != 'Continuous':
            element.stroke_dasharray = DASH_ARRAYS[self.line_type]
        return element

    @staticmethod
    def polyline2d_to_svg(polyline):
        """SVG Polyline or Path element from ladybug-geometry Polyline2D."""
        if not polyline.interpolated:
            points = []
            for pt in polyline.vertices:
                points.append(pt.x)
                points.append(-pt.y)
            element = svg.Polyline(points=points)
        else:  # convert the polyline to a cubic Bezier curve
            element = DisplayPolyline2D._polyline2d_to_cubic_bezier_svg(polyline)
        element.fill = 'none'
        element.stroke = 'black'
        element.stroke_width = 1
        return element

    @staticmethod
    def _polyline2d_to_cubic_bezier_svg(polyline):
        """SVG Path from ladybug-geometry Polyline2D."""
        alpha = 0.5  # for a centripetal Catmull–Rom spline
        # https://en.wikipedia.org/wiki/Centripetal_Catmull%E2%80%93Rom_spline

        def tj(ti, pi, pj):
            """Get the parameter given that previous parameter and two points."""
            dx, dy = pj.x - pi.x, pj.y - pi.y
            l_val = (dx ** 2 + dy ** 2) ** 0.5
            return ti + l_val ** alpha

        # loop though the vertices and gather the control points
        vertices = polyline.vertices
        control_points = []
        for i, pt in enumerate(vertices):
            p0, p1, p2 = vertices[i - 2], vertices[i - 1], pt
            t0 = 0.0
            t1 = tj(t0, p0, p1)
            t2 = tj(t1, p1, p2)
            c1 = (t2 - t1) / (t2 - t0)
            c2 = (t1 - t0) / (t2 - t0)
            try:
                m1 = (t2 - t1) * (c1 * (p1 - p0) / (t1 - t0) + c2 * (p2 - p1) / (t2 - t1))
                control_pt = p1 - (m1 / 3)
                control_points.append(control_pt)
            except ZeroDivisionError:
                control_points.append(vertices[i - 1])

        # move the first control point to the end to align with vertices
        control_points.append(control_points.pop(0))

        # reset the start and end points if the shape is not closed
        if not polyline.is_closed(0.001):
            control_points[0] = vertices[0]
            control_points[-1] = vertices[-1]

        # create the smooth cubic bezier path
        start_pt = vertices[0]
        path_d = [svg.MoveTo(x=start_pt.x, y=-start_pt.y)]
        for pt, c_pt in zip(vertices, control_points):
            path_d.append(svg.SmoothCubicBezier(x=pt.x, y=-pt.y, x2=c_pt.x, y2=-c_pt.y))
        return svg.Path(d=path_d)

    def __copy__(self):
        new_g = DisplayPolyline2D(
            self.geometry, self.color, self.line_width, self.line_type)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayPolyline2D: {}'.format(self.geometry)
