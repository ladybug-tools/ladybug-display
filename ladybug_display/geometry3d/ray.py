"""A ray that can be displayed in 3D space."""
from ladybug_geometry.geometry3d.ray import Ray3D
from ladybug.color import Color

from ._base import _SingleColorBase3D


class DisplayRay3D(_SingleColorBase3D):
    """A ray in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Ray3D object.
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
        assert isinstance(geometry, Ray3D), '\
            Expected ladybug_geometry Ray3D. Got {}'.format(type(geometry))
        _SingleColorBase3D.__init__(self, geometry, color)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayRay3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayRay3D object.
        """
        assert data['type'] == 'DisplayRay3D', \
            'Expected DisplayRay3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        geo = cls(Ray3D.from_dict(data['geometry']), color)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def p(self):
        """Get a Point3D representing the base of the ray."""
        return self._geometry.p

    @property
    def v(self):
        """Get a Vector3D representing the direction of the ray."""
        return self._geometry.v
    
    def reverse(self):
        """Reverse this DisplayRay3D."""
        self._geometry = self._geometry.reverse()

    def to_dict(self):
        """Return DisplayRay3D as a dictionary."""
        base = {'type': 'DisplayRay3D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayRay3D(self.geometry, self.color)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayRay3D: {}'.format(self.geometry)
