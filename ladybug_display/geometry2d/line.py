"""A line segment that can be displayed in 2D space."""
from ladybug_geometry.geometry2d.line import LineSegment2D
from ladybug.color import Color

from ladybug_display.altnumber import default
from ._base import _LineCurveBase2D


class DisplayLineSegment2D(_LineCurveBase2D):
    """A single line segment in 2D space with display properties.

    Args:
        geometry: A ladybug-geometry LineSegment2D object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        line_width: Number for line width in pixels (for the screen) or  millimeters
            (in print). This can also be the Default object to indicate that the
            default settings of the interface should be used.
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
        * p
        * v
        * p1
        * p2
        * length
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, line_width=default, line_type='Continuous'):
        """Initialize base with shade object."""
        assert isinstance(geometry, LineSegment2D), '\
            Expected ladybug_geometry LineSegment2D. Got {}'.format(type(geometry))
        _LineCurveBase2D.__init__(self, geometry, color, line_width, line_type)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayLineSegment2D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayLineSegment2D object.
        """
        assert data['type'] == 'DisplayLineSegment2D', \
            'Expected DisplayLineSegment2D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        lw = default if 'line_width' not in data or \
            data['line_width'] == default.to_dict() else data['line_width']
        lt = data['line_type'] if 'line_type' in data and data['line_type'] \
            is not None else 'Continuous'
        geo = cls(LineSegment2D.from_dict(data['geometry']), color, lw, lt)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def p(self):
        """Get a Point2D representing the base of the line segment."""
        return self._geometry.p

    @property
    def v(self):
        """Get a Vector2D representing the direction of the line segment."""
        return self._geometry.v

    @property
    def p1(self):
        """Get a Point2D representing the first point of the line segment."""
        return self._geometry.p1

    @property
    def p2(self):
        """Get a Point2D representing the second point of the line segment."""
        return self._geometry.p2

    @property
    def length(self):
        """Get a number for the length of the line segment."""
        return self._geometry.length

    def to_dict(self):
        """Return DisplayLineSegment2D as a dictionary."""
        base = {'type': 'DisplayLineSegment2D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['line_width'] = default.to_dict() if \
            self.line_width == default else self.line_width
        base['line_type'] = self.line_type
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayLineSegment2D(
            self.geometry, self.color, self.line_width, self.line_type)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayLineSegment2D: {}'.format(self.geometry)
