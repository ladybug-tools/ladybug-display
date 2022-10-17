"""A point that can be displayed in 3D space."""
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug.color import Color

from ._base import _SingleColorBase3D
from ladybug_display.altnumber import default
from ladybug_display.typing import float_positive


class DisplayPoint3D(_SingleColorBase3D):
    """A point in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Point3D object.
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
        * z
        * user_data
    """
    __slots__ = ('_radius',)

    def __init__(self, geometry, color=None, radius=default):
        """Initialize base with shade object."""
        assert isinstance(geometry, Point3D), '\
            Expected ladybug_geometry Point3D. Got {}'.format(type(geometry))
        _SingleColorBase3D.__init__(self, geometry, color)
        self.radius = radius

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayPoint3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayPoint3D object.
        """
        assert data['type'] == 'DisplayPoint3D', \
            'Expected DisplayPoint3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        rad = default if 'radius' not in data or \
            data['radius'] == default.to_dict() else data['radius']
        geo = cls(Point3D.from_dict(data['geometry']), color, rad)
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

    @property
    def z(self):
        """Get the Z coordinate."""
        return self._geometry.z

    def distance_to_point(self, point):
        """Get the distance from this point to another DisplayPoint3D."""
        return self.geometry.distance_to_point(point.geometry)

    def to_dict(self):
        """Return DisplayPoint3D as a dictionary."""
        base = {'type': 'DisplayPoint3D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['radius'] = default.to_dict() if self.radius == default else self.radius
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayPoint3D(self.geometry, self.color, self.radius)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __getitem__(self, key):
        return (self.x, self.y, self.z)[key]

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __repr__(self):
        return 'DisplayPoint3D: {}'.format(self.geometry)
