"""A sphere that can be displayed in 3D space."""
from ladybug_geometry.geometry3d.sphere import Sphere
from ladybug.color import Color

from ._base import _SingleColorModeBase3D


class DisplaySphere(_SingleColorModeBase3D):
    """A sphere in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Sphere.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        display_mode: Text to indicate the display mode (surface, wireframe, etc.).
            Choose from the following. (Default: Surface).

            * Surface
            * SurfaceWithEdges
            * Wireframe
            * Points

    Properties:
        * geometry
        * color
        * display_mode
        * center
        * radius
        * min
        * max
        * diameter
        * circumference
        * area
        * volume
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, display_mode='Surface'):
        """Initialize base with shade object."""
        assert isinstance(geometry, Sphere), '\
            Expected ladybug_geometry Sphere. Got {}'.format(type(geometry))
        _SingleColorModeBase3D.__init__(self, geometry, color, display_mode)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplaySphere from a dictionary.

        Args:
            data: A dictionary representation of an DisplaySphere object.
        """
        assert data['type'] == 'DisplaySphere', \
            'Expected DisplaySphere dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        d_mode = data['display_mode'] if 'display_mode' in data and \
            data['display_mode'] is not None else 'Surface'
        geo = cls(Sphere.from_dict(data['geometry']), color, d_mode)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def center(self):
        """Get a Point3D for the center of the sphere."""
        return self._geometry.center

    @property
    def radius(self):
        """Get a number for the radius of the sphere."""
        return self._geometry.radius

    @property
    def min(self):
        """Get a Point3D for the minimum of the bounding box around the object."""
        return self._geometry.min

    @property
    def max(self):
        """Get a Point3D for the maximum of the bounding box around the object."""
        return self._geometry.max

    @property
    def diameter(self):
        """Get the diameter of the sphere."""
        return self._geometry.diameter

    @property
    def circumference(self):
        """Get the circumference of the sphere."""
        return self._geometry.circumference

    @property
    def area(self):
        """Get the surface area of the sphere."""
        return self._geometry.area

    @property
    def volume(self):
        """Get the volume of the sphere."""
        return self._geometry.volume

    def to_dict(self):
        """Return DisplaySphere as a dictionary."""
        base = {'type': 'DisplaySphere'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['display_mode'] = self.display_mode
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplaySphere(self.geometry, self.color, self.display_mode)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplaySphere: {}'.format(self.geometry)
