# coding=utf-8
"""SVG Stop class for gradients."""
from . import _mixins as m
from ._transforms import Transform
from ._types import _number_or_length, _str, _str_enum, _list_of_objs
from .element import Element


class Mask(Element, m.Color, m.Graphics):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/mask
    """
    UNITS = set(('userSpaceOnUse', 'objectBoundingBox'))
    element_name = 'mask'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 maskUnits=None, x=None, y=None, width=None, height=None,
                 maskContentUnits=None, class_=None, mask=None, clip_path=None):
        super(Mask, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.transform = transform
        self.maskUnits = maskUnits
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.maskContentUnits = maskContentUnits
        self.class_ = class_
        self.mask = mask
        self.clip_path = clip_path

    @property
    def externalResourcesRequired(self):
        """[bool]"""
        return self._externalResourcesRequired

    @externalResourcesRequired.setter
    def externalResourcesRequired(self, value):
        self._externalResourcesRequired = bool(value) if value is not None else None

    @property
    def transform(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
        """
        return self._transform

    @transform.setter
    def transform(self, value):
        self._transform = _list_of_objs(value, Transform, 'transform', True)

    @property
    def maskUnits(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/maskUnits
        """
        return self._maskUnits

    @maskUnits.setter
    def maskUnits(self, value):
        self._maskUnits = _str_enum(value, self.UNITS, 'maskUnits', True)

    @property
    def x(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/x
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = _number_or_length(value, 'x', True)

    @property
    def y(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/y
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = _number_or_length(value, 'y', True)

    @property
    def width(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/width
        """
        return self._width

    @width.setter
    def width(self, value):
        self._width = _number_or_length(value, 'width', True)

    @property
    def height(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/height
        """
        return self._height

    @height.setter
    def height(self, value):
        self._height = _number_or_length(value, 'height', True)

    @property
    def maskContentUnits(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/maskContentUnits
        """
        return self._maskContentUnits

    @maskContentUnits.setter
    def maskContentUnits(self, value):
        self._maskContentUnits = _str_enum(value, self.UNITS, 'maskContentUnits', True)

    @property
    def class_(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/class
        """
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = _list_of_objs(value, str, 'class_', True)

    @property
    def mask(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/mask
        """
        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = _str(value, 'mask', True)

    @property
    def clip_path(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/clip-path
        """
        return self._clip_path

    @clip_path.setter
    def clip_path(self, value):
        self._clip_path = _str(value, 'clip_path', True)
