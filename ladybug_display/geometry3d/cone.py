# coding=utf-8
"""A cone that can be displayed in 3D space."""
from __future__ import division

from ladybug_geometry.geometry3d import Cone, LineSegment3D
from ladybug.color import Color

import ladybug_display.svg as svg
from .point import DisplayPoint3D
from .line import DisplayLineSegment3D
from .arc import DisplayArc3D
from ._base import _SingleColorModeBase3D


class DisplayCone(_SingleColorModeBase3D):
    """A cone in 3D space with display properties.

    Args:
        geometry: A ladybug-geometry Cone.
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
        * vertex
        * axis
        * height
        * radius
        * area
        * volume
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry, color=None, display_mode='Surface'):
        """Initialize base with shade object."""
        assert isinstance(geometry, Cone), '\
            Expected ladybug_geometry Cone. Got {}'.format(type(geometry))
        _SingleColorModeBase3D.__init__(self, geometry, color, display_mode)

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayCone from a dictionary.

        Args:
            data: A dictionary representation of an DisplayCone object.
        """
        assert data['type'] == 'DisplayCone', \
            'Expected DisplayCone dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        d_mode = data['display_mode'] if 'display_mode' in data and \
            data['display_mode'] is not None else 'Surface'
        geo = cls(Cone.from_dict(data['geometry']), color, d_mode)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def vertex(self):
        """Get a Point3D for the vertex of the cone."""
        return self._geometry.vertex

    @property
    def axis(self):
        """Get a Vector3D for the axis of the cone."""
        return self._geometry.axis

    @property
    def height(self):
        """Get a number for the height of the cone."""
        return self._geometry.height

    @property
    def radius(self):
        """Get the radius of the cone."""
        return self._geometry.radius

    @property
    def area(self):
        """Get the surface area of the cone."""
        return self._geometry.area

    @property
    def volume(self):
        """Get the volume of the cone."""
        return self._geometry.volume

    def to_dict(self):
        """Return DisplayCone as a dictionary."""
        base = {'type': 'DisplayCone'}
        base['geometry'] = self._geometry.to_dict()
        base['color'] = self.color.to_dict()
        base['display_mode'] = self.display_mode
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def to_svg(self):
        """Return DisplayCone as an SVG Element."""
        # convert all of the geometry to polygons or points
        element = self.cone_to_svg(self.geometry, self.display_mode)
        if self.color != Color(0, 0, 0):
            col = self.color.to_hex()
            if self.display_mode == 'Wireframe':
                for obj in element.elements:
                    obj.stroke = col
            else:
                for obj in element.elements:
                    if hasattr(obj, 'fill'):
                        obj.fill = col
            if self.color.a != 255:
                element.opacity = self.color.a / 255
        return element

    @staticmethod
    def cone_to_svg(cone, display_mode='Surface'):
        """SVG Group of Path and line elements from ladybug-geometry Cone."""
        # convert all of the geometry to polygons or points
        geo = []
        base = cone.base
        base_svg = DisplayArc3D.arc3d_to_svg(base)
        if display_mode.startswith('Surface'):
            base_svg.fill = 'grey'
            if display_mode == 'Surface':
                base_svg.stroke_width = 0
        geo.append(base_svg)
        if display_mode == 'Points':
            geo.append(DisplayPoint3D.point3d_to_svg(cone.vertex))
        else:
            for pt in base.subdivide_evenly(30):
                line = LineSegment3D.from_end_points(pt, cone.vertex)
                line_svg = DisplayLineSegment3D.linesegment3d_to_svg(line)
                line_svg.stroke_width = 1
                if display_mode in ('Wireframe', 'SurfaceWithEdges'):
                    line_svg.stroke = 'black'
                else:
                    line_svg.stroke = 'grey'
                geo.append(line_svg)
        # group the geometries together and return them
        element = svg.G()
        element.elements = geo
        return element

    def __copy__(self):
        new_g = DisplayCone(self.geometry, self.color, self.display_mode)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayCone: {}'.format(self.geometry)
