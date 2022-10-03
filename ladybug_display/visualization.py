# coding=utf-8
from __future__ import division

from ladybug.legend import Legend, LegendParameters, LegendParametersCategorized
from ladybug.graphic import GraphicContainer
from ladybug.datatype.base import DataTypeBase

from ladybug_geometry.geometry2d import Vector2D, Point2D, Ray2D, LineSegment2D, \
    Polyline2D, Arc2D, Polygon2D, Mesh2D
from ladybug_geometry.geometry3d import Vector3D, Point3D, Ray3D, Plane, LineSegment3D, \
    Polyline3D, Arc3D, Face3D, Mesh3D, Polyface3D, Sphere, Cone, Cylinder
from .geometry2d import DisplayVector2D, DisplayPoint2D, \
    DisplayRay2D, DisplayLineSegment2D, DisplayPolyline2D, DisplayArc2D, \
    DisplayPolygon2D, DisplayMesh2D
from .geometry3d import DisplayVector3D, DisplayPoint3D, \
    DisplayRay3D, DisplayPlane, DisplayLineSegment3D, DisplayPolyline3D, DisplayArc3D, \
    DisplayFace3D, DisplayMesh3D, DisplayPolyface3D, DisplaySphere, DisplayCone, \
    DisplayCylinder
from ladybug_geometry.bounding import bounding_box
from ladybug_geometry.dictutil import geometry_dict_to_object

from .typing import int_in_range
from .dictutil import dict_to_object

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
    DisplayPolyface3D, DisplaySphere, DisplayCone, DisplayCylinder
)


