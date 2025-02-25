"""SVG Line class."""
from ._transforms import Transform
from ._types import _number_or_length, _str, _str_enum, _list_of_objs
from .element import Element, _FigureElement, LINECAPS


class Line(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/line
    """
    LINECAPS = LINECAPS
    element_name = 'line'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 x1=None, y1=None, x2=None, y2=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 stroke_linecap=None):
        super(Line, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.transform = transform
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.marker_start = marker_start
        self.marker_mid = marker_mid
        self.marker_end = marker_end
        self.stroke_linecap = stroke_linecap

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

    @property
    def marker_start(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/marker-start
        """
        return self._marker_start

    @marker_start.setter
    def marker_start(self, value):
        self._marker_start = _str(value, 'marker_start', True)

    @property
    def marker_mid(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/marker-mid
        """
        return self._marker_mid

    @marker_mid.setter
    def marker_mid(self, value):
        self._marker_mid = _str(value, 'marker_mid', True)

    @property
    def marker_end(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/marker-end
        """
        return self._marker_end

    @marker_end.setter
    def marker_end(self, value):
        self._marker_end = _str(value, 'marker_end', True)

    @property
    def stroke_linecap(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linecap
        """
        return self._stroke_linecap

    @stroke_linecap.setter
    def stroke_linecap(self, value):
        self._stroke_linecap = _str_enum(value, LINECAPS, 'stroke_linecap', True)
