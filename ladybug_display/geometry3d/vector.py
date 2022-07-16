"""A vector that can be displayed in 3D space."""
import math

from ladybug_geometry.geometry3d.pointvector import Vector3D
from ladybug.color import Color

from .._base import _DisplayBase


class DisplayVector3D(_DisplayBase):
    """A vector in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Vector3D object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).

    Properties:
        * geometry
        * color
        * x
        * y
        * z
        * magnitude
        * user_data
    """
    __slots__ = ('_color',)

    def __init__(self, geometry, color=None):
        """Initialize base with shade object."""
        assert isinstance(geometry, Vector3D), '\
            Expected ladybug_geometry Vector3D. Got {}'.format(type(geometry))
        _DisplayBase.__init__(self, geometry)
        self.color = color

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayVector3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayVector3D object.
        """
        assert data['type'] == 'DisplayVector3D', \
            'Expected DisplayVector3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        geo = cls(Vector3D.from_dict(data['geometry']), color)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def color(self):
        """Get or set a color for this object."""
        return self._color

    @color.setter
    def color(self, value):
        if value is None:
            value = Color(0, 0, 0)
        else:
            assert isinstance(value, Color), 'Expected Color for ladybug_display ' \
                'object color. Got {}.'.format(type(value))
        self._color = value

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

    @property
    def magnitude(self):
        """Get the magnitude of the vector."""
        return self._geometry.magnitude

    def normalize(self):
        """Ensure that this DisplayVector3D is a unit vector (magnitude=1)."""
        self._geometry = self._geometry.normalize()

    def reverse(self):
        """Reverse this DisplayVector3D."""
        self._geometry = self._geometry.__neg__()

    def dot(self, other):
        """Get the dot product of this vector with another DisplayVector3D."""
        return self.geometry.dot(other.geometry)

    def cross(self, other):
        """Get the cross product of this vector and another DisplayVector3D."""
        return self.geometry.cross(other.geometry)

    def angle(self, other):
        """Get the angle between this vector and another DisplayVector3D in degrees."""
        return math.degrees(self.geometry.angle(other.geometry))

    def rotate(self, axis, angle):
        """Rotate this geometry by a certain angle around an axis and origin.

        Args:
            axis: A ladybug_geometry Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in degrees.
        """
        self._geometry = self.geometry.rotate(axis, math.radians(angle))

    def rotate_xy(self, angle):
        """Rotate this geometry counterclockwise in the world XY plane by an angle.

        Args:
            angle: An angle in degrees.
        """
        self._geometry = self.geometry.rotate_xy(math.radians(angle))

    def reflect(self, normal):
        """Reflect this geometry across a plane with the input normal vector.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the vector will be reflected. THIS VECTOR MUST BE NORMALIZED.
        """
        self._geometry = self.geometry.reflect(normal)

    def to_dict(self):
        """Return DisplayVector3D as a dictionary.
        """
        base = {'type': 'DisplayVector3D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayVector3D(self.geometry, self.color)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __getitem__(self, key):
        return (self.x, self.y, self.z)[key]

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __mul__(self, other):
        assert type(other) in (int, float), 'Cannot multiply types {} and {}'.format(
            self.__class__.__name__, type(other))
        new_g = DisplayVector3D(self.geometry * other, self.color)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __div__(self, other):
        assert type(other) in (int, float), 'Cannot divide types {} and {}'.format(
            self.__class__.__name__, type(other))
        new_g = DisplayVector3D(self.geometry / other, self.color)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayVector3D: {}'.format(self.geometry)
