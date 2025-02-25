"""SVG Path class."""
from ._path import PathData
from ._transforms import Transform
from ._types import _number, _str, _str_enum, _list_of_objs
from .element import Element, _FigureElement, LINECAPS, LINEJOINS, FILL_RULES


class Path(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/path
    """
    LINECAPS = LINECAPS
    LINEJOINS = LINEJOINS
    FILL_RULES = FILL_RULES
    element_name = 'path'

    def __init__(self, externalResourcesRequired=None, transform=None, d=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 stroke_linecap=None, stroke_linejoin=None, stroke_miterlimit=None,
                 fill_rule=None, fill_opacity=None, fill=None):
        super(Path, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.transform = transform
        self.d = d
        self.marker_start = marker_start
        self.marker_mid = marker_mid
        self.marker_end = marker_end
        self.stroke_linecap = stroke_linecap
        self.stroke_linejoin = stroke_linejoin
        self.stroke_miterlimit = stroke_miterlimit
        self.fill_rule = fill_rule
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
    def d(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d
        """
        return self._d

    @d.setter
    def d(self, value):
        self._d = _list_of_objs(value, PathData, 'd', True)

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
    def fill_rule(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule
        """
        return self._fill_rule

    @fill_rule.setter
    def fill_rule(self, value):
        self._fill_rule = _str_enum(value, FILL_RULES, 'fill_rule', True)

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
