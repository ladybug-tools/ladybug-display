"""Class for specifying text within the 3D scene."""
from ladybug_geometry.geometry3d import Plane, Point3D
from ladybug.color import Color

from ._base import _SingleColorBase3D
from ladybug_display.typing import float_positive


class DisplayText3D(_SingleColorBase3D):
    """A text object in 3D space with display properties.

    Args:
        text: A text string to be displayed in the 3D scene.
        plane: A ladybug-geometry Plane object to locate and orient the text in
            the 3D scene.
        height: A number for the height of the text in the 3D scene.
        color: A ladybug Color object. If None, a default black color will be
            used. (Default: None).
        font: A text string for the font in which to draw the text. Note that this field
            may not be interpreted the same on all machines and in all interfaces,
            particularly when a machine lacks a given font. (Default: Arial)
        horizontal_alignment: String to specify the horizontal alignment
             of the text. (Default: Left). Choose from:

             * Left
             * Center
             * Right

        vertical_alignment: String to specify the vertical alignment
             of the text. (Default: Bottom). Choose from:

             * Top
             * Middle
             * Bottom

    Properties:
        * text
        * plane
        * geometry
        * height
        * color
        * font
        * horizontal_alignment
        * vertical_alignment
        * min
        * max
        * user_data
    """
    __slots__ = ('_text', '_height', '_font', '_horizontal_alignment',
                 '_vertical_alignment')

    HORIZONTAL_ALIGN = ('Left', 'Center', 'Right')
    VERTICAL_ALIGN = ('Top', 'Middle', 'Bottom')

    def __init__(self, text, plane, height, color=None, font='Arial',
                 horizontal_alignment='Left', vertical_alignment='Bottom'):
        """Initialize object."""
        assert isinstance(plane, Plane), '\
            Expected ladybug_geometry Plane. Got {}'.format(type(plane))
        _SingleColorBase3D.__init__(self, plane, color)
        self.text = text
        self.height = height
        self.font = font
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment

    @classmethod
    def from_dict(cls, data):
        """Initialize a DisplayText3D from a dictionary.

        Args:
            data: A dictionary representation of an DisplayText3D object.
        """
        assert data['type'] == 'DisplayText3D', \
            'Expected DisplayText3D dictionary. Got {}.'.format(data['type'])
        color = Color.from_dict(data['color']) if 'color' in data and data['color'] \
            is not None else None
        font = data['font'] if 'font' in data and \
            data['font'] is not None else 'Arial'
        h_align = data['horizontal_alignment'] if 'horizontal_alignment' in data and \
            data['horizontal_alignment'] is not None else 'Left'
        v_align = data['vertical_alignment'] if 'vertical_alignment' in data and \
            data['vertical_alignment'] is not None else 'Bottom'
        geo = cls(data['text'], Plane.from_dict(data['plane']), data['height'],
                  color, font, h_align, v_align)
        if 'user_data' in data and data['user_data'] is not None:
            geo.user_data = data['user_data']
        return geo

    @property
    def text(self):
        """Get or set a text string to be displayed in the 3D scene."""
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)

    @property
    def plane(self):
        """Get a ladybug_geometry Plane for the text."""
        return self._geometry

    @property
    def height(self):
        """Get or set a number for the height of the text in the 3D scene."""
        return self._height

    @height.setter
    def height(self, value):
        self._height = float_positive(value, 'text height')

    @property
    def font(self):
        """Get or set a string for the font in which to draw the text."""
        return self._font

    @font.setter
    def font(self, value):
        self._font = str(value)

    @property
    def horizontal_alignment(self):
        """Get or set text to specify the horizontal alignment."""
        return self._horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, value):
        clean_input = value.lower()
        for key in self.HORIZONTAL_ALIGN:
            if key.lower() == clean_input:
                value = key
                break
        else:
            raise ValueError(
                'horizontal_alignment {} is not recognized.\nChoose from the '
                'following:\n{}'.format(value, self.HORIZONTAL_ALIGN))
        self._horizontal_alignment = value

    @property
    def vertical_alignment(self):
        """Get or set text to specify the vertical alignment."""
        return self._vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value):
        clean_input = value.lower()
        for key in self.VERTICAL_ALIGN:
            if key.lower() == clean_input:
                value = key
                break
        else:
            raise ValueError(
                'vertical_alignment {} is not recognized.\nChoose from the '
                'following:\n{}'.format(value, self.VERTICAL_ALIGN))
        self._vertical_alignment = value

    @property
    def min(self):
        """Get a Point3D for the minimum of the bounding box around the object."""
        sep_text = self.text.split('\n')
        h_len = max([len(txt) for txt in sep_text])
        v_len = len(sep_text)

        if self.horizontal_alignment == 'Right':
            min_x = h_len * self.height
        elif self.horizontal_alignment == 'Center':
            min_x = (h_len * self.height) / 2
        else:
            min_x = 0
        min_x = self.plane.o.x - min_x

        if self.vertical_alignment == 'Top':
            min_y = v_len * self.height
        elif self.vertical_alignment == 'Middle':
            min_y = (v_len * self.height) / 2
        else:
            min_y = 0
        min_y = self.plane.o.y + min_y
        return Point3D(min_x, min_y, self.plane.o.z)

    @property
    def max(self):
        """Get a Point3D for the maximum of the bounding box around the object."""
        sep_text = self.text.split('\n')
        h_len = max([len(txt) for txt in sep_text])
        v_len = len(sep_text)

        if self.horizontal_alignment == 'Left':
            max_x = h_len * self.height
        elif self.horizontal_alignment == 'Center':
            max_x = (h_len * self.height) / 2
        else:
            max_x = 0
        max_x = self.plane.o.x + max_x

        if self.vertical_alignment == 'Bottom':
            max_y = v_len * self.height
        elif self.vertical_alignment == 'Middle':
            max_y = (v_len * self.height) / 2
        else:
            max_y = self.height
        max_y = self.plane.o.y + max_y
        return Point3D(max_x, max_y, self.plane.o.z)

    def to_dict(self):
        """Return DisplayText3D as a dictionary."""
        base = {'type': 'DisplayText3D'}
        base['text'] = self.text
        base['plane'] = self.plane.to_dict()
        base['height'] = self.height
        base['color'] = self.color.to_dict()
        base['font'] = self.font
        base['horizontal_alignment'] = self.horizontal_alignment
        base['vertical_alignment'] = self.vertical_alignment
        if self.user_data is not None:
            base['user_data'] = self.user_data
        return base

    def __copy__(self):
        new_g = DisplayText3D(
            self.text, self.plane, self.height, self.color, self.font,
            self.horizontal_alignment, self.vertical_alignment)
        new_g._user_data = None if self.user_data is None else self.user_data.copy()
        return new_g

    def __repr__(self):
        return 'DisplayText3D: {}'.format(self.plane)
