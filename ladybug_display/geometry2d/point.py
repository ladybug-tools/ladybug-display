"""A point that can be displayed in 2D space."""
from ladybug_geometry.geometry2d.pointvector import Point2D
from ladybug.color import Color

from ._base import _SingleColorBase2D
from ladybug_display.altnumber import default
from ladybug_display.typing import float_positive


class DisplayPoint2D(_SingleColorBase2D):
    """A point in 2D space with display properties.

    Args:
        geometry: A ladybug-geometry Point2D object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        radius: Number for radius in pixels (for the screen) or millimeters
            (in print). This can also be the Default object to indicate that the
            default settings of the interface should be used.

    Properties:
        * geometry
        * color
        * radius
        * x
        * y
        * user_data
    """
    __slots__ = ('_radius',)

    def __init__(self, geometry, color=None, radius=default):
        """Initialize base with shade object."""
        assert isinstance(geometry, Point2D), '\
            Expected ladybug_geometry Point2D. Got {}'.format(type(geometry))
        _SingleColorBase2D.__init__(self, geometry, color)
        self.radius = radius

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayPoint2D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayPoint2D object.
        """
        assert data['type'] == 'DisplayPoint2D', \
            'Expected DisplayPoint2D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        rad = default if 'radius' not in data or \
            data['radius'] == default.to_dict() else data['radius']
        geo = cls(Point2D.from_dict(data['geometry']), color, rad)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def radius(self):
        """Get or set a number for the radius of this object."""
        return self._radius

    @radius.setter
    def radius(self, value):
        if value == default:
            self._radius = default
        else:
            self._radius = float_positive(value, 'point radius')

    @property
    def x(self):
        """Get the X coordinate."""
        return self._geometry.x

    @property
    def y(self):
        """Get the Y coordinate."""
        return self._geometry.y

    def distance_to_point(self, point):
        """Get the distance from this point to another DisplayPoint2D."""
        return self.geometry.distance_to_point(point.geometry)

    def to_dict(self):
        """Return DisplayPoint2D as a dictionary."""
        base = {'type': 'DisplayPoint2D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['radius'] = default.to_dict() if self.radius == default else self.radius
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayPoint2D(self.geometry, self.color, self.radius)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __getitem__(self, key):
        return (self.x, self.y)[key]

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return 'DisplayPoint2D: {}'.format(self.geometry)