class VisualizationSet(object):
    """A visualization set containing analysis and context geometry to be visualized.

    Args:
        analysis_geometry: A list of AnalysisGeometry objects for spatial data that is
            displayed in the visualization. Multiple AnalysisGeometry objects can
            be used to specify different related studies that were run to create
            the visualization (eg. a radiation study of windows next to a daylight
            study of interior floor plates). (Default: None).
        context_geometry: An optional list of ladybug-geometry or ladybug-display
            objects that gives context to the analysis geometry or other aspects
            of the visualization. Typically, these will display in wireframe around
            the geometry, though the properties of display geometry can be used to
            customize the visualization. (Default: None).

    Properties:
        * analysis_geometry
        * context_geometry
        * min_point
        * max_point
        * user_data
    """
    __slots__ = (
        '_analysis_geometry', '_context_geometry',
        '_min_point', '_max_point', '_user_data')

    WIREFRAME_MAP = {
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

    def __init__(self, analysis_geometry=None, context_geometry=None):
        """Initialize VisualizationSet."""
        self.analysis_geometry = analysis_geometry
        self.context_geometry = context_geometry
        self._min_point = None
        self._max_point = None
        self._user_data = None

    @classmethod
    def from_dict(cls, data):
        """Create an VisualizationSet from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": "VisualizationSet",
            "analysis_geometry": {},  # an AnalysisGeometry specification
            "context_geometry": []  # list of ladybug-display geometry objects
            }
        """
        # check the type key
        assert data['type'] == 'VisualizationSet', \
            'Expected VisualizationSet, Got {}.'.format(data['type'])
        # re-serialize the context and analysis geometry
        a_geo = tuple(AnalysisGeometry.from_dict(g) for g in data['analysis_geometry']) \
            if 'analysis_geometry' in data and \
            data['analysis_geometry'] is not None else None
        c_geos = tuple(dict_to_object(geo) for geo in data['context_geometry']) \
            if 'context_geometry' in data and data['context_geometry'] is not None \
            else None
        new_obj = cls(a_geo, c_geos)
        if 'user_data' in data and data['user_data'] is not None:
            new_obj.user_data = data['user_data']
        return new_obj

    @property
    def analysis_geometry(self):
        """Get or set a tuple of AnalysisGeometry for spatial data in the visualization.
        """
        return self._analysis_geometry

    @analysis_geometry.setter
    def analysis_geometry(self, value):
        if value is not None:
            assert isinstance(value, (list, tuple)), 'Expected list or tuple for' \
                ' VisualizationSet analysis_geometry. Got {}.'.format(type(value))
            if not isinstance(value, tuple):
                value = tuple(value)
            for geo in value:
                assert isinstance(geo, AnalysisGeometry), 'Expected AnalysisGeometry ' \
                    'for VisualizationSet analysis_geometry. Got {}.'.format(type(value))
        self._analysis_geometry = value

    @property
    def context_geometry(self):
        """Get or set a tuple of ladybug_display geometry objects for context.

        When setting this property, it is also acceptable to include raw
        ladybug_geometry objects in the list and they will automatically be
        converted into a wireframe representation as a ladybug-display object.
        """
        return self._context_geometry

    @context_geometry.setter
    def context_geometry(self, value):
        if value is not None:
            assert isinstance(value, (list, tuple)), 'Expected list or tuple for' \
                ' VisualizationSet context_geometry. Got {}.'.format(type(value))
            processed_value = []
            for geo in value:
                if isinstance(geo, DISPLAY_UNION):
                    processed_value.append(geo)
                elif isinstance(geo, GEOMETRY_UNION):
                    processed_value.append(self.geometry_to_wireframe(geo))
                else:
                    raise ValueError(
                        'Expected ladybug-geometry or ladybug-display object for '
                        'context_geometry. Got {}.'.format(type(geo)))
            value = tuple(processed_value)
        self._context_geometry = value

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

    def graphic_container(self, geo_index=0, data_index=None,
                          min_point=None, max_point=None):
        """Get a Ladybug GraphicContainer object, which can be used to draw legends.

        Note that this object must have analysis_geometry assigned to it in order
        to get a data collection.

        Args:
            geo_index: Integer for the index of the analysis_geometry for which a
                GraphicContainer will be returned. (Default: 0).
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
        # check to be sure that there is analysis geometry
        assert self.analysis_geometry is not None, 'VisualizationSet must have ' \
            'analysis_geometry in order to use graphic_container method.'
        # ensure that min and max points always make sense
        min_point = self.min_point if min_point is None else min_point
        max_point = self.max_point if max_point is None else max_point
        # return the Graphic Container for the correct data set
        data_index = self.analysis_geometry[geo_index].active_data \
            if data_index is None else data_index
        dat_set = self.analysis_geometry[geo_index].data_sets[data_index]
        return dat_set.graphic_container(min_point, max_point)

    def to_dict(self):
        """Get VisualizationSet as a dictionary."""
        base = {'type': 'VisualizationSet'}
        if self.analysis_geometry is not None:
            base['analysis_geometry'] = \
                [a_geo.to_dict() for a_geo in self.analysis_geometry]
        if self.context_geometry is not None:
            base['context_geometry'] = \
                [d_geo.to_dict() for d_geo in self.context_geometry]
        return base

    @staticmethod
    def geometry_to_wireframe(geometry):
        """Convert a raw ladybug-geometry object into a wireframe ladybug-display object.

        Args:
            geometry: A raw ladybug-geometry object to be converted to a wireframe
                ladybug-display object.
        """
        conv_info = VisualizationSet.WIREFRAME_MAP[geometry.__class__]
        new_class, wire_args = conv_info[0], list(conv_info[1:])
        wire_args.insert(0, geometry)
        return new_class(*wire_args)

    def _calculate_min_max(self):
        """Calculate maximum and minimum Point3D for this object."""
        all_geo = []
        if self.analysis_geometry is not None:
            for a_geo in self.analysis_geometry:
                for geo in a_geo.geometry:
                    all_geo.append(geo)
        if self.context_geometry is not None:
            for d_geo in self.context_geometry:
                all_geo.append(d_geo.geometry)
        if len(all_geo) != 0:
            self._min_point, self._max_point = bounding_box(all_geo)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __len__(self):
        """Return number of analysis geometries on the object."""
        return len(self.analysis_geometry)

    def __getitem__(self, key):
        """Return one of the analysis geometries."""
        return self.analysis_geometry[key]

    def __iter__(self):
        """Iterate through the data sets."""
        return iter(self.analysis_geometry)

    def __repr__(self):
        """VisualizationSet representation."""
        base_str = 'Visualization Set'
        if self.analysis_geometry is not None:
            base_str = base_str + ' ({} geometries)'.format(len(self.analysis_geometry))
        if self.context_geometry is not None:
            base_str = base_str + ' ({} contexts)'.format(len(self.context_geometry))
        return base_str


class AnalysisGeometry(object):
    """An object where multiple data streams correspond to the same geometry.

    Args:
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

    Properties:
        * geometry
        * data_sets
        * active_data
        * min_point
        * max_point
        * matching_method
        * user_data
    """
    __slots__ = (
        '_geometry', '_data_sets', '_active_data', '_min_point', '_max_point',
        '_possible_lengths', '_matching_method', '_user_data')

    def __init__(self, geometry, data_sets, active_data=0):
        """Initialize AnalysisGeometry."""
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
        self._min_point = None
        self._max_point = None
        self._user_data = None

    @classmethod
    def from_dict(cls, data):
        """Create an AnalysisGeometry from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": "AnalysisGeometry",
            "geometry": [],  # list of geometry objects
            "data_sets": [],  # list of data sets associated with the geometry
            "active_data": 0  # integer for the index of the active data set
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
        new_obj = cls(geos, dts, act_dt)
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
        self._active_data = int_in_range(value, 0, len(self._data_sets), 'active_data')

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

    def to_dict(self):
        """Get AnalysisGeometry as a dictionary."""
        base = {
            'type': 'AnalysisGeometry',
            'geometry': [geo.to_dict() for geo in self.geometry],
            'data_sets': [ds.to_dict() for ds in self.data_sets],
            'active_data': self.active_data
        }
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

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

    def _calculate_min_max(self):
        """Calculate maximum and minimum Point3D for this object."""
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

    def __len__(self):
        """Return number of data sets on the object."""
        return len(self.data_sets)

    def __getitem__(self, key):
        """Return one of the data sets."""
        return self.data_sets[key]

    def __iter__(self):
        """Iterate through the data sets."""
        return iter(self.data_sets._values)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """AnalysisGeometry representation."""
        return 'Analysis Geometry ({} data sets)'.format(len(self))


class VisualizationData(object):
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
        * data_type
        * min_point
        * max_point
        * user_data
    """
    __slots__ = ('_legend', '_legend_parameters', '_data_type', '_unit', '_user_data')

    def __init__(self, values, legend_parameters=None, data_type=None, unit=None):
        """Initialize VisualizationData."""
        # set up the legend using the values and legend parameters
        self._legend = Legend(values, legend_parameters)
        self._legend_parameters = legend_parameters
        self._user_data = None

        # set default legend parameters based on input data_type and unit
        self._data_type = data_type
        self._unit = unit
        if data_type is not None:
            assert isinstance(data_type, DataTypeBase), \
                'data_type should be a ladybug DataType. Got {}'.format(type(data_type))
            if self.legend_parameters.is_title_default:
                unit = unit if unit else data_type.units[0]
                data_type.is_unit_acceptable(unit)
                self.legend_parameters.title = unit if \
                    self.legend_parameters.vertical \
                    else '{} ({})'.format(data_type.name, unit)
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
    def data_type(self):
        """Get the data_type input to this object (if it exists)."""
        return self._data_type

    @property
    def unit(self):
        """Get the unit input to this object (if it exists)."""
        return self._unit

    @property
    def legend(self):
        """Get the legend assigned to this data set."""
        return self._legend

    @property
    def value_colors(self):
        """Get a List of colors associated with the assigned values."""
        return self._legend.value_colors

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

    def graphic_container(self, min_point, max_point):
        """Get a Ladybug GraphicContainer object, which can be used to a draw legend.

        Args:
            min_point: An optional Point3D to denote the minimum bounding box
                for the graphic container.
            max_point: An optional Point3D to denote the maximum bounding box
                for the graphic container.
        """
        return GraphicContainer(
            self.values, min_point, max_point, self._legend_parameters,
            self._data_type, self._unit)

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
