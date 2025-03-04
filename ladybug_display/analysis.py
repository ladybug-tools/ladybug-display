# coding=utf-8
"""Class for representing geometry colored with data according to legend parameters."""
from __future__ import division
import math
import uuid

from ladybug_geometry.geometry2d import Vector2D, Point2D, Ray2D, LineSegment2D, \
    Polyline2D, Arc2D, Polygon2D, Mesh2D
from ladybug_geometry.geometry3d import Vector3D, Point3D, Ray3D, Plane, LineSegment3D, \
    Polyline3D, Arc3D, Face3D, Mesh3D, Polyface3D, Sphere, Cone, Cylinder
from ladybug_geometry.bounding import bounding_box
from ladybug_geometry.dictutil import geometry_dict_to_object
from ladybug_geometry.projection import project_geometry_2d

from ladybug.legend import Legend, LegendParameters, LegendParametersCategorized
from ladybug.graphic import GraphicContainer
from ladybug.datatype.base import DataTypeBase

from .geometry2d import DisplayVector2D, DisplayPoint2D, \
    DisplayRay2D, DisplayLineSegment2D, DisplayPolyline2D, DisplayArc2D, \
    DisplayPolygon2D, DisplayMesh2D
from .geometry3d import DisplayVector3D, DisplayPoint3D, \
    DisplayRay3D, DisplayPlane, DisplayLineSegment3D, DisplayPolyline3D, DisplayArc3D, \
    DisplayFace3D, DisplayMesh3D, DisplayPolyface3D, DisplaySphere, DisplayCone, \
    DisplayCylinder, DisplayText3D

from ._base import DISPLAY_MODES, _VisualizationBase
from .typing import int_in_range
import ladybug_display.svg as svg

GEOMETRY_UNION = (
    Vector2D, Point2D, Ray2D, LineSegment2D, Polyline2D, Arc2D, Polygon2D,
    Mesh2D, Vector3D, Point3D, Ray3D, Plane, LineSegment3D,
    Polyline3D, Arc3D, Face3D, Mesh3D, Polyface3D, Sphere, Cone, Cylinder
)
DISPLAY_UNION = (
    DisplayVector2D, DisplayPoint2D, DisplayRay2D, DisplayLineSegment2D,
    DisplayPolyline2D, DisplayArc2D, DisplayPolygon2D, DisplayMesh2D,
    DisplayVector3D, DisplayPoint3D, DisplayRay3D, DisplayPlane, DisplayLineSegment3D,
    DisplayPolyline3D, DisplayArc3D, DisplayFace3D, DisplayMesh3D,
    DisplayPolyface3D, DisplaySphere, DisplayCone, DisplayCylinder, DisplayText3D
)
DISPLAY_MAP = {
    Vector2D: (DisplayVector2D, None),
    Point2D: (DisplayPoint2D, None),
    Ray2D: (DisplayRay2D, None),
    LineSegment2D: (DisplayLineSegment2D, None),
    Polyline2D: (DisplayPolyline2D, None),
    Arc2D: (DisplayArc2D, None),
    Polygon2D: (DisplayPolygon2D, None, 'Wireframe'),
    Mesh2D: (DisplayMesh2D, None, 'Wireframe'),
    Vector3D: (DisplayVector3D, None),
    Point3D: (DisplayPoint3D, None),
    Ray3D: (DisplayRay3D, None),
    Plane: (DisplayPlane, None),
    LineSegment3D: (DisplayLineSegment3D, None),
    Polyline3D: (DisplayPolyline3D, None),
    Arc3D: (DisplayArc3D, None),
    Face3D: (DisplayFace3D, None, 'Wireframe'),
    Mesh3D: (DisplayMesh3D, None, 'Wireframe'),
    Polyface3D: (DisplayPolyface3D, None, 'Wireframe'),
    Sphere: (DisplaySphere, None, 'Wireframe'),
    Cone: (DisplayCone, None, 'Wireframe'),
    Cylinder: (DisplayCylinder, None, 'Wireframe')
}


