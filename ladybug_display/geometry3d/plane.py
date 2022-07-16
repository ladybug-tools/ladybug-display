"""A plane that can be displayed in 3D space."""
from ladybug_geometry.geometry3d.plane import Plane
from ladybug.color import Color

from ._base import _SingleColorBase3D


class DisplayPlane(_SingleColorBase3D):
    """A plane in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Plane object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        show_axes: A boolean to note whether the plane should be displayed with
            XY axes instead of just an origin point and a normal vector.
        show_grid: A boolean to note whether the plane should be displayed
            with a grid.

    Properties:
        * geometry
        * color
        * show_axes
        * show_grid
        * o
        * n
        * x
        * y
        * k
        * user_data
    """
    __slots__ = ('_show_axes', '_show_grid')

    def __init__(self, geometry, color=None, show_axes=False, show_grid=False):
        """Initialize base with shade object."""
        assert isinstance(geometry, Plane), '\
            Expected ladybug_geometry Plane. Got {}'.format(type(geometry))
        _SingleColorBase3D.__init__(self, geometry, color)
        self.show_axes = show_axes
        self.show_grid = show_grid

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayPlane from a dictionary.

        Args:
            data: A dictionary representation of an DisplayPlane object.
        """
        assert data['type'] == 'DisplayPlane', \
            'Expected DisplayPlane dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        ax = data['show_axes'] if 'show_axes' in data else False
        gd = data['show_grid'] if 'show_grid' in data else False
        geo = cls(Plane.from_dict(data['geometry']), color, ax, gd)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def show_axes(self):
        """Get or set a boolean for whether to display the XY axes of the plane."""
        return self._show_axes

    @show_axes.setter
    def show_axes(self, value):
        try:
            self._show_axes = bool(value)
        except TypeError:
            raise TypeError(
                'Expected boolean for DisplayPlane.show_axes. Got {}.'.format(value))

    @property
    def show_grid(self):
        """Get or set a boolean for whether to display the grid of the plane."""
        return self._show_grid

    @show_grid.setter
    def show_grid(self, value):
        try:
            self._show_grid = bool(value)
        except TypeError:
            raise TypeError(
                'Expected boolean for DisplayPlane.show_grid. Got {}.'.format(value))

    @property
    def o(self):
        """Get a Point3D representing the origin of the plane."""
        return self._geometry.o

    @property
    def n(self):
        """Get a Vector3D representing the normal of the plane."""
        return self._geometry.n

    @property
    def x(self):
        """Get  aVector3D representing the x axis of the plane."""
        return self._geometry.x

    @property
    def y(self):
        """Get a Vector3D representing the y axis of the plane."""
        return self._geometry.y

    @property
    def k(self):
        """Get a number for the constant of the plane."""
        return self._geometry.k

    def to_dict(self):
        """Return DisplayPlane as a dictionary."""
        base = {'type': 'DisplayPlane'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['show_axes'] = self.show_axes
        base['show_grid'] = self.show_grid
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayPlane(self.geometry, self.color, self.show_axes, self.show_grid)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayPlane: {}'.format(self.geometry)
