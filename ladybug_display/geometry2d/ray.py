"""A ray that can be displayed in 2D space."""
from __future__ import division
import uuid

from ladybug_geometry.geometry2d.ray import Ray2D
from ladybug.color import Color

import ladybug_display.svg as svg
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

    def to_svg(self):
        """Return DisplayRay2D as an SVG Element."""
        element = self.ray2d_to_svg(self.geometry)
        marker, line = element.elements
        line.stroke = self.color.to_hex()
        marker.elements[0].fill = self.color.to_hex()
        if self.color.a != 255:
            element.opacity = self.color.a / 255
        return element

    @staticmethod
    def ray2d_to_svg(ray):
        """SVG Group with Line and Marker elements from ladybug-geometry Ray2D."""
        # create the marker for the arrow
        view_box = svg.ViewBoxSpec(0, 0, 10, 10)
        marker = svg.Marker(viewBox=view_box, refX=5, refY=5,
                            markerWidth=6, markerHeight=6, orient='auto-start-reverse')
        marker.id = 'arrow_{}'.format(str(uuid.uuid4())[:8])
        path = svg.Path(d=[svg.MoveTo(x=0, y=0), svg.LineTo(x=10, y=5),
                           svg.LineTo(x=0, y=10), svg.ClosePath()])
        marker.elements = [path]
        # create the line and add the marker to it
        line = svg.Line(x1=ray.p.x, y1=-ray.p.y,
                        x2=ray.p.x + ray.v.x, y2=-ray.p.y - ray.v.y)
        line.stroke = 'black'
        line.stroke_width = 1
        line.marker_end = "url('#{}')".format(marker.id)
        # put the marker and line together in a group
        element = svg.G()
        element.elements = [marker, line]
        return element

    def __copy__(self):
        new_g = DisplayRay2D(self.geometry, self.color)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayRay2D: {}'.format(self.geometry)
