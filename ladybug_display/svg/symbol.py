# coding=utf-8
"""SVG Symbol class."""
from . import _mixins as m
from ._types import PreserveAspectRatio, ViewBoxSpec, \
    _number, _number_or_length, _str, _str_enum, _obj, _list_of_objs
from .element import Element, OVERFLOWS


class Symbol(
    Element,
    m.GraphicsElementEvents,
    m.Color,
    m.Graphics,
):
    """The <symbol> is used to define template objects which can be used by a <use> element.

    The use of <symbol> elements for graphics that are used multiple times in the same
    document adds structure and semantics. Documents that are rich in structure may be
    rendered graphically, as speech, or as Braille, and thus promote accessibility.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/symbol
    """
    OVERFLOWS = OVERFLOWS
    element_name = 'symbol'

    def __init__(self, viewBox=None, preserveAspectRatio=None, refX=None, refY=None,
                 x=None, y=None, class_=None, mask=None, opacity=None,
                 clip_path=None, overflow=None):
        super(Symbol, self).__init__()
        self.viewBox = viewBox
        self.preserveAspectRatio = preserveAspectRatio
        self.refX = refX
        self.refY = refY
        self.x = x
        self.y = y
        self.class_ = class_
        self.mask = mask
        self.opacity = opacity
        self.clip_path = clip_path
        self.overflow = overflow

    @property
    def viewBox(self):
        """[obj]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox
        """
        return self._viewBox

    @viewBox.setter
    def viewBox(self, value):
        self._viewBox = _obj(value, ViewBoxSpec, 'viewBox', True)

    @property
    def preserveAspectRatio(self):
        """[obj]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/preserveAspectRatio
        """
        return self._preserveAspectRatio

    @preserveAspectRatio.setter
    def preserveAspectRatio(self, value):
        self._preserveAspectRatio = _obj(
            value, PreserveAspectRatio, 'preserveAspectRatio', True)

    @property
    def refX(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/refX
        """
        return self._refX

    @refX.setter
    def refX(self, value):
        self._refX = _number_or_length(value, 'refX', True)

    @property
    def refY(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/refY
        """
        return self._refY

    @refY.setter
    def refY(self, value):
        self._refY = _number_or_length(value, 'refY', True)

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
    def opacity(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/opacity
        """
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = _number(value, 'opacity', True)

    @property
    def clip_path(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/clip-path
        """
        return self._clip_path

    @clip_path.setter
    def clip_path(self, value):
        self._clip_path = _str(value, 'clip_path', True)

    @property
    def overflow(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/overflow
        """
        return self._overflow

    @overflow.setter
    def overflow(self, value):
        self._overflow = _str_enum(value, OVERFLOWS, 'overflow', True)
