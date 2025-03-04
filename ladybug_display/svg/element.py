# coding=utf-8
"""Base class for all SVG elements."""
from . import _mixins as m
from ._transforms import Transform
from ._types import _int, _float, _number, _str, _str_enum, _list_of_objs, _dict

OVERFLOWS = set(('visible', 'hidden', 'scroll', 'auto', 'inherit'))
FILL_RULES = set(('evenodd', 'nonzero', 'inherit'))
VECTOR_EFFECTS = set(('none', 'non-scaling-stroke', 'non-scaling-size',
                      'non-rotation', 'fixed-position'))
VISIBILITIES = set(('visible', 'hidden', 'inherit'))
LINECAPS = set(('butt', 'round', 'square', 'inherit'))
LINEJOINS = set(('miter', 'round', 'bevel', 'inherit'))
LENGTH_ADJUSTS = set(('spacing', 'spacingAndGlyphs'))
WRITING_MODES = set(('horizontal-tb', 'vertical-rl', 'vertical-lr'))


class Element(object):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/Core
    """
    element_name = ''

    def __init__(self, elements=None, text=None, id=None, tabindex=None, lang=None,
                 transform_origin=None, style=None, data=None):
        self.elements = elements
        self.text = text
        self.id = id
        self.tabindex = tabindex
        self.lang = lang
        self.transform_origin = transform_origin
        self.style = style
        self.data = data

    @property
    def elements(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/elements
        """
        return self._elements

    @elements.setter
    def elements(self, value):
        self._elements = _list_of_objs(value, Element, 'elements', True)

    @property
    def text(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text
        """
        return self._text

    @text.setter
    def text(self, value):
        self._text = _str(value, 'text', True)

    @property
    def id(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/id
        """
        return self._id

    @id.setter
    def id(self, value):
        self._id = _str(value, 'id', True)

    @property
    def tabindex(self):
        """[int]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/tabindex
        """
        return self._tabindex

    @tabindex.setter
    def tabindex(self, value):
        self._tabindex = _int(value, 'tabindex', True)

    @property
    def lang(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/lang
        """
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = _str(value, 'lang', True)

    @property
    def transform_origin(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform-origin
        """
        return self._transform_origin

    @transform_origin.setter
    def transform_origin(self, value):
        self._transform_origin = _str(value, 'transform_origin', True)

    @property
    def style(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/style
        """
        return self._style

    @style.setter
    def style(self, value):
        self._style = _str(value, 'style', True)

    @property
    def data(self):
        """[dict]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/data
        """
        return self._data

    @data.setter
    def data(self, value):
        self._data = _dict(value, 'data', True)

    @classmethod
    def _as_str(cls, val):
        """Get Element as string."""
        if val is None:
            return ''
        if isinstance(val, Element):
            return str(val)
        if isinstance(val, bool):
            return str(val).lower()
        if isinstance(val, (list, tuple)):
            return ' '.join(cls._as_str(v) for v in val)
        return str(val)

    def as_dict(self):
        result = {}
        for key, val in vars(self).items():
            if val is None:
                continue
            key = key.strip('_')
            if key in ('elements', 'text', 'data'):
                continue
            key = key.rstrip('_')
            key = key.replace('__', ':')
            key = key.replace('_', '-')
            result[key] = self._as_str(val)
        return result

    def as_str(self):
        props = ' '.join('{}="{}"'.format(k, v) for k, v in self.as_dict().items())
        if self.data:
            props += ' ' + ' '.join('data-{}="{}"'.format(k, v) for k, v in self.data.items())
        if self.text:
            return '<{} {}>{}</{}>'.format(
                self.element_name, props, self.text, self.element_name)
        if self.elements:
            content = ''.join(self._as_str(e) for e in self.elements)
            return '<{} {}>{}</{}>'.format(self.element_name, props, content, self.element_name)
        return '<{} {}/>'.format(self.element_name, props)

    def __str__(self):
        return self.as_str()

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__str__()


class _FigureElement(m.Color, m.GraphicsElementEvents, m.Graphics, m.FillStroke):
    PAINT_ORDERS = set(('normal', 'fill', 'stroke', 'markers'))
    RENDERINGS = set(('auto', 'optimizeSpeed', 'crispEdges', 'geometricPrecision', 'inherit'))

    def __init__(self, pathLength=None, paint_order=None, shape_rendering=None,
                 class_=None, vector_effect=None, visibility=None, mask=None,
                 opacity=None, clip_path=None):
        super(_FigureElement, self).__init__()
        self.pathLength = pathLength
        self.paint_order = paint_order
        self.shape_rendering = shape_rendering
        self.class_ = class_
        self.vector_effect = vector_effect
        self.visibility = visibility
        self.mask = mask
        self.opacity = opacity
        self.clip_path = clip_path

    @property
    def pathLength(self):
        """[float]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/pathLength
        """
        return self._pathLength

    @pathLength.setter
    def pathLength(self, value):
        self._pathLength = _float(value, 'pathLength', True)

    @property
    def paint_order(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/paint-order
        """
        return self._paint_order

    @paint_order.setter
    def paint_order(self, value):
        self._paint_order = _str_enum(value, self.PAINT_ORDERS, 'paint_order', True)

    @property
    def shape_rendering(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/shape-rendering
        """
        return self._shape_rendering

    @shape_rendering.setter
    def shape_rendering(self, value):
        self._shape_rendering = _str_enum(value, self.RENDERINGS, 'shape_rendering', True)

    @property
    def class_(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/class-
        """
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = _list_of_objs(value, str, 'class_', True)

    @property
    def vector_effect(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/vector-effect
        """
        return self._vector_effect

    @vector_effect.setter
    def vector_effect(self, value):
        self._vector_effect = _str_enum(value, VECTOR_EFFECTS, 'vector_effect', True)

    @property
    def visibility(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/visibility
        """
        return self._visibility

    @visibility.setter
    def visibility(self, value):
        self._visibility = _str_enum(value, VISIBILITIES, 'visibility', True)

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


class _TextElement(
    m.FontSpecification,
    m.TextContentElements,
    m.Color,
    m.GraphicsElementEvents,
    m.Graphics,
    m.FillStroke,
):

    PAINT_ORDERS = set(('normal', 'fill', 'stroke', 'markers'))

    def __init__(self, paint_order=None, class_=None, vector_effect=None,
                 visibility=None, fill_opacity=None, fill=None):
        super(_TextElement, self).__init__()
        self.paint_order = paint_order
        self.class_ = class_
        self.vector_effect = vector_effect
        self.visibility = visibility
        self.fill_opacity = fill_opacity
        self.fill = fill

    @property
    def paint_order(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/paint-order
        """
        return self._paint_order

    @paint_order.setter
    def paint_order(self, value):
        self._paint_order = _str_enum(value, self.PAINT_ORDERS, 'paint_order', True)

    @property
    def class_(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/class-
        """
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = _list_of_objs(value, str, 'class_', True)

    @property
    def vector_effect(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/vector-effect
        """
        return self._vector_effect

    @vector_effect.setter
    def vector_effect(self, value):
        self._vector_effect = _str_enum(value, VECTOR_EFFECTS, 'vector_effect', True)

    @property
    def visibility(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/visibility
        """
        return self._visibility

    @visibility.setter
    def visibility(self, value):
        self._visibility = _str_enum(value, VISIBILITIES, 'visibility', True)

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


class _Gradient:
    UNITS = set(('userSpaceOnUse', 'objectBoundingBox'))
    SPREAD_METHODS = set(('pad', 'reflect', 'repeat'))

    def __init__(self, externalResourcesRequired=None,
                 gradientUnits=None, gradientTransform=None, spreadMethod=None,
                 href=None, class_=None):
        super(_Gradient, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.gradientUnits = gradientUnits
        self.gradientTransform = gradientTransform
        self.spreadMethod = spreadMethod
        self.href = href
        self.class_ = class_

    @property
    def externalResourcesRequired(self):
        """[bool]"""
        return self._externalResourcesRequired

    @externalResourcesRequired.setter
    def externalResourcesRequired(self, value):
        self._externalResourcesRequired = bool(value) if value is not None else None

    @property
    def gradientUnits(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/gradientUnits
        """
        return self._gradientUnits

    @gradientUnits.setter
    def gradientUnits(self, value):
        self._gradientUnits = _str_enum(value, self.UNITS, 'gradientUnits', True)

    @property
    def gradientTransform(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/gradientTransform
        """
        return self._gradientTransform

    @gradientTransform.setter
    def gradientTransform(self, value):
        self._gradientTransform = _list_of_objs(value, Transform, 'gradientTransform', True)

    @property
    def spreadMethod(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/spreadMethod
        """
        return self._spreadMethod

    @spreadMethod.setter
    def spreadMethod(self, value):
        self._spreadMethod = _str_enum(value, self.SPREAD_METHODS, 'spreadMethod', True)

    @property
    def href(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/href
        """
        return self._href

    @href.setter
    def href(self, value):
        self._href = _str(value, 'href', True)

    @property
    def class_(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/class-
        """
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = _list_of_objs(value, str, 'class_', True)
