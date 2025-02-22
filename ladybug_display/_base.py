# coding: utf-8
"""Base class for all geometry objects."""
from .typing import valid_string

LINE_TYPES = ('Continuous', 'Dashed', 'Dotted', 'DashDot')
DISPLAY_MODES = ('Surface', 'SurfaceWithEdges', 'Wireframe', 'Points')


class _DisplayBase(object):
    """A base class for all ladybug-display geometry objects.

    Args:
        geometry: A ladybug-geometry object.

    Properties:
        * geometry
        * user_data
    """
    __slots__ = ('_geometry', '_user_data')

    def __init__(self, geometry):
        """Initialize base object."""
        self._geometry = geometry
        self._user_data = None

    @property
    def geometry(self):
        """Get a ladybug_geometry object."""
        return self._geometry

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
            assert isinstance(value, dict), 'Expected dictionary for honeybee ' \
                'object user_data. Got {}.'.format(type(value))
        self._user_data = value

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def __copy__(self):
        new_obj = self.__class__(self.geometry)
        new_obj._user_data = None if self.user_data is None else self.user_data.copy()
        return new_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Ladybug Display Base Object'


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
