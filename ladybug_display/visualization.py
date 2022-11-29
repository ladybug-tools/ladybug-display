# coding=utf-8
from __future__ import division
import os
import sys
import json
import collections
try:  # check if we are in IronPython
    import cPickle as pickle
except ImportError:  # wea are in cPython
    import pickle

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
    DisplayCylinder, DisplayText3D
from ladybug_geometry.bounding import bounding_box
from ladybug_geometry.dictutil import geometry_dict_to_object

from ._base import DISPLAY_MODES
from .typing import int_in_range, valid_string
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
    DisplayPolyface3D, DisplaySphere, DisplayCone, DisplayCylinder, DisplayText3D
)


class _VisualizationBase(object):
    """A base class for visualization objects.

    Args:
        identifier: Text string for a unique object ID. Must be less than 100
            characters and not contain spaces or special characters.

    Properties:
        * identifier
        * display_name
        * full_id
        * user_data
    """
    __slots__ = ('_identifier', '_display_name', '_user_data')

    def __init__(self, identifier):
        """Initialize base object."""
        self.identifier = identifier
        self._display_name = None
        self._user_data = None

    @property
    def identifier(self):
        """Get or set a text string for the unique object identifier.

        This identifier remains constant as the object is mutated, copied, and
        serialized to different formats.
        """
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = valid_string(value, 'visualization object identifier')

    @property
    def display_name(self):
        """Get or set text for the object name without any character restrictions.

        This is typically used to set the layer of the object in the interface that
        renders the VisualizationSet. A :: in the display_name can be used to denote
        sub-layers following a convention of ParentLayer::SubLayer.

        If not set, the display_name will be equal to the object identifier.
        """
        if self._display_name is None:
            return self._identifier
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        if value is not None:
            try:
                value = str(value)
            except UnicodeEncodeError:  # Python 2 machine lacking the character set
                pass  # keep it as unicode
        self._display_name = value

    @property
    def full_id(self):
        """Get a string with both the object display_name and identifier.

        This is formatted as display_name[identifier].

        This is useful in error messages to give users an easy means of finding
        invalid objects within models. If there is no display_name assigned,
        only the identifier will be returned.
        """
        if self._display_name is None:
            return self._identifier
        else:
            return '{}[{}]'.format(self._display_name, self._identifier)

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
            assert isinstance(value, dict), 'Expected dictionary for visualization ' \
                'object user_data. Got {}.'.format(type(value))
        self._user_data = value

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def __copy__(self):
        new_obj = _VisualizationBase(self.identifier)
        new_obj._display_name = self._display_name
        new_obj._user_data = None if self.user_data is None else self.user_data.copy()
        return new_obj


