# coding: utf-8
"""Base classes for all 2D geometry objects."""
import math

from ladybug.color import Color

from ladybug_display._base import _DisplayBase, LINE_TYPES
from ladybug_display.altnumber import default
from ladybug_display.typing import float_positive


class _DisplayBase2D(_DisplayBase):
    """A base class for all 2D ladybug-display geometry objects.

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

    def rotate(self, angle, origin):
        """Rotate this geometry counterclockwise by a certain angle.

        Args:
            angle: An angle for rotation in degrees.
            origin: A Point2D for the origin around which the line segment will
                be rotated.
        """
        self._geometry = self.geometry.rotate(math.radians(angle), origin)

    def reflect(self, normal, origin):
        """Reflect this geometry across a plane defined by a normal and origin.

        Args:
            normal: A Vector2D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point2D representing the origin from which to reflect.
        """
        self._geometry = self.geometry.reflect(normal, origin)

    def scale(self, factor, origin=None):
        """Scale this geometry by a factor from an origin point.

        Args:
            factor: A number representing how much the object should be scaled.
            origin: A ladybug_geometry Point representing the origin from which
                to scale. If None, it will be scaled from the World origin.
        """
        self._geometry = self.geometry.scale(factor, origin)

    def __repr__(self):
        return 'Ladybug Display 2D Base Object'


class _SingleColorBase2D(_DisplayBase2D):
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
        _DisplayBase2D.__init__(self, geometry)
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


class _LineCurveBase2D(_SingleColorBase2D):
    """A base class for all line-like 2D geometry objects.

    Args:
        geometry: A ladybug-geometry object.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        line_width: Number for line width in pixels (for the screen) or millimeters
            (in print). This can also be the Default object to indicate that the
            default settings of the interface should be used.
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
        _SingleColorBase2D.__init__(self, geometry, color)
        self.line_width = line_width
        self.line_type = line_type

    @property
    def line_width(self):
        """Get or set a color for this object."""
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
