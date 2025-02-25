"""SVG Circle class."""
from ._transforms import Transform
from ._types import _number, _number_or_length, _str, _list_of_objs
from .element import Element, _FigureElement


class Circle(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/circle
    """
    element_name = 'circle'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 cx=None, cy=None, r=None,
                 marker_mid=None, fill_opacity=None, fill=None):
        super(Circle, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.transform = transform
        self.cx = cx
        self.cy = cy
        self.r = r
        self.marker_mid = marker_mid
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
    def cx(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/cx
        """
        return self._cx

    @cx.setter
    def cx(self, value):
        self._cx = _number_or_length(value, 'cx', True)

    @property
    def cy(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/cy
        """
        return self._cy

    @cy.setter
    def cy(self, value):
        self._cy = _number_or_length(value, 'cy', True)

    @property
    def r(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/r
        """
        return self._r

    @r.setter
    def r(self, value):
        self._r = _number_or_length(value, 'r', True)

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
