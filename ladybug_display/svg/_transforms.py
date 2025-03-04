# coding=utf-8
"""Classes for representing Transforms."""
from ._types import _number


class Transform:
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
    """
    pass


class Matrix(Transform):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform#matrix
    """
    __slots__ = ('a', 'b', 'c', 'd', 'e', 'f')

    def __init__(self, a, b, c, d, e, f):
        self.a = _number(a, 'a')
        self.b = _number(b, 'b')
        self.c = _number(c, 'c')
        self.d = _number(d, 'd')
        self.e = _number(e, 'e')
        self.f = _number(f, 'f')

    def __str__(self):
        return 'matrix({} {} {} {} {} {})'.format(
            self.a, self.b, self.c, self.d, self.e, self.f)


class Translate(Transform):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform#translate
    """
    __slots__ = ('x', 'y')

    def __init__(self, x, y=None):
        self.x = _number(x, 'x')
        self.y = _number(y, 'y', True)

    def __str__(self):
        if self.y is None:
            return 'translate({})'.format(self.x)
        return 'translate({} {})'.format(self.x, self.y)


class Scale(Transform):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform#scale
    """
    __slots__ = ('x', 'y')

    def __init__(self, x, y=None):
        self.x = _number(x, 'x')
        self.y = _number(y, 'y', True)

    def __str__(self):
        if self.y is None:
            return 'scale({})'.format(self.x)
        return 'scale({} {})'.format(self.x, self.y)


class Rotate(Transform):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform#rotate
    """
    __slots__ = ('a', 'x', 'y')

    def __init__(self, a, x=None, y=None):
        self.a = _number(a, 'a')
        self.x = _number(x, 'x', True)
        self.y = _number(y, 'y', True)

    def __str__(self):
        if self.x is None:
            return 'rotate({})'.format(self.a)
        assert self.y is not None
        return 'rotate({} {} {})'.format(self.a, self.x, self.y)


class SkewX(Transform):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform#skewx
    """
    __slots__ = ('a',)

    def __init__(self, a):
        self.a = _number(a, 'a')

    def __str__(self):
        return 'skewX({})'.format(self.a)


class SkewY(Transform):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform#skewy
    """
    __slots__ = ('a',)

    def __init__(self, a):
        self.a = _number(a, 'a')

    def __str__(self):
        return 'skewY({})'.format(self.a)