class AnalysisGeometry(_VisualizationBase):
    """An object where geometry is colored with data.

    Multiple data sets for different metrics can correspond to the same geometry.

    Args:
        identifier: Text string for a unique object ID. Must be less than 100
            characters and not contain spaces or special characters.
        geometry: A list of ladybug-geometry objects that is aligned with the values in
            the input data_sets. The length of this list should usually be equal to the
            total number of values in each data_set, indicating that each geometry
            gets a single color. Alternatively, if all of the geometry objects are
            meshes, the number of values in the data can be equal to the total number
            of faces across the meshes or the total number of vertices across the meshes.
        data_sets: A list of VisualizationData objects representing the data sets
            that are associated with the input geometry.
        active_data: An integer to denote which of the input data_sets should be
            displayed by default. (Default: 0).
        display_mode: Text to indicate the display mode (surface, wireframe, etc.).
            Choose from the following. (Default: Surface).

            * Surface
            * SurfaceWithEdges
            * Wireframe
            * Points

        hidden: A boolean to note whether the geometry is hidden by default and
            must be un-hidden to be visible in the 3D scene. (Default: False).

    Properties:
        * identifier
        * display_name
        * geometry
        * data_sets
        * active_data
        * display_mode
        * hidden
        * min_point
        * max_point
        * min_point_with_legend
        * max_point_with_legend
        * matching_method
        * user_data
    """
    __slots__ = (
        '_geometry', '_data_sets', '_active_data', '_display_mode', '_hidden',
        '_min_point', '_max_point', '_min_point_with_legend', '_max_point_with_legend',
        '_possible_lengths', '_matching_method')
    T_FORMABLE_2D = (Point2D, Ray2D, LineSegment2D, Polyline2D, Arc2D, Polygon2D, Mesh2D)

    def __init__(self, identifier, geometry, data_sets,
                 active_data=0, display_mode='Surface', hidden=False):
        """Initialize AnalysisGeometry."""
        _VisualizationBase.__init__(self, identifier)  # process the identifier
        if not isinstance(geometry, tuple):
            geometry = tuple(geometry)
        if not isinstance(data_sets, tuple):
            data_sets = tuple(data_sets)
        self._possible_lengths = self._possible_data_lengths(geometry)
        self._matching_method = None
        for dat in data_sets:
            self._check_data_set(dat)
        self._geometry = geometry
        self._data_sets = data_sets
        self.active_data = active_data
        self.display_mode = display_mode
        self.hidden = hidden
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

    @classmethod
    def from_dict(cls, data):
        """Create an AnalysisGeometry from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": "AnalysisGeometry",
            "identifier": "",  # unique object identifier
            "geometry": [],  # list of geometry objects
            "data_sets": [],  # list of data sets associated with the geometry
            "active_data": 0,  # integer for the index of the active data set
            "display_mode": "Surface",  # text for the display mode of the data
            "hidden": True  # boolean for whether the layer is hidden by default
            }
        """
        # check the type key
        assert data['type'] == 'AnalysisGeometry', \
            'Expected AnalysisGeometry, Got {}.'.format(data['type'])
        # re-serialize the geometry and data sets
        geos = tuple(geometry_dict_to_object(geo) for geo in data['geometry'])
        dts = tuple(VisualizationData.from_dict(dt) for dt in data['data_sets'])
        # re-serialize the data type and unit
        act_dt = data['active_data'] if 'active_data' in data else 0
        d_mode = data['display_mode'] if 'display_mode' in data else 'Surface'
        hidden = False if 'hidden' not in data else data['hidden']
        new_obj = cls(data['identifier'], geos, dts, act_dt, d_mode, hidden)
        if 'display_name' in data and data['display_name'] is not None:
            new_obj.display_name = data['display_name']
        if 'user_data' in data and data['user_data'] is not None:
            new_obj.user_data = data['user_data']
        return new_obj

    @property
    def geometry(self):
        """Get a tuple of geometry objects assigned to this AnalysisGeometry."""
        return self._geometry

    @property
    def data_sets(self):
        """Get a tuple of VisualizationData assigned to the AnalysisGeometry."""
        return self._data_sets

    @property
    def active_data(self):
        """Get or set an integer for the index of data set that is actively displaying.
        """
        return self._active_data

    @active_data.setter
    def active_data(self, value):
        self._active_data = int_in_range(
            value, 0, len(self._data_sets) - 1, 'active_data')

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

    @property
    def min_point_with_legend(self):
        """A Point3D for the minimum around all geometry, including 3D legends."""
        if self._min_point_with_legend is None:
            self._calculate_min_max(True)
        return self._min_point_with_legend

    @property
    def max_point_with_legend(self):
        """A Point3D for the maximum around all geometry, including 3D legends."""
        if self._max_point_with_legend is None:
            self._calculate_min_max(True)
        return self._max_point_with_legend

    @property
    def matching_method(self):
        """Get text for the method by which the data is matched to the geometry.

        This will be one of the following.

        * geometries - One value is assigned for each geometry
        * faces - One value is assigned per each face of the Mesh
        * vertices - One value is assigned per each vertex of the Mesh
        """
        return self._matching_method

    @property
    def user_data(self):
        """Get or set an optional dictionary for additional meta data for this object.

        This will be None until it has been set. All keys and values of this
        dictionary should be of a standard Python type to ensure correct
        serialization of the object to/from JSON (eg. str, float, int, list, dict)
        """
        return self._user_data

    @user_data.setter
    def user_data(self, value):
        if value is not None:
            assert isinstance(value, dict), 'Expected dictionary for ' \
                'object user_data. Got {}.'.format(type(value))
        self._user_data = value

    def add_data_set(self, data, insert_index=None):
        """Add a data set to this AnalysisGeometry object.

        Args:
            data: A VisualizationData object to be added to this AnalysisGeometry.
            insert_index: An integer for the index at which the data should be
                inserted. If None, the data will be appended to the end. (Default: None).
        """
        self._check_data_set(data)
        if insert_index is None:
            self._data_sets = self._data_sets + (data,)
        else:
            ds_list = list(self._data_sets)
            ds_list.insert(insert_index, data)
            self._data_sets = tuple(ds_list)

    def remove_data_set(self, data_index):
        """Remove a data set from this AnalysisGeometry object.

        Args:
            data_index: An integer for the data index to be removed.
        """
        assert data_index < len(self._data_sets), 'data_index ({}) must be less than ' \
            'the number of items in the data_sets ({}).'.format(
                data_index, len(self._data_sets))
        ds_list = list(self._data_sets)
        ds_list.pop(data_index)
        self._data_sets = tuple(ds_list)
        if self._active_data == len(self._data_sets):
            self._active_data = len(self._data_sets) - 1

    def graphic_container(self, data_index=None, min_point=None, max_point=None):
        """Get a Ladybug GraphicContainer object, which can be used to draw legends.

        Args:
            data_index: Integer for the index of the data set for which a
                GraphicContainer will be returned. If None, the active_data set
                will be used. (Default: None).
            min_point: An optional Point3D to denote the minimum bounding box
                for the graphic container. If None, this object's own min_point
                will be used, which corresponds to the bounding box around
                the geometry. (Default: None).
            max_point: An optional Point3D to denote the maximum bounding box
                for the graphic container. If None, this object's own max_point
                will be used, which corresponds to the bounding box around
                the geometry. (Default: None).
        """
        # ensure that min and max points always make sense
        min_point = self.min_point if min_point is None else min_point
        max_point = self.max_point if max_point is None else max_point
        # return the Graphic Container for the correct data set
        data_index = self.active_data if data_index is None else data_index
        return self.data_sets[data_index].graphic_container(min_point, max_point)

    def move(self, moving_vec):
        """Move this AnalysisGeometry along a vector.

        Args:
            moving_vec: A ladybug_geometry Vector3D with the direction and distance
                to move the AnalysisGeometry.
        """
        new_geo = []
        moving_vec_2d = Vector2D(moving_vec.x, moving_vec.y)
        for geo in self._geometry:
            try:  # most likely a 3D object
                new_geo.append(geo.move(moving_vec))
            except Exception:  # possibly a 2D object
                if isinstance(geo, self.T_FORMABLE_2D):
                    new_geo.append(geo.move(moving_vec_2d))
                else:  # object like a vector for which the transform is meaningless
                    new_geo.append(geo)
        for v_data in self.data_sets:
            l_par = v_data.legend.legend_parameters
            if not l_par.is_base_plane_default:
                l_par.base_plane = l_par.base_plane.move(moving_vec)
            else:
                l_par.properties_3d._base_plane = \
                    l_par.properties_3d._base_plane.move(moving_vec)
        self._geometry = tuple(new_geo)
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

    def rotate_xy(self, angle, origin):
        """Rotate this AnalysisGeometry counterclockwise in the world XY plane.

        Args:
            angle: An angle in degrees.
            origin: A ladybug_geometry Point3D for the origin around which the
                object will be rotated.
        """
        new_geo = []
        angle = math.radians(angle)
        origin_2d = Point2D(origin.x, origin.y)
        for geo in self._geometry:
            try:
                new_geo.append(geo.rotate_xy(angle, origin))
            except Exception:  # possibly a 2D object
                if isinstance(geo, self.T_FORMABLE_2D):
                    new_geo.append(geo.rotate(angle, origin_2d))
                else:  # object like a vector for which the transform is meaningless
                    new_geo.append(geo)
        for v_data in self.data_sets:
            l_par = v_data.legend.legend_parameters
            if not l_par.is_base_plane_default:
                l_par.base_plane = l_par.base_plane.rotate_xy(angle, origin)
            else:
                l_par.properties_3d._base_plane = \
                    l_par.properties_3d._base_plane.rotate_xy(angle, origin)
        self._geometry = tuple(new_geo)
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

    def scale(self, factor, origin=None):
        """Scale this AnalysisGeometry by a factor from an origin point.

        Args:
            factor: A number representing how much the object should be scaled.
            origin: A ladybug_geometry Point3D representing the origin from which
                to scale. If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_geo = []
        origin_2d = Point2D(origin.x, origin.y) if origin is not None else None
        for geo in self._geometry:
            try:
                new_geo.append(geo.scale(factor, origin))
            except Exception:  # possibly a 2D object
                if isinstance(geo, self.T_FORMABLE_2D):
                    new_geo.append(geo.scale(factor, origin_2d))
                else:  # object like a vector for which the transform is meaningless
                    new_geo.append(geo)
        for v_data in self.data_sets:
            l_par = v_data.legend.legend_parameters
            if not l_par.is_segment_height_default:
                l_par.segment_height = l_par.segment_height * factor
            elif l_par.properties_3d._segment_height != 1:
                l_par.properties_3d._segment_height = \
                    l_par.properties_3d._segment_height * factor
            if not l_par.is_segment_width_default:
                l_par.segment_width = l_par.segment_width * factor
            elif l_par.properties_3d._segment_height != 1:
                l_par.properties_3d._segment_width = \
                    l_par.properties_3d._segment_width * factor
            if not l_par.is_text_height_default:
                l_par.text_height = l_par.text_height * factor
            elif l_par.properties_3d._text_height is not None:
                l_par.properties_3d._text_height = \
                    l_par.properties_3d._text_height * factor
            l_par.properties_3d._base_plane = \
                l_par.properties_3d._base_plane.scale(factor, origin)
        self._geometry = tuple(new_geo)
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

    def project_2d(self, plane):
        """"Project this AnalysisGeometry into a plane to get it in the plane's 2D system.

        This is useful as a pre-step before converting to SVG to get the geometry
        from a certain view.

        Args:
            plane: The Plane into which the AnalysisGeometry will be projected.
        """
        self._geometry = tuple(project_geometry_2d(plane, self.geometry))
        for v_data in self.data_sets:
            l_par = v_data.legend.legend_parameters
            l_plane = l_par.properties_3d._base_plane
            origin = plane.xyz_to_xy(plane.project_point(l_plane.o))
            l_par.properties_3d._base_plane = \
                Plane(n=l_plane.n, o=Point3D(origin.x, origin.y), x=l_plane.x)
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

    def to_dict(self):
        """Get AnalysisGeometry as a dictionary."""
        base = {
            'type': 'AnalysisGeometry',
            'identifier': self.identifier,
            'geometry': [geo.to_dict() for geo in self.geometry],
            'data_sets': [ds.to_dict() for ds in self.data_sets],
            'active_data': self.active_data,
            'display_mode': self.display_mode,
            'hidden': self.hidden
        }
        if self._display_name is not None:
            base['display_name'] = self.display_name
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def to_svg(self, width=800, height=600,
               render_3d_legend=False, render_2d_legend=False, default_leg_pos=None):
        """Get this AnalysisGeometry as an editable SVG object.

        Casting the SVG object to string will give the file contents of a SVG.

        Note that it is expected that the AnalysisGeometry has been scaled to
        fit in the specified width and height dimensions and it exists within
        the lower-right quadrant of the world coordinate system (Quadrant 4)
        in oder to be translated correctly into the XY coordinate system of
        the screen.

        Args:
            width: The screen width in pixels.
            height: The screen height in pixels.
            render_3d_legend: Boolean to note whether a 3D version of the legend
                for any AnalysisGeometry should be included in the SVG (following
                the 3D dimensions specified in the LegendParameters).
            render_2d_legend: Boolean to note whether a 2D version of the legend
                for any AnalysisGeometry should be included in the SVG (following
                the 2D dimensions specified in the LegendParameters).
            default_leg_pos: An optional tuple of 3 numbers that can be used to
                customize the default legend positions such that they are not on top
                of one another when multiple AnalysisGeometries exist in a
                VisualizationSet. (Default: None).
        """
        elements = []  # list to hold all of the generated SVG elements
        # translate the geometry to SVG
        data_set = self.data_sets[self.active_data]
        l_par = data_set.legend_parameters
        colors = data_set.value_colors
        if self.matching_method in ('faces', 'vertices'):
            # translate the AnalysisGeometry using DisplayMesh2D
            prev_i = 0
            for mesh in self.geometry:
                m_len = len(mesh.faces) if self.matching_method == 'faces' \
                    else len(mesh.vertices)
                mesh.colors = colors[prev_i:prev_i + m_len]
                prev_i += m_len
                elements.append(DisplayMesh2D.mesh2d_to_svg(mesh, self.display_mode))
        else:  # translate the AnalysisGeometry using other display classes
            sample_geo = self.geometry[0]
            conv_info = DISPLAY_MAP[sample_geo.__class__]
            dis_class, conv_args = conv_info[0], list(conv_info[1:])
            if len(conv_args) == 2:
                conv_args[1] = self.display_mode
            for geo, col in zip(self.geometry, colors):
                dis_args = [geo] + conv_args
                dis_args[1] = col
                display_geo = dis_class(*dis_args)
                elements.append(display_geo.to_svg())
        # translate the legend to SVG if requested
        if default_leg_pos is None:
            default_leg_x3d, default_leg_x2d, default_leg_y2d = 0, 10, 50
        else:
            default_leg_x3d, default_leg_x2d, default_leg_y2d = default_leg_pos
        if render_3d_legend:
            # ensure multiple legends are not on top of each other
            if l_par.is_base_plane_default:
                m_vec = Vector3D(default_leg_x3d, 0, 0)
                l_par.base_plane = l_par.base_plane.move(m_vec)
                l_par.properties_3d._is_base_plane_default = True
                leg_width = l_par.segment_width + 6 * l_par.text_height \
                    if l_par.vertical else \
                    l_par.segment_width * (l_par.segment_count + 2)
                default_leg_x3d += leg_width
            elements.extend(self.legend_3d_to_svg(data_set.legend))
        if render_2d_legend:
            # ensure multiple legends are not on top of each other
            if l_par.vertical and l_par.is_origin_x_default:
                l_par.origin_x = '{}px'.format(default_leg_x2d)
                l_par.properties_2d._is_origin_x_default = True
                sw = data_set.legend.parse_dim_2d(
                    l_par.segment_width_2d, width)
                th = data_set.legend.parse_dim_2d(
                    l_par.text_height_2d, height)
                leg_width = sw + 6 * th
                default_leg_x2d += leg_width
            elif not l_par.vertical and l_par.is_origin_y_default:
                l_par.origin_y = '{}px'.format(default_leg_y2d)
                l_par.properties_2d._is_origin_y_default = True
                sh = data_set.legend.parse_dim_2d(
                    l_par.segment_height_2d, height)
                th = data_set.legend.parse_dim_2d(
                    l_par.text_height_2d, height)
                leg_height = sh + 4 * th
                default_leg_y2d += leg_height
            leg_svg = VisualizationData.legend_2d_to_svg(data_set.legend, width, height)
            elements.extend(leg_svg.elements)
        # add a description with the default legend dims if they were edited
        default_leg_pos = [default_leg_x3d, default_leg_x2d, default_leg_y2d]
        dim_desc = svg.Desc(content=str(default_leg_pos))
        elements.append(dim_desc)
        # combine everything into a final SVG object
        canvas = svg.SVG(width=width, height=height)
        canvas.elements = elements
        return canvas

    @staticmethod
    def legend_3d_to_svg(legend):
        """Translate a 3D Legend geometry into an SVG.

        Args:
            legend: A Ladybug Legend object to be converted to SVG.

        Returns:
            A list of SVG elements in the following order.

            -   legend_mesh -- A colored mesh for the legend.

            -   legend_title -- A text object for the legend title.

            -   legend_text -- Text objects for the rest of the legend text.
        """
        legend_mesh = DisplayMesh3D.mesh3d_to_svg(legend.segment_mesh, 'SurfaceWithEdges')
        legend_text = AnalysisGeometry.legend_text_objects(legend)
        svg_text = [txt.to_svg() for txt in legend_text]
        return [legend_mesh] + svg_text

    @staticmethod
    def legend_text_objects(legend):
        """Get DisplayText3D objects that correspond with a 3D legend."""
        _height = legend.legend_parameters.text_height
        _font = legend.legend_parameters.font
        legend_title = DisplayText3D(legend.title, legend.title_location,
                                     _height, font=_font)
        if not legend.legend_parameters.continuous_legend:
            legend_text = [
                DisplayText3D(txt, loc, _height, font=_font, horizontal_alignment='Left',
                              vertical_alignment='Bottom')
                for txt, loc in zip(legend.segment_text, legend.segment_text_location)
            ]
        elif legend.legend_parameters.vertical is True:
            legend_text = [
                DisplayText3D(txt, loc, _height, font=_font, horizontal_alignment='Left',
                              vertical_alignment='Middle')
                for txt, loc in zip(legend.segment_text, legend.segment_text_location)
            ]
        else:
            legend_text = [
                DisplayText3D(txt, loc, _height, font=_font,
                              horizontal_alignment='Center', vertical_alignment='Bottom')
                for txt, loc in zip(legend.segment_text, legend.segment_text_location)]
        return [legend_title] + legend_text

    def _check_data_set(self, data_set):
        """Check that a data set is compatible with the geometry."""
        assert isinstance(data_set, VisualizationData), 'Expected VisualizationData ' \
            'for AnalysisGeometry. Got {}.'.format(type(data_set))
        if self._matching_method is None:  # first data set to be matched
            pl = self._possible_lengths
            if pl[1] == 0 and pl[2] == 0:
                assert len(data_set) == pl[0], 'Expected number of data set values ' \
                    '({}) to align with the number of geometries ({}).'.format(
                        len(data_set.values), pl[0])
            else:
                assert len(data_set) in pl, 'Expected number of data set values ' \
                    '({}) to align with the number of geometries ({}), the number of ' \
                    'geometry faces ({}), or the number of geometry vertices ' \
                    '({}).'.format(len(data_set.values), pl[0], pl[1], pl[2])
            self._matching_method = self._matching_type(data_set)[0]
        else:
            assert self._matching_type(data_set)[0] == self._matching_method, \
                'Expected number of data set values ({}) to align with the number ' \
                'of {} ({}).'.format(len(data_set.values), self._matching_method,
                                     self._matching_type(data_set)[1])

    def _matching_type(self, dat_set):
        """Get text and number of values for the method by which data and geometry match.

        Args:
            dat_set: A data set which will have its length evaluated in relation to
                this object's geometry.
        """
        geo_len, face_len, vert_len = self._possible_lengths
        if len(dat_set) == geo_len:
            return 'geometries', geo_len
        if len(dat_set) == face_len:
            return 'faces', face_len
        if len(dat_set) == vert_len:
            return 'vertices', vert_len

    def _calculate_min_max(self, with_legend=False):
        """Calculate maximum and minimum Point3D for this object."""
        if with_legend:
            legend = self.data_sets[self.active_data].legend
            leg_geo = (legend.segment_mesh,) + tuple(self.legend_text_objects(legend))
            self._min_point_with_legend, self._max_point_with_legend = \
                bounding_box(self.geometry + leg_geo)
        else:
            self._min_point, self._max_point = bounding_box(self.geometry)

    @staticmethod
    def _possible_data_lengths(geometry):
        """Get the acceptable data lengths given the input geometry."""
        geo_count_0, geo_count_1, geo_count_2 = len(geometry), 0, 0
        for geo in geometry:
            if isinstance(geo, (Mesh2D, Mesh3D)):
                geo_count_1 += len(geo.faces)
                geo_count_2 += len(geo.vertices)
            else:
                assert isinstance(geo, GEOMETRY_UNION), 'Expected ladybug geometry ' \
                    'object for AnalysisGeometry. Got {}.'.format(type(geo))
        return (geo_count_0, geo_count_1, geo_count_2)

    def __copy__(self):
        new_d = tuple(data.duplicate() for data in self.data_sets)
        new_obj = AnalysisGeometry(
            self.identifier, self.geometry, new_d, self.active_data,
            self.display_mode, self.hidden)
        new_obj._display_name = self._display_name
        new_obj._user_data = None if self.user_data is None else self.user_data.copy()
        return new_obj

    def __len__(self):
        """Return number of data sets on the object."""
        return len(self.data_sets)

    def __getitem__(self, key):
        """Return one of the data sets."""
        return self.data_sets[key]

    def __iter__(self):
        """Iterate through the data sets."""
        return iter(self.data_sets)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """AnalysisGeometry representation."""
        return 'Analysis Geometry: {}'.format(self.display_name)


class VisualizationMetaData(object):
    """Represents the metadata for visualization with legend parameters and data type.

    Args:
        legend_parameters: An Optional LegendParameters object to override default
            parameters of the legend. None indicates that default legend parameters
            will be used. (Default: None).
        data_type: Optional DataType from the ladybug datatype subpackage (ie.
            Temperature()) , which will be used to assign default legend properties.
            If None, the legend associated with this object will contain no units
            unless a unit below is specified. (Default: None).
        unit: Optional text string for the units of the values. (ie. "C"). If None
            or empty, the default units of the data_type will be used. If no data
            type is specified in this case, this will simply be an empty
            string. (Default: None).

    Properties:
        * legend_parameters
        * data_type
        * unit
        * user_data
    """
    __slots__ = ('_legend_parameters', '_data_type', '_unit', '_user_data')

    def __init__(self, legend_parameters=None, data_type=None, unit=None):
        """Initialize VisualizationMetaData."""
        self._legend_parameters = legend_parameters
        self._data_type = data_type
        self._unit = unit
        self._user_data = None

    @classmethod
    def from_dict(cls, data):
        """Create VisualizationMetaData from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": "VisualizationMetaData",
            "legend_parameters": {},  # optional LegendParameter specification
            "data_type": {},  # optional DataType object
            "unit": "C"  # optional text for the units
            }
        """
        # check the type key
        assert data['type'] == 'VisualizationMetaData', \
            'Expected VisualizationMetaData, Got {}.'.format(data['type'])
        # re-serialize the legend parameters
        legend_parameters = None
        if 'legend_parameters' in data and data['legend_parameters'] is not None:
            if data['legend_parameters']['type'] == 'LegendParametersCategorized':
                legend_parameters = LegendParametersCategorized.from_dict(
                    data['legend_parameters'])
            else:
                legend_parameters = LegendParameters.from_dict(data['legend_parameters'])
        # re-serialize the data type and unit
        data_type = None
        if 'data_type' in data and data['data_type'] is not None:
            data_type = DataTypeBase.from_dict(data['data_type'])
        unit = data['unit'] if 'unit' in data else None
        new_obj = cls(legend_parameters, data_type, unit)
        if 'user_data' in data and data['user_data'] is not None:
            new_obj.user_data = data['user_data']
        return new_obj

    @property
    def legend_parameters(self):
        """Get the legend parameters assigned to this data set."""
        return self._legend_parameters

    @property
    def data_type(self):
        """Get the data_type input to this object (if it exists)."""
        return self._data_type

    @property
    def unit(self):
        """Get the unit input to this object (if it exists)."""
        return self._unit

    @property
    def user_data(self):
        """Get or set an optional dictionary for additional meta data for this object.

        This will be None until it has been set. All keys and values of this
        dictionary should be of a standard Python type to ensure correct
        serialization of the object to/from JSON (eg. str, float, int, list, dict)
        """
        return self._user_data

    @user_data.setter
    def user_data(self, value):
        if value is not None:
            assert isinstance(value, dict), 'Expected dictionary for ' \
                'object user_data. Got {}.'.format(type(value))
        self._user_data = value

    def to_dict(self):
        """Get visualization data as a dictionary."""
        base = {
            'type': 'VisualizationMetaData'
        }
        if self._legend_parameters is not None:
            base['legend_parameters'] = self._legend_parameters.to_dict()
        if self.data_type is not None:
            base['data_type'] = self.data_type.to_dict()
        if self.unit:
            base['unit'] = self.unit
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """VisualizationMetaData representation."""
        return 'Visualization MetaData'


class VisualizationData(VisualizationMetaData):
    """Represents a data set for visualization with legend parameters and data type.

    Args:
        values: A list of numerical values that will be used to generate the
            visualization colors.
        legend_parameters: An Optional LegendParameters object to override default
            parameters of the legend. None indicates that default legend parameters
            will be used. (Default: None).
        data_type: Optional DataType from the ladybug datatype subpackage (ie.
            Temperature()) , which will be used to assign default legend properties.
            If None, the legend associated with this object will contain no units
            unless a unit below is specified. (Default: None).
        unit: Optional text string for the units of the values. (ie. "C"). If None
            or empty, the default units of the data_type will be used. If no data
            type is specified in this case, this will simply be an empty
            string. (Default: None).

    Properties:
        * values
        * legend_parameters
        * legend
        * data_type
        * unit
        * value_colors
        * user_data
    """
    __slots__ = ('_legend',)

    def __init__(self, values, legend_parameters=None, data_type=None, unit=None):
        """Initialize VisualizationData."""
        # set up the legend using the values and legend parameters
        VisualizationMetaData.__init__(self, legend_parameters, data_type, unit)

        # assign defaults to the legend parameter using the values and the data type
        self._legend = Legend(values, legend_parameters)
        if data_type is not None:
            assert isinstance(data_type, DataTypeBase), \
                'data_type should be a ladybug DataType. Got {}'.format(type(data_type))
            if self.legend_parameters.is_title_default:
                self._unit = unit if unit else data_type.units[0]
                data_type.is_unit_acceptable(self._unit)
                self.legend_parameters.title = self._unit if \
                    self.legend_parameters.vertical \
                    else '{} ({})'.format(data_type.name, self._unit)
            if data_type.unit_descr is not None and \
                    self.legend_parameters.ordinal_dictionary is None and not \
                    isinstance(self.legend_parameters, LegendParametersCategorized):
                self.legend_parameters.ordinal_dictionary = data_type.unit_descr
                sorted_keys = sorted(data_type.unit_descr.keys())
                if self.legend.is_min_default:
                    self.legend_parameters._min = sorted_keys[0]
                if self.legend.is_max_default:
                    self.legend_parameters._max = sorted_keys[-1]
                assert self.legend_parameters._min <= self.legend_parameters._max, \
                    'Legend min is greater than legend max. {} > {}.'.format(
                        self.legend_parameters._min, self.legend_parameters._max)
                if self.legend_parameters.is_segment_count_default:
                    try:  # try to set the number of segments to align with ordinal text
                        min_i = sorted_keys.index(self.legend_parameters.min)
                        max_i = sorted_keys.index(self.legend_parameters.max)
                        self.legend_parameters.segment_count = \
                            len(sorted_keys[min_i:max_i + 1])
                    except IndexError:
                        pass
        elif unit and self.legend_parameters.is_title_default:
            assert isinstance(unit, str), \
                'Expected string for unit. Got {}.'.format(type(unit))
            self.legend_parameters.title = unit

    @classmethod
    def from_dict(cls, data):
        """Create VisualizationData from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": "VisualizationData",
            "values": [0, 10],
            "legend_parameters": {},  # optional LegendParameter specification
            "data_type": {},  # optional DataType object
            "unit": "C"  # optional text for the units
            }
        """
        # check the type key
        assert data['type'] == 'VisualizationData', \
            'Expected VisualizationData, Got {}.'.format(data['type'])
        # re-serialize the legend parameters
        legend_parameters = None
        if 'legend_parameters' in data and data['legend_parameters'] is not None:
            if data['legend_parameters']['type'] == 'LegendParametersCategorized':
                legend_parameters = LegendParametersCategorized.from_dict(
                    data['legend_parameters'])
            else:
                legend_parameters = LegendParameters.from_dict(data['legend_parameters'])
        # re-serialize the data type and unit
        data_type = None
        if 'data_type' in data and data['data_type'] is not None:
            data_type = DataTypeBase.from_dict(data['data_type'])
        unit = data['unit'] if 'unit' in data else None
        new_obj = cls(data['values'], legend_parameters, data_type, unit)
        if 'user_data' in data and data['user_data'] is not None:
            new_obj.user_data = data['user_data']
        return new_obj

    @property
    def values(self):
        """Get the values assigned to the data set."""
        return self._legend.values

    @property
    def legend_parameters(self):
        """Get the legend parameters assigned to this data set."""
        return self._legend._legend_par

    @property
    def legend(self):
        """Get the legend assigned to this data set."""
        return self._legend

    @property
    def value_colors(self):
        """Get a List of colors associated with the assigned values."""
        return self._legend.value_colors

    def graphic_container(self, min_point, max_point):
        """Get a Ladybug GraphicContainer object, which can be used to a draw legend.

        Args:
            min_point: An optional Point3D to denote the minimum bounding box
                for the graphic container.
            max_point: An optional Point3D to denote the maximum bounding box
                for the graphic container.
        """
        return GraphicContainer(
            self.values, min_point, max_point, self._legend._legend_par,
            self._data_type, self._unit)

    def convert_to_unit(self, unit, convert_min_max=False):
        """Convert the VisualizationData to the input unit.

        Note that the VisualizationData must have a data_type and unit assigned
        to it in order for this method to run successfully and not raise an exception.

        Args:
            unit: Text indicating the units to which the value should be
                converted (eg. 'kWh/m2'). See ladybug.datatype.UNITS for
                a dictionary containing all acceptable units for each data type.
            convert_min_max: Boolean to note whether the min and max of the
                LegendParameters should also have their units converted, which
                may or may not be desirable depending on when this min and max
                was originally set. (Default: False).
        """
        assert self._data_type is not None and self._unit is not None, \
            'VisualizationData must have a data_type and unit assigned in ' \
            'order to perform unit conversions.'
        new_values = self._data_type.to_unit(self.values, unit, self._unit)
        self._change_units(new_values, unit, convert_min_max)

    def convert_to_ip(self, convert_min_max=False):
        """Convert the VisualizationData to IP units.

        Note that the VisualizationData must have a data_type and unit assigned
        to it in order for this method to run successfully and not raise an exception.

        Args:
            convert_min_max: Boolean to note whether the min and max of the
                LegendParameters should also have their units converted, which
                may or may not be desirable depending on when this min and max
                was originally set. (Default: False).
        """
        assert self._data_type is not None and self._unit is not None, \
            'VisualizationData must have a data_type and unit assigned in ' \
            'order to perform unit conversions.'
        new_values, new_unit = self._data_type.to_ip(self.values, self._unit)
        self._change_units(new_values, new_unit, convert_min_max)

    def convert_to_si(self, convert_min_max=False):
        """Convert the VisualizationData to SI units.

        Note that the VisualizationData must have a data_type and unit assigned
        to it in order for this method to run successfully and not raise an exception.

        Args:
            convert_min_max: Boolean to note whether the min and max of the
                LegendParameters should also have their units converted, which
                may or may not be desirable depending on when this min and max
                was originally set. (Default: False).
        """
        assert self._data_type is not None and self._unit is not None, \
            'VisualizationData must have a data_type and unit assigned in ' \
            'order to perform unit conversions.'
        new_values, new_unit = self._data_type.to_si(self.values, self._unit)
        self._change_units(new_values, new_unit, convert_min_max)

    def _change_units(self, new_values, new_unit, convert_min_max=False):
        if self._legend.is_min_default:
            self._legend_parameters.min = None
        elif convert_min_max:
            self._legend_parameters.min = \
                self._data_type.to_unit(
                    [self._legend_parameters.min], new_unit, self._unit)[0]
        if self._legend.is_max_default:
            self._legend_parameters.max = None
        elif convert_min_max:
            self._legend_parameters.max = \
                self._data_type.to_unit(
                    [self._legend_parameters.max], new_unit, self._unit)[0]
        self._unit = new_unit
        self._legend = Legend(new_values, self._legend_parameters)
        self.legend_parameters.title = new_unit if self.legend_parameters.vertical \
            else '{} ({})'.format(self._data_type.name, new_unit)

    def to_dict(self):
        """Get visualization data as a dictionary."""
        base = {
            'type': 'VisualizationData',
            'values': self.values
        }
        if self._legend_parameters is not None:
            base['legend_parameters'] = self._legend_parameters.to_dict()
        if self.data_type is not None:
            base['data_type'] = self.data_type.to_dict()
        if self.unit:
            base['unit'] = self.unit
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def to_svg(self, width=800, height=600):
        """Get the legend of the visualization data as an editable SVG object.

        Casting this SVG object to string will give the file contents of a SVG.
        The legend will be rendered using the properties2d of the LegendParameters,
        which is suitable for exporting the legend as a standalone graphic.

        Args:
            width: The screen width in pixels, which is needed to interpret
                dimensions specified in the percent of the screen. (Default: 800).
            height: The screen height in pixels, which is needed to interpret
                dimensions specified in the percent of the screen. (Default: 600).
        """
        # get the legend properties of this object
        return self.legend_2d_to_svg(self.legend, width, height)

    @staticmethod
    def legend_2d_to_svg(legend, width=800, height=600):
        """Translate a 2D Legend geometry into an SVG.

        Args:
            legend: A Ladybug Legend object to be converted to SVG.
            width: The screen width in pixels, which is needed to interpret
                dimensions specified in the percent of the screen. (Default: 800).
            height: The screen height in pixels, which is needed to interpret
                dimensions specified in the percent of the screen. (Default: 600).

        Returns:
            A list of SVG elements in the following order.

            -   legend_mesh -- A colored mesh for the legend.

            -   legend_title -- A text object for the legend title.

            -   legend_text -- Text objects for the rest of the legend text.
        """
        l_par = legend.legend_parameters
        or_x, or_y, sh, sw, th = legend._pixel_dims_2d(width, height)
        elements = []  # list to hold all of the elements of the legend

        # draw a border around the whole legend bar
        lh = sh * l_par.segment_count if l_par.vertical else sh
        lw = sw if l_par.vertical else sw * l_par.segment_count
        if l_par.continuous_legend:
            if l_par.vertical:
                lh = lh - sh
            else:
                lw = lw - sw
        bound_rect = svg.Rect(x=or_x, y=or_y, height=lh, width=lw, fill='none')
        bound_rect.stroke = 'black'
        bound_rect.stroke_width = 1

        # translate the colors of the legend to SVG shapes
        colors = list(reversed(legend.segment_colors)) \
            if l_par.vertical else legend.segment_colors
        if not l_par.continuous_legend:  # output segments as colored rectangles
            for i, col in enumerate(colors):
                rect = svg.Rect(x=or_x, y=or_y, height=sh, width=sw, fill=col.to_hex())
                move = svg.Translate(x=0, y=sh * i) if l_par.vertical else \
                    svg.Translate(x=sw * i, y=0)
                rect.transform = [move]
                elements.append(rect)
        else:
            gradient = svg.LinearGradient()
            gradient.gradientUnits = 'objectBoundingBox'
            gradient.id = 'legend_gradient_{}'.format(str(uuid.uuid4())[:8])
            if l_par.vertical:
                gradient.gradientTransform = [svg.Rotate(90)]
            stop_colors = []
            for i, col in enumerate(colors):
                stop = svg.Stop(stop_color=col.to_hex())
                stop.offset = svg.Length(int((i / len(colors)) * 100), '%')
                stop_colors.append(stop)
            gradient.elements = stop_colors
            elements.append(gradient)
            bound_rect.fill = "url('#{}')".format(gradient.id)
        elements.append(bound_rect)

        # translate the legend title
        t_pt = legend.title_location_2d(width, height)
        svg_txt = svg.Text(x=t_pt.x, y=t_pt.y)
        svg_txt.text = legend.title
        svg_txt.font_size = th
        svg_txt.font_family = l_par.font
        svg_txt.text_anchor = 'start'
        svg_txt.dominant_baseline = 'middle'
        elements.append(svg_txt)

        # translate the legend text for the values in the legend
        txt_pts = legend.segment_text_location_2d(width, height)
        for txt, loc in zip(legend.segment_text, txt_pts):
            svg_txt = svg.Text(x=loc.x, y=loc.y)
            svg_txt.text = txt
            svg_txt.font_size = th
            svg_txt.font_family = l_par.font
            svg_txt.dominant_baseline = 'hanging'
            if not l_par.vertical:
                svg_txt.text_anchor = 'middle'
            elements.append(svg_txt)

        # combine everything into a final SVG object
        canvas = svg.SVG(width=width, height=height)
        canvas.elements = elements
        return canvas

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def __copy__(self):
        new_obj = VisualizationData(
            self.values, self.legend_parameters, self._data_type, self._unit)
        new_obj._user_data = None if self.user_data is None else self.user_data.copy()
        return new_obj

    def __len__(self):
        """Return length of values on the object."""
        return len(self._legend._values)

    def __getitem__(self, key):
        """Return one of the values."""
        return self._legend._values[key]

    def __iter__(self):
        """Iterate through the values."""
        return iter(self._legend._values)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """VisualizationData representation."""
        return 'Visualization Data ({} values)'.format(len(self))
