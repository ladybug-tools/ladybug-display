"""A polyline that can be displayed in 3D space."""
from ladybug_geometry.geometry3d.polyline import Polyline3D
from ladybug.color import Color

from ladybug_display.altnumber import default
from ._base import _LineCurveBase3D


class DisplayPolyline3D(_LineCurveBase3D):
    """A polyline in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Polyline3D object.
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
        assert isinstance(geometry, Polyline3D), '\
            Expected ladybug_geometry Polyline3D. Got {}'.format(type(geometry))
        _LineCurveBase3D.__init__(self, geometry, color, line_width, line_type)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayPolyline3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayPolyline3D object.
        """
        assert data['type'] == 'DisplayPolyline3D', \
            'Expected DisplayPolyline3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        lw = default if 'line_width' not in data or \
            data['line_width'] == default.to_dict() else data['line_width']
        lt = data['line_type'] if 'line_type' in data and data['line_type'] \
            is not None else 'Continuous'
        geo = cls(Polyline3D.from_dict(data['geometry']), color, lw, lt)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def vertices(self):
        """Get a tuple of Point3D for the vertices of the polyline."""
        return self._geometry.vertices

    @property
    def segments(self):
        """Get a tuple of LineSegment3D for the segments of the polyline."""
        return self._geometry.segments

    @property
    def interpolated(self):
        """Get a boolean for whether the polyline should be interpreted as interpolated.
        """
        return self._geometry.interpolated

    @property
    def p1(self):
        """Get a Point3D representing the first end point of the polyline."""
        return self._geometry.p1

    @property
    def p2(self):
        """Get a Point3D representing the second end point of the polyline."""
        return self._geometry.p2

    @property
    def length(self):
        """Get a number for the length of the polyline."""
        return self._geometry.length

    @property
    def min(self):
        """Get a Point3D for the minimum of the bounding box around the object."""
        return self._geometry.min

    @property
    def max(self):
        """Get a Point3D for the maximum of the bounding box around the object."""
        return self._geometry.max

    def to_dict(self):
        """Return DisplayPolyline3D as a dictionary."""
        base = {'type': 'DisplayPolyline3D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['line_width'] = default.to_dict() if \
            self.line_width == default else self.line_width
        base['line_type'] = self.line_type
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayPolyline3D(
            self.geometry, self.color, self.line_width, self.line_type)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayPolyline3D: {}'.format(self.geometry)
