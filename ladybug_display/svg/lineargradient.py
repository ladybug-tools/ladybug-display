# coding=utf-8
"""SVG LinearGradient class."""
from . import _mixins as m
from ._types import _number_or_length
from .element import Element, _Gradient


class LinearGradient(Element, _Gradient, m.Color, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/linearGradient
    """
    element_name = 'linearGradient'

    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        super(LinearGradient, self).__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def x1(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/x1
        """
        return self._x1

    @x1.setter
    def x1(self, value):
        self._x1 = _number_or_length(value, 'x1', True)

    @property
    def y1(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/y1
        """
        return self._y1

    @y1.setter
    def y1(self, value):
        self._y1 = _number_or_length(value, 'y1', True)

    @property
    def x2(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/x2
        """
        return self._x2

    @x2.setter
    def x2(self, value):
        self._x2 = _number_or_length(value, 'x2', True)

    @property
    def y2(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/y2
        """
        return self._y2

    @y2.setter
    def y2(self, value):
        self._y2 = _number_or_length(value, 'y2', True)
