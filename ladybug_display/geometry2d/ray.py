"""A ray that can be displayed in 2D space."""
from ladybug_geometry.geometry2d.ray import Ray2D
from ladybug.color import Color

from ._base import _SingleColorBase2D


class DisplayRay2D(_SingleColorBase2D):
    """A ray in 2D space with display properties.

    Args:
        geometry: A ladybug-geometry Ray2D object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).

    Properties:
        * geometry
        * color
        * p
        * v
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None):
        """Initialize base with shade object."""
        assert isinstance(geometry, Ray2D), '\
            Expected ladybug_geometry Ray2D. Got {}'.format(type(geometry))
        _SingleColorBase2D.__init__(self, geometry, color)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayRay2D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayRay2D object.
        """
        assert data['type'] == 'DisplayRay2D', \
            'Expected DisplayRay2D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        geo = cls(Ray2D.from_dict(data['geometry']), color)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def p(self):
        """Get a Point2D representing the base of the ray."""
        return self._geometry.p

    @property
    def v(self):
        """Get a Vector2D representing the direction of the ray."""
        return self._geometry.v

    def reverse(self):
        """Reverse this DisplayRay2D."""
        self._geometry = self._geometry.reverse()

    def to_dict(self):
        """Return DisplayRay2D as a dictionary."""
        base = {'type': 'DisplayRay2D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayRay2D(self.geometry, self.color)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayRay2D: {}'.format(self.geometry)
