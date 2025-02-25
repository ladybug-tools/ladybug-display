"""SVG Rectangle class."""
from ._transforms import Transform
from ._types import _number, _number_or_length, _str, _str_enum, _list_of_objs
from .element import Element, _FigureElement, LINEJOINS


class Rect(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/rect
    """
    LINEJOINS = LINEJOINS
    element_name = 'rect'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 x=None, y=None, width=None, height=None, rx=None, ry=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 stroke_linejoin=None, stroke_miterlimit=None,
                 fill_opacity=None, fill=None):
        super(Rect, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.transform = transform
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry
        self.marker_start = marker_start
        self.marker_mid = marker_mid
        self.marker_end = marker_end
        self.stroke_linejoin = stroke_linejoin
        self.stroke_miterlimit = stroke_miterlimit
        self.fill_opacity = fill_opacity
        self.fill = fill

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
    def rx(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/rx
        """
        return self._rx

    @rx.setter
    def rx(self, value):
        self._rx = _number_or_length(value, 'rx', True)

    @property
    def ry(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/ry
        """
        return self._ry

    @ry.setter
    def ry(self, value):
        self._ry = _number_or_length(value, 'ry', True)

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
    def stroke_linejoin(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin
        """
        return self._stroke_linejoin

    @stroke_linejoin.setter
    def stroke_linejoin(self, value):
        self._stroke_linejoin = _str_enum(value, LINEJOINS, 'stroke_linejoin', True)

    @property
    def stroke_miterlimit(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-miterlimit
        """
        return self._stroke_miterlimit

    @stroke_miterlimit.setter
    def stroke_miterlimit(self, value):
        self._stroke_miterlimit = _number(value, 'stroke_miterlimit', True)

    @property
    def fill_opacity(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-opacity
        """
        return self._fill_opacity

    @fill_opacity.setter
    def fill_opacity(self, value):
        self._fill_opacity = _number(value, 'fill_opacity', True)

    @property
    def fill(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill
        """
        return self._fill

    @fill.setter
    def fill(self, value):
        self._fill = _str(value, 'fill', True)
