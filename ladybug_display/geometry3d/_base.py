# coding: utf-8
"""Base classes for all 3D geometry objects."""
import math

from ladybug.color import Color

from ladybug_display._base import _DisplayBase, DISPLAY_MODES, LINE_TYPES
from ladybug_display.altnumber import default
from ladybug_display.typing import float_positive


class _DisplayBase3D(_DisplayBase):
    """A base class for all 3D ladybug-display geometry objects.

    Args:
        geometry: A ladybug-geometry object.

    Properties:
        * geometry
        * user_data
    """
    __slots__ = ()

    def __init__(self, geometry):
        """Initialize base with shade object."""
        _DisplayBase.__init__(self, geometry)

    def move(self, moving_vec):
        """Move this geometry along a vector.

        Args:
            moving_vec: A ladybug_geometry Vector with the direction and distance
                to move the geometry.
        """
        self._geometry = self.geometry.move(moving_vec)

    def rotate(self, axis, angle, origin):
        """Rotate this geometry by a certain angle around an axis and origin.

        Args:
            axis: A ladybug_geometry Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in degrees.
            origin: A ladybug_geometry Point3D for the origin around which the
                object will be rotated.
        """
        self._geometry = self.geometry.rotate(axis, math.radians(angle), origin)

    def rotate_xy(self, angle, origin):
        """Rotate this geometry counterclockwise in the world XY plane by an angle.

        Args:
            angle: An angle in degrees.
            origin: A ladybug_geometry Point3D for the origin around which the
                object will be rotated.
        """
        self._geometry = self.geometry.rotate_xy(math.radians(angle), origin)

    def reflect(self, plane):
        """Reflect this geometry across a plane.

        Args:
            plane: A ladybug_geometry Plane across which the object will
                be reflected.
        """
        self._geometry = self.geometry.reflect(plane.n, plane.o)

    def scale(self, factor, origin=None):
        """Scale this geometry by a factor from an origin point.

        Args:
            factor: A number representing how much the object should be scaled.
            origin: A ladybug_geometry Point representing the origin from which
                to scale. If None, it will be scaled from the World origin.
        """
        self._geometry = self.geometry.scale(factor, origin)

    def __repr__(self):
        return 'Ladybug Display 3D Base Object'


class _SingleColorBase3D(_DisplayBase3D):
    """A base class for ladybug-display geometry objects with a single color.

    Args:
        geometry: A ladybug-geometry object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).

    Properties:
        * geometry
        * color
        * user_data
    """
    __slots__ = ('_color',)

    def __init__(self, geometry, color=None):
        """Initialize base with shade object."""
        _DisplayBase3D.__init__(self, geometry)
        self.color = color

    @property
    def color(self):
        """Get or set a color for this object."""
        return self._color

    @color.setter
    def color(self, value):
        if value is None:
            value = Color(0, 0, 0)
        else:
            assert isinstance(value, Color), 'Expected Color for ladybug_display ' \
                'object color. Got {}.'.format(type(value))
        self._color = value


class _SingleColorModeBase3D(_SingleColorBase3D):
    """A base class for ladybug-display geometry objects with a display mode.

    Args:
        geometry: A ladybug-geometry object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        display_mode: Text to indicate the display mode (surface, wireframe, etc.).
            Choose from the following. (Default: Surface).

    Properties:
        * geometry
        * color
        * display_mode
        * user_data
    """
    __slots__ = ('_display_mode',)

    def __init__(self, geometry, color=None, display_mode='Surface'):
        """Initialize object."""
        _SingleColorBase3D.__init__(self, geometry, color)
        self.display_mode = display_mode

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


class _LineCurveBase3D(_SingleColorBase3D):
    """A base class for all line-like 3D geometry objects.

    Args:
        geometry: A ladybug-geometry object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        line_width: Number for line width in pixels (for the screen). For print,
            this will be converted a value in millimeters or inches assuming
            standard web resolution (72 pixels per inch). This can also be the
            Default object to indicate that the default settings of the
            interface should be used (typically one pixel).
        line_type: Get or set text to indicate the type of line to display.
            Choose from the following. (Default: "Continuous")

            * Continuous
            * Dashed
            * Dotted
            * DashDot

    Properties:
        * geometry
        * color
        * line_width
        * line_type
        * user_data
    """
    __slots__ = ('_line_width', '_line_type')

    def __init__(self, geometry, color=None, line_width=default, line_type='Continuous'):
        """Initialize base with shade object."""
        _SingleColorBase3D.__init__(self, geometry, color)
        self.line_width = line_width
        self.line_type = line_type

    @property
    def line_width(self):
        """Get or set a number to indicate the width of the line in pixels."""
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        if value == default:
            self._line_width = default
        else:
            self._line_width = float_positive(value, 'line width')

    @property
    def line_type(self):
        """Get or set text to indicate the type of line to display."""
        return self._line_type

    @line_type.setter
    def line_type(self, value):
        clean_input = value.lower()
        for key in LINE_TYPES:
            if key.lower() == clean_input:
                value = key
                break
        else:
            raise ValueError(
                'line_type {} is not recognized.\nChoose from the '
                'following:\n{}'.format(value, LINE_TYPES))
        self._line_type = value
