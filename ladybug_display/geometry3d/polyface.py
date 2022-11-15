"""A polyface in 3D space with display properties."""
from ladybug_geometry.geometry3d.polyface import Polyface3D
from ladybug.color import Color

from ._base import _SingleColorModeBase3D


class DisplayPolyface3D(_SingleColorModeBase3D): 
    """A polyface in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Polyface3D.
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
        * faces
        * edges
        * naked_edges
        * internal_edges
        * non_manifold_edges
        * face_indices
        * edge_indices
        * edge_types
        * min
        * max
        * center
        * area
        * volume
        * is_solid
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, display_mode='Surface'):
        """Initialize base with shade object."""
        assert isinstance(geometry, Polyface3D), '\
            Expected ladybug_geometry Polyface3D. Got {}'.format(type(geometry))
        _SingleColorModeBase3D.__init__(self, geometry, color, display_mode)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayPolyface3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayPolyface3D object.
        """
        assert data['type'] == 'DisplayPolyface3D', \
            'Expected DisplayPolyface3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        d_mode = data['display_mode'] if 'display_mode' in data and \
            data['display_mode'] is not None else 'Surface'
        geo = cls(Polyface3D.from_dict(data['geometry']), color, d_mode)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def vertices(self):
        """Get a tuple of vertices in the polyface."""
        return self._geometry.vertices

    @property
    def faces(self):
        """Get a tuple of all Face3D objects making up this polyface."""
        return self._geometry.faces

    @property
    def edges(self):
        """Get a tuple of all edges in this polyface as LineSegment3D objects."""
        return self._geometry.edges

    @property
    def naked_edges(self):
        """Get a tuple of all naked edges in this polyface as LineSegment3D objects."""
        return self._geometry.naked_edges

    @property
    def internal_edges(self):
        """Get a tuple of all internal edges in this polyface as LineSegment3D objects.
        """
        return self._geometry.internal_edges

    @property
    def non_manifold_edges(self):
        """Get a tuple of all non-manifold edges as LineSegment3D objects."""
        return self._geometry.non_manifold_edges

    @property
    def face_indices(self):
        """Get a tuple of face tuples with integers corresponding to indices of vertices.
        """
        return self._geometry.face_indices

    @property
    def edge_indices(self):
        """Get a tuple of edge tuples with integers corresponding to indices of vertices.
        """
        return self._geometry.edge_indices

    @property
    def edge_types(self):
        """Get a tuple of integers for each edge that denotes the type of edge.

        0 denotes a naked edge, 1 denotes an internal edge, and anything higher is a
        non-manifold edge.
        """
        return self._geometry.edge_types

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
        """Get the area of the polyface."""
        return self._geometry.area

    @property
    def volume(self):
        """Get the volume of the polyface."""
        return self._geometry.volume

    @property
    def is_solid(self):
        """Get a boolean to note whether the polyface is solid (True) or is open (False).
        """
        return self._geometry.is_solid

    def to_dict(self):
        """Return DisplayPolyface3D as a dictionary."""
        base = {'type': 'DisplayPolyface3D'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['display_mode'] = self.display_mode
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayPolyface3D(self.geometry, self.color, self.display_mode)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayPolyface3D: {}'.format(self.geometry)
