# coding=utf-8
"""Class for representing geometry objects that each have custom properties.

Such properties can include color, line_width, line_type, and display_mode.
"""
from __future__ import division

from ladybug_geometry.geometry2d import Vector2D, Point2D
from ladybug_geometry.bounding import bounding_box
from ladybug_geometry.projection import project_geometry_2d

from .geometry2d._base import _DisplayBase2D
from .geometry3d._base import _DisplayBase3D
from .geometry3d import DisplayText3D
from .dictutil import dict_to_object

import ladybug_display.svg as svg
from ._base import _VisualizationBase
from .analysis import GEOMETRY_UNION, DISPLAY_UNION, DISPLAY_MAP


class ContextGeometry(_VisualizationBase):
    """An object representing context geometry to display.

    Args:
        identifier: Text string for a unique object ID. Must be less than 100
            characters and not contain spaces or special characters.
        geometry: A list of ladybug-geometry or ladybug-display objects that gives
            context to analysis geometry or other aspects of the visualization.
            Typically, these will display in wireframe around the geometry, though
            the properties of display geometry can be used to customize the
            visualization.
        hidden: A boolean to note whether the geometry is hidden by default and
            must be un-hidden to be visible in the 3D scene. (Default: False).

    Properties:
        * identifier
        * display_name
        * geometry
        * hidden
        * min_point
        * max_point
        * user_data
    """
    __slots__ = ('_geometry', '_min_point', '_max_point', '_hidden')

    def __init__(self, identifier, geometry, hidden=False):
        """Initialize ContextGeometry."""
        _VisualizationBase.__init__(self, identifier)  # process the identifier
        self.geometry = geometry
        self.hidden = hidden
        self._min_point = None
        self._max_point = None

    @classmethod
    def from_dict(cls, data):
        """Create an ContextGeometry from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": "ContextGeometry",
            "identifier": "",  # unique object identifier
            "geometry": [],  # list of ladybug-display geometry objects
            "hidden": True  # boolean for whether the layer is hidden by default
            }
        """
        # check the type key
        assert data['type'] == 'ContextGeometry', \
            'Expected ContextGeometry, Got {}.'.format(data['type'])
        # re-serialize the object
        geos = tuple(dict_to_object(geo) for geo in data['geometry'])
        hidden = False if 'hidden' not in data else data['hidden']
        new_obj = cls(data['identifier'], geos, hidden)
        if 'display_name' in data and data['display_name'] is not None:
            new_obj.display_name = data['display_name']
        if 'user_data' in data and data['user_data'] is not None:
            new_obj.user_data = data['user_data']
        return new_obj

    @property
    def geometry(self):
        """Get or set a tuple of ladybug_display geometry objects for context.

        When setting this property, it is also acceptable to include raw
        ladybug_geometry objects in the list and they will automatically be
        converted into a wireframe representation as a ladybug-display object.
        """
        return self._geometry

    @geometry.setter
    def geometry(self, value):
        assert isinstance(value, (list, tuple)), 'Expected list or tuple for' \
            ' ContextGeometry geometry. Got {}.'.format(type(value))
        processed_value = []
        for geo in value:
            if isinstance(geo, DISPLAY_UNION):
                processed_value.append(geo)
            elif isinstance(geo, GEOMETRY_UNION):
                processed_value.append(self.geometry_to_wireframe(geo))
            else:
                raise ValueError(
                    'Expected ladybug-geometry or ladybug-display object for '
                    'ContextGeometry. Got {}.'.format(type(geo)))
        self._geometry = tuple(processed_value)

    @property
    def hidden(self):
        """Get or set a boolean for whether the geometry is hidden by default."""
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        self._hidden = bool(value)

    @property
    def min_point(self):
        """A Point3D for the minimum bounding box vertex around all of the geometry."""
        if self._min_point is None:
            self._calculate_min_max()
        return self._min_point

    @property
    def max_point(self):
        """A Point3D for the maximum bounding box vertex around all of the geometry."""
        if self._max_point is None:
            self._calculate_min_max()
        return self._max_point

    def move(self, moving_vec):
        """Move this ContextGeometry along a vector.

        Args:
            moving_vec: A ladybug_geometry Vector3D with the direction and distance
                to move the ContextGeometry.
        """
        moving_vec_2d = Vector2D(moving_vec.x, moving_vec.y)
        for geo in self._geometry:
            if isinstance(geo, _DisplayBase3D):
                geo.move(moving_vec)
            elif isinstance(geo, _DisplayBase2D):
                geo.move(moving_vec_2d)

    def rotate_xy(self, angle, origin):
        """Rotate this ContextGeometry counterclockwise in the world XY plane.

        Args:
            angle: An angle in degrees.
            origin: A ladybug_geometry Point3D for the origin around which the
                object will be rotated.
        """
        origin_2d = Point2D(origin.x, origin.y)
        for geo in self._geometry:
            if isinstance(geo, _DisplayBase3D):
                geo.rotate_xy(angle, origin)
            elif isinstance(geo, _DisplayBase2D):
                geo.rotate(angle, origin_2d)

    def scale(self, factor, origin=None):
        """Scale this ContextGeometry by a factor from an origin point.

        Args:
            factor: A number representing how much the object should be scaled.
            origin: A ladybug_geometry Point3D representing the origin from which
                to scale. If None, it will be scaled from the World origin (0, 0, 0).
        """
        origin_2d = Point2D(origin.x, origin.y) if origin is not None else None
        for geo in self._geometry:
            if isinstance(geo, _DisplayBase3D):
                geo.scale(factor, origin)
            elif isinstance(geo, _DisplayBase2D):
                geo.scale(factor, origin_2d)

    def project_2d(self, plane):
        """"Project this AnalysisGeometry into a plane to get it in the plane's 2D system.

        This is useful as a pre-step before converting to SVG to get the geometry
        from a certain view.

        Args:
            plane: The Plane into which the AnalysisGeometry will be projected.
        """
        proj_geos = []
        for geo in self._geometry:
            p_geo = project_geometry_2d(plane, [geo.geometry])[0]
            if not isinstance(p_geo, geo.geometry.__class__):
                p_geo_class = DISPLAY_MAP[p_geo.__class__][0]
                new_geo = p_geo_class(p_geo)
                new_geo._transfer_attributes(geo)
            else:
                geo._geometry = p_geo
                new_geo = geo
            proj_geos.append(new_geo)
        self._geometry = tuple(proj_geos)

    def to_dict(self):
        """Get ContextGeometry as a dictionary."""
        base = {
            'type': 'ContextGeometry',
            'identifier': self.identifier,
            'geometry': [geo.to_dict() for geo in self.geometry],
            'hidden': self.hidden
        }
        if self._display_name is not None:
            base['display_name'] = self.display_name
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def to_svg(self, width=800, height=600):
        """Get this ContextGeometry as an editable SVG object.

        Casting the resulting SVG object to string will give the file contents of a SVG.

        Note that it is expected that the ContextGeometry has been scaled to
        fit in the specified width and height dimensions and it exists within
        the lower-right quadrant of the world coordinate system (Quadrant 4)
        in oder to be translated correctly into the XY coordinate system of
        the screen.

        Args:
            width: The screen width in pixels.
            height: The screen height in pixels.
        """
        elements = [geo.to_svg() for geo in self.geometry]
        canvas = svg.SVG(width=width, height=height)
        canvas.elements = elements
        return canvas

    @staticmethod
    def geometry_to_wireframe(geometry):
        """Convert a raw ladybug-geometry object into a wireframe ladybug-display object.

        Args:
            geometry: A raw ladybug-geometry object to be converted to a wireframe
                ladybug-display object.
        """
        conv_info = DISPLAY_MAP[geometry.__class__]
        new_class, wire_args = conv_info[0], list(conv_info[1:])
        wire_args.insert(0, geometry)
        return new_class(*wire_args)

    def _calculate_min_max(self):
        """Calculate maximum and minimum Point3D for this object."""
        lb_geos = []
        for d_geo in self.geometry:
            if isinstance(d_geo, DisplayText3D):
                lb_geos.append(d_geo.min)
                lb_geos.append(d_geo.max)
            else:
                lb_geos.append(d_geo.geometry)
        self._min_point, self._max_point = bounding_box(lb_geos)

    def __copy__(self):
        new_geo_objs = tuple(geo.duplicate() for geo in self.geometry)
        new_obj = ContextGeometry(self.identifier, new_geo_objs, self.hidden)
        new_obj._display_name = self._display_name
        new_obj._user_data = None if self.user_data is None else self.user_data.copy()
        return new_obj

    def __len__(self):
        """Return number of geometries on the object."""
        return len(self.geometry)

    def __getitem__(self, key):
        """Return one of the geometries."""
        return self.geometry[key]

    def __iter__(self):
        """Iterate through the geometries."""
        return iter(self.geometry)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """ContextGeometry representation."""
        return 'Context Geometry: {}'.format(self.display_name)
