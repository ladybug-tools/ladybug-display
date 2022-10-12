"""A single planar face that can be displayed in 3D space."""
import math

from ladybug_geometry.geometry3d.face import Face3D
from ladybug.color import Color

from ._base import _SingleColorModeBase3D


class DisplayFace3D(_SingleColorModeBase3D):
    """A single planar face in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Face3D.
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
        * vertices
        * normal
        * center
        * area
        * perimeter
        * min
        * max
        * altitude
        * azimuth
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, display_mode='Surface'):
        """Initialize object."""
        assert isinstance(geometry, Face3D), '\
            Expected ladybug_geometry Face3D. Got {}'.format(type(geometry))
        _SingleColorModeBase3D.__init__(self, geometry, color, display_mode)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayFace3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayFace3D object.
        """
        assert data['type'] == 'DisplayFace3D', \
            'Expected DisplayFace3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        d_mode = data['display_mode'] if 'display_mode' in data and \
            data['display_mode'] is not None else 'Surface'
        geo = cls(Face3D.from_dict(data['geometry']), color, d_mode)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def vertices(self):
        """Get a list of vertices for the face (in counter-clockwise order)."""
        return self._geometry.vertices

    @property
    def normal(self):
        """Get a Vector3D for the direction in which the face is pointing.
        """
        return self._geometry.normal

    @property
    def center(self):
        """Get a Point3D for the center of the face.

        Note that this is the center of the bounding rectangle around this geometry
        and not the area centroid.
        """
        return self._geometry.center

    @property
    def area(self):
        """Get the area of the face."""
        return self._geometry.area

    @property
    def perimeter(self):
        """Get the perimeter of the face. This includes the length of holes in the face.
        """
        return self._geometry.perimeter

    @property
    def min(self):
        """Get a Point3D for the minimum of the bounding box around the object."""
        return self._geometry.min

    @property
    def max(self):
        """Get a Point3D for the maximum of the bounding box around the object."""
        return self._geometry.max

    @property
    def altitude(self):
        """Get the altitude of the geometry between +90 (up) and -90 (down)."""
        return math.degrees(self._geometry.altitude)

    @property
    def azimuth(self):
        """Get the azimuth of the geometry, between 0 and 360.

        Given Y-axis as North, 0 = North, 90 = East, 180 = South, 270 = West
        This will be zero if the Face3D is perfectly horizontal.
        """
        return math.degrees(self._geometry.azimuth)

    def to_dict(self, include_plane=True):
        """Return DisplayFace3D as a dictionary.

        Args:
            include_plane: Boolean to note wether the plane of the Face3D should be
                included in the output. This can preserve the orientation of the
                X/Y axes of the plane but is not required and can be removed to
                keep the dictionary smaller. (Default: True).
        """
        base = {'type': 'DisplayFace3D'}
        base['geometry'] = self._geometry.to_dict(include_plane)
        base['color'] = self.color.to_dict()
        base['display_mode'] = self.display_mode
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayFace3D(self.geometry, self.color, self.display_mode)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayFace3D: {}'.format(self.geometry)
