# coding=utf-8
from __future__ import division
import os
import io
import json
import collections
try:  # check if we are in IronPython
    import cPickle as pickle
except ImportError:  # wea are in cPython
    import pickle

from ladybug_geometry.geometry3d import Vector3D, Point3D, Plane
from ladybug_geometry.bounding import bounding_box

from ._base import _VisualizationBase
from .analysis import GEOMETRY_UNION, AnalysisGeometry, \
    VisualizationData, VisualizationMetaData
from .context import DISPLAY_UNION, ContextGeometry
import ladybug_display.svg as svg


class VisualizationSet(_VisualizationBase):
    """A visualization set containing analysis and context geometry to be visualized.

    Args:
        identifier: Text string for a unique object ID. Must be less than 100
            characters and not contain spaces or special characters.
        geometry: A list of AnalysisGeometry and ContextGeometry objects to display
            in the visualization. Each geometry object will typically be translated
            to its own layer within the interface that renders the VisualizationSet.
        units: Text for the units system in which the visualization geometry
            exists. If None, the geometry will always be assumed to be in the current
            units system of the display interface. (Default: None). Choose from
            the following:

            * Meters
            * Millimeters
            * Feet
            * Inches
            * Centimeters

    Properties:
        * identifier
        * display_name
        * geometry
        * min_point
        * max_point
        * min_point_with_legend
        * max_point_with_legend
        * units
        * user_data
    """
    __slots__ = ('_geometry', '_min_point', '_max_point', '_min_point_with_legend',
                 '_max_point_with_legend', '_units')

    UNITS = ('Meters', 'Millimeters', 'Feet', 'Inches', 'Centimeters')
    GEOMETRY_UNION = GEOMETRY_UNION
    DISPLAY_UNION = DISPLAY_UNION
    ANALYSIS_CLASSES = (AnalysisGeometry, VisualizationData, VisualizationMetaData)
    VIEW_MAP = {
        'Top': Plane(n=Vector3D(0, 0, 1)),
        'Left': Plane(n=Vector3D(1, 0, 0)),
        'Right': Plane(n=Vector3D(-1, 0, 0)),
        'Front': Plane(n=Vector3D(0, 1, 0)),
        'Back': Plane(n=Vector3D(0, -1, 0)),
        'NE': Plane(n=Vector3D(1, 1, 1)),
        'NW': Plane(n=Vector3D(-1, 1, 1)),
        'SE': Plane(n=Vector3D(1, -1, 1)),
        'SW': Plane(n=Vector3D(-1, -1, 1))
    }

    def __init__(self, identifier, geometry, units=None):
        """Initialize VisualizationSet."""
        _VisualizationBase.__init__(self, identifier)  # process the identifier
        self.geometry = geometry
        self.units = units
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

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
        if 'units' in data and data['units'] is not None:
            new_obj.units = data['units']
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
        with io.open(vis_set_file, encoding='utf-8') as inf:
            try:
                first_char = inf.read(1)
                second_char = inf.read(1)
                is_json = True if first_char == '{' or second_char == '{' else False
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
        with io.open(json_file, encoding='utf-8') as inf:
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
    def units(self):
        """Get or set Text for the units system in which the geometry exists."""
        return self._units

    @units.setter
    def units(self, value):
        if value is not None:
            value = value.title()
            assert value in self.UNITS, '{} is not supported as a units system. ' \
                'Choose from the following: {}'.format(value, self.UNITS)
        self._units = value

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
        self._min_point_with_legend = None
        self._max_point_with_legend = None

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
        self._min_point_with_legend = None
        self._max_point_with_legend = None

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

    def move(self, moving_vec):
        """Move this VisualizationSet along a vector.

        Args:
            moving_vec: A ladybug_geometry Vector3D with the direction and distance
                to move the VisualizationSet.
        """
        for geo in self.geometry:
            geo.move(moving_vec)
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

    def rotate_xy(self, angle, origin):
        """Rotate this VisualizationSet counterclockwise in the world XY plane.

        Args:
            angle: An angle in degrees.
            origin: A ladybug_geometry Point3D for the origin around which the
                object will be rotated.
        """
        for geo in self.geometry:
            geo.rotate_xy(angle, origin)
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

    def scale(self, factor, origin=None):
        """Scale this VisualizationSet by a factor from an origin point.

        Args:
            factor: A number representing how much the object should be scaled.
            origin: A ladybug_geometry Point3D representing the origin from which
                to scale. If None, it will be scaled from the World origin (0, 0, 0).
        """
        for geo in self._geometry:
            geo.scale(factor, origin)
        self._min_point = None
        self._max_point = None
        self._min_point_with_legend = None
        self._max_point_with_legend = None

    def convert_to_units(self, units):
        """Convert all of the geometry in this VisualizationSet to certain units.

        This involves scaling the geometry and changing the VisualizationSet's
        units property.

        Args:
            units: Text for the units to which the VisualizationSet geometry should be
                converted. Choose from the following:

                * Meters
                * Millimeters
                * Feet
                * Inches
                * Centimeters
        """
        if self.units != units:
            scale_fac1 = self._conversion_factor_to_meters(self.units)
            scale_fac2 = self._conversion_factor_to_meters(units)
            scale_fac = scale_fac1 / scale_fac2
            self.scale(scale_fac)
            self.units = units

    def to_dict(self):
        """Get VisualizationSet as a dictionary."""
        base = {
            'type': 'VisualizationSet',
            'identifier': self.identifier,
            'geometry': [geo_obj.to_dict() for geo_obj in self.geometry]
        }
        if self._units is not None:
            base['units'] = self.units
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

    def to_svg(self, width=800, height=600, margin=None,
               render_3d_legend=False, render_2d_legend=False, view='Top'):
        """Get this VisualizationSet as an editable SVG object.

        Casting the SVG object to string will give the file contents of a SVG.

        All contents of the VisualizationSet will automatically scaled to fit
        within the specified pixel width and height of the SVG

        Args:
            width: The screen width in pixels.
            height: The screen height in pixels.
            margin: An optional number to set the size of the margins around the
                base graphic in the final image. If None, this is automatically
                set to be 2% of whatever the constraining dimension is (either
                width or height). (Default: None).
            render_3d_legend: Boolean to note whether a 3D version of the legend
                for any AnalysisGeometry should be included in the SVG (following
                the 3D dimensions specified in the LegendParameters).
            render_2d_legend: Boolean to note whether a 2D version of the legend
                for any AnalysisGeometry should be included in the SVG (following
                the 2D dimensions specified in the LegendParameters).
            view: An optional text string for the view for which the SVG will be
                generated. This can also be a ladybug-geometry Plane object for
                the plane in which an axonometric view will be generated. Choose
                from the common options below when using a text string.

                * Top
                * Left
                * Right:
                * Front
                * Back
                * NE
                * NW
                * SE
                * SW
        """
        # compute the scene width and height
        if margin is None:
            scene_width, scene_height = width * 0.96, height * 0.96
        else:
            scene_width, scene_height = width - (2 * margin), height - (2 * margin)
        default_leg_pos = [0, 10, 50]
        # project the geometry into a plane if requested
        vis_geometry = [geo.duplicate() for geo in self.geometry if not geo.hidden]
        if view != 'Top' and view != Plane():
            if isinstance(view, str):
                try:
                    view = self.VIEW_MAP[view]
                except KeyError:
                    msg = 'Unrecognized view type "{}". Choose from: {}'.format(
                        view, ' '.join(list(self.VIEW_MAP.keys())))
                    raise ValueError(msg)
            else:
                assert isinstance(view, Plane), 'Input view must be a string or ' \
                    'Plane. Got {}.'.format(type(view))
            for geo in vis_geometry:
                geo.project_2d(view)
                geo.rotate_xy(180, Point3D())
        # compute the bounding box dimensions around all of the VisualizationSet geometry
        if render_3d_legend:
            min_pt, max_pt = self.min_point_with_legend, self.max_point_with_legend
        else:
            min_pt, max_pt = self.min_point, self.max_point
        move_vec = Vector3D(-min_pt.x, -max_pt.y)
        x_dim, y_dim = max_pt.x - min_pt.x, max_pt.y - min_pt.y

        x_factor, y_factor = scene_width / x_dim, scene_height / y_dim
        scale_fac = min(x_factor, y_factor)
        if scale_fac == x_factor:  # center the geometry in the Y dimension
            scene_height = y_dim * scale_fac
        else:
            scene_width = x_dim * scale_fac
        center_vec = Vector3D((width - scene_width) / 2,  -(height - scene_height) / 2)
        # transform all of the visualization set geometry to be in the lower quadrant
        svg_elements = []
        for geo in reversed(vis_geometry):
            geo.move(move_vec)
            geo.scale(scale_fac)
            geo.move(center_vec)
            if isinstance(geo, AnalysisGeometry):
                svg_data = geo.to_svg(render_3d_legend=render_3d_legend,
                                      render_2d_legend=render_2d_legend,
                                      default_leg_pos=default_leg_pos)
                default_leg_pos = list(svg_data.elements[-1].content)
            else:
                svg_data = geo.to_svg()
            svg_elements.extend(svg_data.elements)
        # combine everything into a final SVG object
        canvas = svg.SVG(width=width, height=height)
        canvas.elements = svg_elements
        return canvas

    def _check_geometry(self, geo):
        """Check that the geometry object is valid."""
        assert isinstance(geo, (AnalysisGeometry, ContextGeometry)), 'Expected ' \
            'AnalysisGeometry or ContextGeometry for VisualizationSet geometry. ' \
            'Got {}.'.format(type(geo))

    def _calculate_min_max(self, with_legend=False):
        """Calculate maximum and minimum Point3D for this object."""
        all_geo = []
        for geo_obj in self.geometry:
            if with_legend and isinstance(geo_obj, AnalysisGeometry):
                all_geo.append(geo_obj.min_point_with_legend)
                all_geo.append(geo_obj.max_point_with_legend)
            else:
                all_geo.append(geo_obj.min_point)
                all_geo.append(geo_obj.max_point)
        if len(all_geo) != 0:
            if with_legend:
                self._min_point_with_legend, self._max_point_with_legend = \
                    bounding_box(all_geo)
            else:
                self._min_point, self._max_point = bounding_box(all_geo)

    def _conversion_factor_to_meters(self, units):
        """Get the conversion factor to meters based on input units.

        Args:
            units: Text for the units.

        Returns:
            A number for the conversion factor, which should be multiplied by
            all distance units taken from Rhino geometry in order to convert
            them to meters.
        """
        if units == 'Meters':
            return 1.0
        elif units == 'Millimeters':
            return 0.001
        elif units == 'Feet':
            return 0.305
        elif units == 'Inches':
            return 0.0254
        elif units == 'Centimeters':
            return 0.01
        else:
            raise ValueError(
                'You are kidding me! What units are you using? {}?\n'
                'Please use one of the following: {}'.format(units, ' '.join(self.UNITS))
            )

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __copy__(self):
        new_geo_objs = tuple(obj.duplicate() for obj in self.geometry)
        new_obj = VisualizationSet(self.identifier, new_geo_objs, self.units)
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
