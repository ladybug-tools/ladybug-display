"""An arc that can be displayed in 3D space."""
from __future__ import division
import math

from ladybug_geometry.geometry2d import Point2D, Arc2D
from ladybug_geometry.geometry3d import Vector3D, Arc3D
from ladybug.color import Color

from ladybug_display.altnumber import default
from ladybug_display._base import DASH_ARRAYS
from ..geometry2d import DisplayArc2D, DisplayPolyline2D
from ._base import _LineCurveBase3D


class DisplayArc3D(_LineCurveBase3D):
    """An arc in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Arc3D object.
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
        * plane
        * radius
        * p1
        * p2
        * c
        * angle
        * length
        * is_circle
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, line_width=default, line_type='Continuous'):
        """Initialize base with shade object."""
        assert isinstance(geometry, Arc3D), '\
            Expected ladybug_geometry Arc3D. Got {}'.format(type(geometry))
        _LineCurveBase3D.__init__(self, geometry, color, line_width, line_type)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayArc3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayArc3D object.
        """
        assert data['type'] == 'DisplayArc3D', \
            'Expected DisplayArc3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        lw = default if 'line_width' not in data or \
            data['line_width'] == default.to_dict() else data['line_width']
        lt = data['line_type'] if 'line_type' in data and data['line_type'] \
            is not None else 'Continuous'
        geo = cls(Arc3D.from_dict(data['geometry']), color, lw, lt)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def plane(self):
        """Get a Plane which the arc lies with an origin representing the center."""
        return self._geometry.plane

    @property
    def radius(self):
        """Get a number for the radius of the arc."""
        return self._geometry.radius

    @property
    def p1(self):
        """Get a Point3D representing the first end point of the arc."""
        return self._geometry.p1

    @property
    def p2(self):
        """Get a Point3D representing the second end point of the arc."""
        return self._geometry.p2

    @property
    def c(self):
        """Get a Point3D representing the center of the arc."""
        return self._geometry.c

    @property
    def angle(self):
        """The total angle over the domain of the arc in degrees."""
        return math.degrees(self._geometry.angle)

    @property
    def length(self):
        """Get a number for the length of the arc."""
        return self._geometry.length

    @property
    def is_circle(self):
        """Get a boolean for whether the arc is a circle."""
        return self._geometry.is_circle

    def to_dict(self):
        """Return DisplayArc3D as a dictionary."""
        base = {'type': 'DisplayArc3D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['line_width'] = default.to_dict() if \
            self.line_width == default else self.line_width
        base['line_type'] = self.line_type
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def to_svg(self):
        """Return DisplayArc3D as an SVG Element."""
        element = self.arc3d_to_svg(self.geometry)
        element.stroke = self.color.to_hex()
        if self.color.a != 255:
            element.opacity = self.color.a / 255
        if self.line_width != default:
            element.stroke_width = self.line_width
        if self.line_type != 'Continuous':
            element.stroke_dasharray = DASH_ARRAYS[self.line_type]
        return element

    @staticmethod
    def arc3d_to_svg(arc):
        """SVG Circle or Path element from ladybug-geometry Arc3D."""
        xy_angle = math.degrees(arc.plane.n.angle(Vector3D(0, 0, 1)))
        if xy_angle < 1 or xy_angle > 179:  # close enough to represent with circle
            origin = arc.plane.o
            arc_2d = Arc2D(Point2D(origin.x, origin.y), arc.radius, arc.a1, arc.a2)
            return DisplayArc2D.arc2d_to_svg(arc_2d)
        else:  # project to XY as an interpolated polyline
            p_line = arc.to_polyline(30, interpolated=True)
            return DisplayPolyline2D.polyline2d_to_svg(p_line)

    def __copy__(self):
        new_g = DisplayArc3D(
            self.geometry, self.color, self.line_width, self.line_type)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayArc3D: {}'.format(self.geometry)
