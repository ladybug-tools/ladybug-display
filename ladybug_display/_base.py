# coding: utf-8
"""Base class for all geometry objects."""
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
