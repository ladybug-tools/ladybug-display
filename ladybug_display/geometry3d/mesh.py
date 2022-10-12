"""A mesh in 3D space with display properties."""
from ladybug_geometry.geometry3d.mesh import Mesh3D
from ladybug.color import Color

from .._base import DISPLAY_MODES
from ._base import _DisplayBase3D


class DisplayMesh3D(_DisplayBase3D):
    """A mesh in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Mesh3D.
        colors: A list of colors that correspond to either the faces of the mesh
            or the vertices of the mesh. It can also be a single color for the
            entire mesh. (Default: None).
        display_mode: Text to indicate the display mode (surface, wireframe, etc.).
            Choose from the following. (Default: Surface).

            * Surface
            * SurfaceWithEdges
            * Wireframe
            * Points

    Properties:
        * geometry
        * colors
        * display_mode
        * vertices
        * faces
        * min
        * max
        * center
        * area
        * face_areas
        * face_centroids
        * face_normals
        * vertex_normals
        * user_data
    """
    __slots__ = ('_colors', '_display_mode')

    def __init__(self, geometry, colors=None, display_mode='Surface'):
        """Initialize base with shade object."""
        assert isinstance(geometry, Mesh3D), '\
            Expected ladybug_geometry Mesh3D. Got {}'.format(type(geometry))
        _DisplayBase3D.__init__(self, geometry)
        self.colors = colors
        self.display_mode = display_mode

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayMesh3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayMesh3D object.
        """
        assert data['type'] == 'DisplayMesh3D', \
            'Expected DisplayMesh3D dictionary. Got {}.'.format(data['type'])
        colors = [Color.from_dict(c) for c in data['colors']] if 'colors' in data \
            and data['colors'] is not None else None
        d_mode = data['display_mode'] if 'display_mode' in data and \
            data['display_mode'] is not None else 'Surface'
        geo = cls(Mesh3D.from_dict(data['geometry']), colors, d_mode)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def colors(self):
        """Get or set a tuple of colors for this object.

        The length of this tuple must be either equal to the number or faces or
        vertices of the mesh. Or it can be a tuple with a single color for the
        whole geometry object.
        """
        return self._colors

    @colors.setter
    def colors(self, col):
        if col is None:
            col = (Color(0, 0, 0),)
        else:
            assert isinstance(col, (list, tuple)), \
                'colors should be a list or tuple. Got {}'.format(type(col))
            if isinstance(col, list):
                col = tuple(col)
            l_col = len(col)
            if l_col == 1 or l_col == len(self.faces) or l_col == len(self.vertices):
                pass
            elif l_col == 0:
                col = (Color(0, 0, 0),)
            else:
                msg = 'Number of colors ({}) does not match the number of mesh faces ' \
                    '({}) nor the number of vertices ({}).'.format(
                        len(col), len(self.faces), len(self.vertices))
                raise ValueError(msg)
            assert all(isinstance(v, Color) for v in col), 'Expected Color for ' \
                'ladybug_display object color.'
        self._colors = col

    @property
    def display_mode(self):
        """Get or set text to indicate the display mode."""
        return self._display_mode

    @display_mode.setter
    def display_mode(self, value):
        clean_input = value.lower()
        for key in DISPLAY_MODES:
            if key.lower() == clean_input:
                value = key
                break
        else:
            raise ValueError(
                'display_mode {} is not recognized.\nChoose from the '
                'following:\n{}'.format(value, DISPLAY_MODES))
        self._display_mode = value

    @property
    def vertices(self):
        """Get a tuple of vertices in the mesh."""
        return self._geometry.vertices

    @property
    def faces(self):
        """Get a tuple of all faces in the mesh."""
        return self._geometry.faces

    @property
    def min(self):
        """Get a Point3D for the minimum of the bounding box around the object."""
        return self._geometry.min

    @property
    def max(self):
        """Get a Point3D for the maximum of the bounding box around the object."""
        return self._geometry.max

    @property
    def center(self):
        """Get a Point3D for the center of the bounding box around the object."""
        return self._geometry.center

    @property
    def area(self):
        """Get the area of the mesh."""
        return self._geometry.area

    @property
    def face_areas(self):
        """Get a tuple with the area of each face in the mesh."""
        return self._geometry.face_areas

    @property
    def face_centroids(self):
        """Get a tuple with the centroid of each face in the mesh."""
        return self._geometry.face_centroids

    @property
    def face_normals(self):
        """Get a tuple of Vector3D objects for all face normals."""
        return self._geometry.face_normals

    @property
    def vertex_normals(self):
        """Get a tuple of Vector3D objects for all vertex normals."""
        return self._geometry.vertex_normals

    def to_dict(self):
        """Return DisplayMesh3D as a dictionary."""
        base = {'type': 'DisplayMesh3D'}
        base['geometry'] = self._geometry.to_dict()
        base['colors'] = [c.to_dict() for c in self.colors]
        base['display_mode'] = self.display_mode
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayMesh3D(self.geometry, self.colors, self.display_mode)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayMesh3D: {}'.format(self.geometry)