class VisualizationSet(_VisualizationBase):
    """A visualization set containing analysis and context geometry to be visualized.

    Args:
        identifier: Text string for a unique object ID. Must be less than 100
            characters and not contain spaces or special characters.
        geometry: A list of AnalysisGeometry and ContextGeometry objects to display
            in the visualization. Each geometry object will typically be translated
            to its own layer within the interface that renders the VisualizationSet.

    Properties:
        * identifier
        * display_name
        * geometry
        * min_point
        * max_point
        * user_data
    """
    __slots__ = ('_geometry', '_min_point', '_max_point')

    def __init__(self, identifier, geometry):
        """Initialize VisualizationSet."""
        _VisualizationBase.__init__(self, identifier)  # process the identifier
        self.geometry = geometry
        self._min_point = None
        self._max_point = None

    @classmethod
    def from_dict(cls, data):
        """Create an VisualizationSet from a dictionary.

        Args:
            data: A python dictionary in the following format

        .. code-block:: python

            {
            "type": "VisualizationSet",
            "identifier": "",  # unique object identifier
            "geometry": []  # list of AnalysisGeometry and ContextGeometry objects
            }
        """
        # check the type key
        assert data['type'] == 'VisualizationSet', \
            'Expected VisualizationSet, Got {}.'.format(data['type'])
        # re-serialize the context and analysis geometry
        geos = []
        for geo_data in data['geometry']:
            if geo_data['type'] == 'AnalysisGeometry':
                geos.append(AnalysisGeometry.from_dict(geo_data))
            else:
                geos.append(ContextGeometry.from_dict(geo_data))
        new_obj = cls(data['identifier'], geos)
        if 'display_name' in data and data['display_name'] is not None:
            new_obj.display_name = data['display_name']
        if 'user_data' in data and data['user_data'] is not None:
            new_obj.user_data = data['user_data']
        return new_obj

    @classmethod
    def from_file(cls, vis_set_file):
        """Initialize a VisualizationSet from a JSON or pkl file, auto-sensing the type.

        Args:
            VisualizationSet: Path to either a VisualizationSet JSON or pkl file.
        """
        # sense the file type from the first character to avoid maxing memory with JSON
        # this is needed since queenbee overwrites all file extensions
        with open(vis_set_file) as inf:
            try:
                first_char = inf.read(1)
                is_json = True if first_char == '{' else False
            except UnicodeDecodeError:  # definitely a pkl file
                is_json = False
        # load the file using either JSON pathway or pkl
        if is_json:
            return cls.from_json(vis_set_file)
        return cls.from_pkl(vis_set_file)

    @classmethod
    def from_json(cls, json_file):
        """Initialize a VisualizationSet from a JSON file.

        Args:
            json_file: Path to VisualizationSet JSON file.
        """
        assert os.path.isfile(json_file), 'Failed to find %s' % json_file
        if (sys.version_info < (3, 0)):
            with open(json_file) as inf:
                data = json.load(inf)
        else:
            with open(json_file, encoding='utf-8') as inf:
                data = json.load(inf)
        return cls.from_dict(data)

    @classmethod
    def from_pkl(cls, pkl_file):
        """Initialize a Model from a pkl file.

        Args:
            pkl_file: Path to pkl file.
        """
        assert os.path.isfile(pkl_file), 'Failed to find %s' % pkl_file
        with open(pkl_file, 'rb') as inf:
            data = pickle.load(inf)
        return cls.from_dict(data)

    @classmethod
    def from_single_analysis_geo(
            cls, identifier, geometry, values, legend_parameters=None,
            data_type=None, unit=None):
        """Create an VisualizationSet from a raw geometry object and a list of values.

        Args:
            identifier: Text string for a unique object ID. Must be less than 100
                characters and not contain spaces or special characters.
            geometry: A list of ladybug-geometry objects that is aligned with the
                values. The length of this list should usually be equal to the total
                number of values in each data_set, indicating that each geometry gets
                a single color. Alternatively, if all of the geometry objects are
                meshes, the number of values in the data can be equal to the total
                number of faces across the meshes or the total number of vertices
                across the meshes.
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
        """
        viz_data = VisualizationData(values, legend_parameters, data_type, unit)
        a_geo = AnalysisGeometry('{}_Geometry'.format(identifier), geometry, [viz_data])
        return cls(identifier, (a_geo,))

    @property
    def geometry(self):
        """Get or set a tuple of AnalysisGeometry and ContextGeometry objects."""
        return self._geometry

    @geometry.setter
    def geometry(self, value):
        assert isinstance(value, (list, tuple)), 'Expected list or tuple for' \
            ' VisualizationSet geometry. Got {}.'.format(type(value))
        if not isinstance(value, tuple):
            value = tuple(value)
        for geo in value:
            self._check_geometry(geo)
        self._geometry = value

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

    def add_vis_set(self, vis_set):
        """Add all geometry objects of another VisualizationSet to this one.

        Args:
            vis_set: A VisualizationData object to be added to this AnalysisGeometry.
        """
        for geo in vis_set.geometry:
            self.add_geometry(geo)

    def add_geometry(self, geometry, insert_index=None):
        """Add a ContextGeometry or AnalysisGeometry object to this VisualizationSet.

        Args:
            geometry: A ContextGeometry or AnalysisGeometry object to be added
                to this VisualizationSet.
            insert_index: An integer for the index at which the data should be
                inserted. If None, the data will be appended to the end. (Default: None).
        """
        self._check_geometry(geometry)
        if insert_index is None:
            self._geometry = self._geometry + (geometry,)
        else:
            geos_list = list(self._geometry)
            geos_list.insert(insert_index, geometry)
            self._geometry = tuple(geos_list)
        self._min_point = None
        self._max_point = None

    def remove_geometry(self, geo_index):
        """Remove a geometry object from this VisualizationSet.

        Args:
            geo_index: An integer for the geometry index to be removed.
        """
        assert geo_index < len(self._geometry), 'geo_index ({}) must be less than ' \
            'the number of items in the data_sets ({}).'.format(
                geo_index, len(self._geometry))
        geos_list = list(self._geometry)
        geos_list.pop(geo_index)
        self._geometry = tuple(geos_list)
        self._min_point = None
        self._max_point = None

    def check_duplicate_identifiers(self, raise_exception=True, detailed=False):
        """Check that there are no duplicate geometry object identifiers in the set.

        Args:
            raise_exception: Boolean to note whether a ValueError should be raised
                if duplicate identifiers are found. (Default: True).
            detailed: Boolean for whether the returned object is a detailed list of
                dicts with error info or a string with a message. (Default: False).

        Returns:
            A string with the message or a list with a dictionary if detailed is True.
        """
        detailed = False if raise_exception else detailed
        obj_id_iter = (obj.identifier for obj in self.geometry)
        dup = [t for t, c in collections.Counter(obj_id_iter).items() if c > 1]
        if len(dup) != 0:
            if detailed:
                err_list = []
                for dup_id in dup:
                    msg = 'There is a duplicated geometry identifier: {}'.format(dup_id)
                    dup_dict = {
                        'type': 'ValidationError',
                        'element_type': 'Geometry',
                        'element_id': dup_id,
                        'element_name': dup_id,
                        'message': msg
                    }
                    err_list.append(dup_dict)
                return err_list
            msg = 'The following duplicated Geometry identifiers were found:\n{}'.format(
                '\n'.join(dup))
            if raise_exception:
                raise ValueError(msg)
            return msg
        return [] if detailed else ''

    def graphic_container(self, geo_index=0, data_index=None,
                          min_point=None, max_point=None):
        """Get a Ladybug GraphicContainer object, which can be used to draw legends.

        Args:
            geo_index: Integer for the index of the geometry for which a
                GraphicContainer will be returned. Note that this index must refer
                to an analysis geometry in order to produce a valid graphic
                container. (Default: 0).
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
        geo_obj = self.geometry[geo_index]
        assert isinstance(geo_obj, AnalysisGeometry), 'VisualizationSet geo_index ' \
            'must refer to an  AnalysisGeometry in order to use ' \
            'graphic_container method.'
        # ensure that min and max points always make sense
        min_point = self.min_point if min_point is None else min_point
        max_point = self.max_point if max_point is None else max_point
        # return the Graphic Container for the correct data set
        data_index = geo_obj.active_data if data_index is None else data_index
        dat_set = geo_obj.data_sets[data_index]
        return dat_set.graphic_container(min_point, max_point)

    def to_dict(self):
        """Get VisualizationSet as a dictionary."""
        base = {
            'type': 'VisualizationSet',
            'identifier': self.identifier,
            'geometry': [geo_obj.to_dict() for geo_obj in self.geometry]
        }
        if self._display_name is not None:
            base['display_name'] = self.display_name
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def to_json(self, name, folder, indent=None):
        """Write VisualizationSet to JSON.

        Args:
            name: A text string for the name of the JSON file.
            folder: A text string for the directory where the JSON will be written.
            indent: A positive integer to set the indentation used in the resulting
                JSON file. (Default: None).
        """
        # create dictionary from the VisualizationSet
        vs_dict = self.to_dict()
        # set up a name and folder for the JSON
        nl = name.lower()
        file_name = name if nl.endswith('.vsf') or nl.endswith('.json') \
            else '{}.vsf'.format(name)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        vs_file = os.path.join(folder, file_name)
        # write JSON
        with open(vs_file, 'w') as fp:
            json.dump(vs_dict, fp, indent=indent)
        return vs_file

    def to_pkl(self, name, folder):
        """Write VisualizationSet to compressed pickle file (pkl).

        Args:
            name: A text string for the name of the pickle file.
            folder: A text string for the directory where the pickle file will be
                written.
        """
        # create dictionary from the VisualizationSet
        vs_dict = self.to_dict()
        # set up a name and folder for the pkl
        nl = name.lower()
        file_name = name if nl.endswith('.vsf') or nl.endswith('.pkl') \
            else '{}.vsf'.format(name)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        vs_file = os.path.join(folder, file_name)
        # write the Model dictionary into a file
        with open(vs_file, 'wb') as fp:
            pickle.dump(vs_dict, fp)
        return vs_file

    def _check_geometry(self, geo):
        """Check that the geometry object is valid."""
        assert isinstance(geo, (AnalysisGeometry, ContextGeometry)), 'Expected ' \
            'AnalysisGeometry or ContextGeometry for VisualizationSet geometry. ' \
            'Got {}.'.format(type(geo))

    def _calculate_min_max(self):
        """Calculate maximum and minimum Point3D for this object."""
        all_geo = []
        for geo_obj in self.geometry:
            all_geo.append(geo_obj.min_point)
            all_geo.append(geo_obj.max_point)
        if len(all_geo) != 0:
            self._min_point, self._max_point = bounding_box(all_geo)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __copy__(self):
        new_geo_objs = tuple(obj.duplicate() for obj in self.geometry)
        new_obj = VisualizationSet(self.identifier, new_geo_objs)
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

    def __repr__(self):
        """VisualizationSet representation."""
        return 'Visualization Set: {}'.format(self.display_name)


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

    @staticmethod
    def geometry_to_wireframe(geometry):
        """Convert a raw ladybug-geometry object into a wireframe ladybug-display object.

        Args:
            geometry: A raw ladybug-geometry object to be converted to a wireframe
                ladybug-display object.
        """
        conv_info = ContextGeometry.WIREFRAME_MAP[geometry.__class__]
        new_class, wire_args = conv_info[0], list(conv_info[1:])
        wire_args.insert(0, geometry)
        return new_class(*wire_args)

    def _calculate_min_max(self):
        """Calculate maximum and minimum Point3D for this object."""
        lb_geos = [d_geo.geometry for d_geo in self.geometry]
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
        """AnalysisGeometry representation."""
        return 'Context Geometry: {}'.format(self.display_name)


class AnalysisGeometry(_VisualizationBase):
    """An object where multiple data streams correspond to the same geometry.

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
        * matching_method
        * user_data
    """
    __slots__ = (
        '_geometry', '_data_sets', '_active_data', '_display_mode', '_hidden',
        '_min_point', '_max_point', '_possible_lengths', '_matching_method')

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
        self._active_data = int_in_range(value, 0, len(self._data_sets), 'active_data')

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

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def __copy__(self):
        new_obj = VisualizationData(
            self.values, self._legend_parameters, self._data_type, self._unit)
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
