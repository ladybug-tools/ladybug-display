"""A polygon that can be displayed in 2D space."""
from ladybug_geometry.geometry2d.polygon import Polygon2D
from ladybug.color import Color

from ladybug_display.altnumber import default
from ._base import _LineCurveBase2D


class DisplayPolygon2D(_LineCurveBase2D):
    """A polygon in 2D space with display properties.

    Args:
        geometry: A ladybug-geometry Polygon2D object.
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
        * min
        * max
        * center
        * perimeter
        * area
        * is_clockwise
        * is_convex
        * is_self_intersecting
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, line_width=default, line_type='Continuous'):
        """Initialize base with shade object."""
        assert isinstance(geometry, Polygon2D), '\
            Expected ladybug_geometry Polygon2D. Got {}'.format(type(geometry))
        _LineCurveBase2D.__init__(self, geometry, color, line_width, line_type)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayPolygon2D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayPolygon2D object.
        """
        assert data['type'] == 'DisplayPolygon2D', \
            'Expected DisplayPolygon2D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        lw = default if 'line_width' not in data or \
            data['line_width'] == default.to_dict() else data['line_width']
        lt = data['line_type'] if 'line_type' in data and data['line_type'] \
            is not None else 'Continuous'
        geo = cls(Polygon2D.from_dict(data['geometry']), color, lw, lt)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def vertices(self):
        """Get a tuple of Point2Ds that make up the polygon."""
        return self._geometry.vertices

    @property
    def segments(self):
        """Get a tuple of LineSegment2Ds that make up the polygon."""
        return self._geometry.segments

    @property
    def min(self):
        """Get a Point2D for the minimum of the bounding box around the object."""
        return self._geometry.min

    @property
    def max(self):
        """Get a Point2D for the maximum of the bounding box around the object."""
        return self._geometry.max

    @property
    def center(self):
        """Get a Point2D for the center of the bounding box around the object."""
        return self._geometry.center

    @property
    def perimeter(self):
        """Get a number for the perimeter of the polygon."""
        return self._geometry.perimeter

    @property
    def area(self):
        """Get a number for the area of the polygon."""
        return self._geometry.area

    @property
    def is_clockwise(self):
        """Get a boolean for whether the polygon is clockwise."""
        return self._geometry.is_clockwise

    @property
    def is_convex(self):
        """Get a boolean for whether the polygon is convex."""
        return self._geometry.is_convex

    @property
    def is_self_intersecting(self):
        """Get a boolean for whether the polygon is self intersecting."""
        return self._geometry.is_self_intersecting

    def to_dict(self):
        """Return DisplayPolygon2D as a dictionary."""
        base = {'type': 'DisplayPolygon2D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['line_width'] = default.to_dict() if \
            self.line_width == default else self.line_width
        base['line_type'] = self.line_type
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayPolygon2D(
            self.geometry, self.color, self.line_width, self.line_type)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayPolygon2D: {}'.format(self.geometry)
