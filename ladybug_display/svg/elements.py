"""Classes for constructing SVGs."""
from . import _mixins as m
from ._path import PathData
from ._transforms import Transform
from ._types import Number, PreserveAspectRatio, ViewBoxSpec, \
    _int, _float, _number, _number_or_length, _str, _str_enum, \
    _obj, _list_of_objs, _dict

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
        self.elements = _list_of_objs(elements, Element, 'elements', True)
        self.text = _str(text, 'text', True)
        self.id = _str(id, 'id', True)
        self.tabindex = _int(tabindex, 'tabindex', True)
        self.lang = _str(lang, 'lang', True)

        self.transform_origin = _str(transform_origin, 'transform_origin', True)
        self.style = _str(style, 'style', True)
        self.data = _dict(data, 'data', True)

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


class SVG(
    Element,
    m.GraphicsElementEvents,
    m.Color,
    m.Graphics,
):
    """The svg element is a container that defines a new coordinate system and viewport.

    It is used as the outermost element of SVG documents, but it can also be used
    to embed an SVG fragment inside an SVG or HTML document.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/svg
    """
    element_name = 'svg'

    def __init__(self, xmlns=None, viewBox=None, preserveAspectRatio=None,
                 x=None, y=None, width=None, height=None, class_=None,
                 mask=None, opacity=None, clip_path=None, overflow=None,
                 onunload=None, onabort=None, onerror=None, onresize=None,
                 onscroll=None, onzoom=None):
        super(SVG, self).__init__()
        self.xmlns = _str(xmlns, 'xmlns') \
            if xmlns is not None else 'http://www.w3.org/2000/svg'
        self.viewBox = _obj(viewBox, ViewBoxSpec, 'viewBox', True)
        self.preserveAspectRatio = \
            _obj(preserveAspectRatio, PreserveAspectRatio, 'preserveAspectRatio', True)
        self.x = _number_or_length(x, 'x', True)
        self.y = _number_or_length(y, 'y', True)
        self.width = _number_or_length(width, 'width', True)
        self.height = _number_or_length(height, 'height', True)

        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.mask = _str(mask, 'mask', True)
        self.opacity = _number(opacity, 'opacity', True)
        self.clip_path = _str(clip_path, 'clip_path', True)
        self.overflow = _str_enum(overflow, OVERFLOWS, 'overflow', True)

        self.onunload = _str(onunload, 'onunload', True)
        self.onabort = _str(onabort, 'onabort', True)
        self.onerror = _str(onerror, 'onerror', True)
        self.onresize = _str(onresize, 'onresize', True)
        self.onscroll = _str(onscroll, 'onscroll', True)
        self.onzoom = _str(onzoom, 'onzoom', True)


class G(
    Element,
    m.GraphicsElementEvents,
    m.Color,
    m.Graphics,
):
    """The <g> SVG element is a container used to group other SVG elements.

    Transformations applied to the <g> element are performed on its child elements,
    and its attributes are inherited by its children. It can also group multiple elements
    to be referenced later with the <use> element.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/g
    """
    element_name = 'g'

    def __init__(self, transform=None, class_=None, mask=None, opacity=None,
                 clip_path=None, fill_rule=None, fill_opacity=None, fill=None):
        super(G, self).__init__()
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.mask = _str(mask, 'mask', True)
        self.opacity = _number(opacity, 'opacity', True)
        self.clip_path = _str(clip_path, 'clip_path', True)
        self.fill_rule = _str_enum(fill_rule, FILL_RULES, 'fill_rule', True)
        self.fill_opacity = _number(fill_opacity, 'fill_opacity', True)
        self.fill = _str(fill, 'fill', True)


class Defs(
    Element,
    m.Color,
    m.GraphicsElementEvents,
):
    """The <defs> is used to store graphical objects that will be used at a later time.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/defs
    """
    element_name = 'defs'

    def __init__(self, transform=None, class_=None, pointer_events=None):
        super(Defs, self).__init__()
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.pointer_events = _str(pointer_events, 'pointer_events', True)  # TODO


class Desc(Element, m.GraphicsElementEvents):
    """The <desc> element provides an accessible, long-text description of any element.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/desc
    """
    element_name = 'desc'

    def __init__(self, content=None, class_=None):
        super(Desc, self).__init__()
        self.content = _str(content, 'content', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)


class Title(Element, m.GraphicsElementEvents):
    """The <title> element provides an accessible, short-text description of any element.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title
    """
    element_name = 'title'

    def __init__(self, content=None, class_=None):
        super(Title, self).__init__()
        self.content = _str(content, 'content', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)


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
    element_name = 'symbol'

    def __init__(self, viewBox=None, preserveAspectRatio=None, refX=None, refY=None,
                 x=None, y=None, class_=None, mask=None, opacity=None,
                 clip_path=None, overflow=None):
        super(Symbol, self).__init__()
        self.viewBox = _obj(viewBox, ViewBoxSpec, 'viewBox', True)
        self.preserveAspectRatio = \
            _obj(preserveAspectRatio, PreserveAspectRatio, 'preserveAspectRatio', True)
        self.refX = _number_or_length(refX, 'refX', True)
        self.refY = _number_or_length(refY, 'refY', True)
        self.x = _number_or_length(x, 'x', True)
        self.y = _number_or_length(y, 'y', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.mask = _str(mask, 'mask', True)
        self.opacity = _number(opacity, 'opacity', True)
        self.clip_path = _str(clip_path, 'clip_path', True)
        self.overflow = _str_enum(overflow, OVERFLOWS, 'overflow', True)


class Image(
    Element,
    m.Color,
    m.Graphics,
    m.GraphicsElementEvents,
):
    """The <image> SVG element includes images inside SVG documents.

    The only image formats SVG software must support are JPEG, PNG, and other SVG files.
    Animated GIF behavior is undefined.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/image
    """
    RENDERINGS = set(('auto', 'optimizeSpeed', 'optimizeQuality'))
    element_name = 'image'

    def __init__(self, href=None, transform=None, x=None, y=None, width=None, height=None,
                 preserveAspectRatio=None, image_rendering=None, class_=None,
                 vector_effect=None, visibility=None, mask=None, opacity=None,
                 clip_path=None, overflow=None):
        super(Image, self).__init__()
        self.href = _str(href, 'href', True)
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.x = _number_or_length(x, 'x', True)
        self.y = _number_or_length(y, 'y', True)
        self.width = _number_or_length(width, 'width', True)
        self.height = _number_or_length(height, 'height', True)
        self.preserveAspectRatio = \
            _obj(preserveAspectRatio, PreserveAspectRatio, 'preserveAspectRatio', True)
        self.image_rendering = \
            _str_enum(image_rendering, self.RENDERINGS, 'image_rendering', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.vector_effect = _str_enum(vector_effect, VECTOR_EFFECTS, 'vector_effect', True)
        self.visibility = _str_enum(visibility, VISIBILITIES, 'visibility', True)
        self.mask = _str(mask, 'mask', True)
        self.opacity = _number(opacity, 'opacity', True)
        self.clip_path = _str(clip_path, 'clip_path', True)
        self.overflow = _str_enum(overflow, OVERFLOWS, 'overflow', True)


class Switch(Element, m.Color, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/switch
    """
    element_name = 'switch'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 opacity=None, class_=None, pointer_events=None):
        super(Switch, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.opacity = _number(opacity, 'opacity', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.pointer_events = _str(pointer_events, 'pointer_events', True)  # TODO


class Style(Element, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/style
    """
    element_name = 'style'

    def __init__(self, type=None, media=None, title=None):
        super(Style, self).__init__()
        self.type = _str(type, 'type', True)
        self.media = _list_of_objs(media, str, 'media', True)
        self.title = _str(title, 'title', True)


class _FigureElement(m.Color, m.GraphicsElementEvents, m.Graphics, m.FillStroke):
    PAINT_ORDERS = set(('normal', 'fill', 'stroke', 'markers'))
    RENDERINGS = set(('auto', 'optimizeSpeed', 'crispEdges', 'geometricPrecision', 'inherit'))

    def __init__(self, pathLength=None, paint_order=None, shape_rendering=None,
                 class_=None, vector_effect=None, visibility=None, mask=None,
                 opacity=None, clip_path=None):
        super(_FigureElement, self).__init__()
        self.pathLength = _float(pathLength, 'pathLength', True)
        self.paint_order = _str_enum(paint_order, self.PAINT_ORDERS, 'paint_order', True)
        self.shape_rendering = _str_enum(shape_rendering, self.RENDERINGS, 'shape_rendering', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.vector_effect = _str_enum(vector_effect, VECTOR_EFFECTS, 'vector_effect', True)
        self.visibility = _str_enum(visibility, VISIBILITIES, 'visibility', True)
        self.mask = _str(mask, 'mask', True)
        self.opacity = _number(opacity, 'opacity', True)
        self.clip_path = _str(clip_path, 'clip_path', True)


class Path(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/path
    """
    element_name = 'path'

    def __init__(self, externalResourcesRequired=None, transform=None, d=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 stroke_linecap=None, stroke_linejoin=None, stroke_miterlimit=None,
                 fill_rule=None, fill_opacity=None, fill=None):
        super(Path, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.d = _list_of_objs(d, PathData, 'd', True)
        self.marker_start = _str(marker_start, 'marker_start', True)
        self.marker_mid = _str(marker_mid, 'marker_mid', True)
        self.marker_end = _str(marker_end, 'marker_end', True)
        self.stroke_linecap = _str_enum(stroke_linecap, LINECAPS, 'stroke_linecap', True)
        self.stroke_linejoin = \
            _str_enum(stroke_linejoin, LINEJOINS, 'stroke_linejoin', True)
        self.stroke_miterlimit = _number(stroke_miterlimit, 'stroke_miterlimit', True)
        self.fill_rule = _str_enum(fill_rule, FILL_RULES, 'fill_rule', True)
        self.fill_opacity = _number(fill_opacity, 'fill_opacity', True)
        self.fill = _str(fill, 'fill', True)


class Rect(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/rect
    """
    element_name = 'rect'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 x=None, y=None, width=None, height=None, rx=None, ry=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 stroke_linejoin=None, stroke_miterlimit=None,
                 fill_opacity=None, fill=None):
        super(Rect, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.x = _number_or_length(x, 'x', True)
        self.y = _number_or_length(y, 'y', True)
        self.width = _number_or_length(width, 'width', True)
        self.height = _number_or_length(height, 'height', True)
        self.rx = _number_or_length(rx, 'rx', True)
        self.ry = _number_or_length(ry, 'ry', True)
        self.marker_start = _str(marker_start, 'marker_start', True)
        self.marker_mid = _str(marker_mid, 'marker_mid', True)
        self.marker_end = _str(marker_end, 'marker_end', True)
        self.stroke_linejoin = \
            _str_enum(stroke_linejoin, LINEJOINS, 'stroke_linejoin', True)
        self.stroke_miterlimit = _number(stroke_miterlimit, 'stroke_miterlimit', True)
        self.fill_opacity = _number(fill_opacity, 'fill_opacity', True)
        self.fill = _str(fill, 'fill', True)


class Circle(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/circle
    """
    element_name = 'circle'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 cx=None, cy=None, r=None,
                 marker_mid=None, fill_opacity=None, fill=None):
        super(Circle, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.cx = _number_or_length(cx, 'cx', True)
        self.cy = _number_or_length(cy, 'cy', True)
        self.r = _number_or_length(r, 'r', True)
        self.marker_mid = _str(marker_mid, 'marker_mid', True)
        self.fill_opacity = _number(fill_opacity, 'fill_opacity', True)
        self.fill = _str(fill, 'fill', True)


class Ellipse(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/ellipse
    """
    element_name = 'ellipse'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 cx=None, cy=None, rx=None, ry=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 fill_opacity=None, fill=None):
        super(Ellipse, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.cx = _number_or_length(cx, 'cx', True)
        self.cy = _number_or_length(cy, 'cy', True)
        self.rx = _number_or_length(rx, 'rx', True)
        self.ry = _number_or_length(ry, 'ry', True)
        self.marker_start = _str(marker_start, 'marker_start', True)
        self.marker_mid = _str(marker_mid, 'marker_mid', True)
        self.marker_end = _str(marker_end, 'marker_end', True)
        self.fill_opacity = _number(fill_opacity, 'fill_opacity', True)
        self.fill = _str(fill, 'fill', True)


class Line(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/line
    """
    element_name = 'line'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 x1=None, y1=None, x2=None, y2=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 stroke_linecap=None):
        super(Line, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.x1 = _number_or_length(x1, 'x1', True)
        self.y1 = _number_or_length(y1, 'y1', True)
        self.x2 = _number_or_length(x2, 'x2', True)
        self.y2 = _number_or_length(y2, 'y2', True)
        self.marker_start = _str(marker_start, 'marker_start', True)
        self.marker_mid = _str(marker_mid, 'marker_mid', True)
        self.marker_end = _str(marker_end, 'marker_end', True)
        self.stroke_linecap = _str_enum(stroke_linecap, LINECAPS, 'stroke_linecap', True)


class Polyline(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/polyline
    """
    element_name = 'polyline'

    def __init__(self, externalResourcesRequired=None, transform=None, points=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 stroke_linecap=None, stroke_linejoin=None, stroke_miterlimit=None,
                 fill_rule=None, fill_opacity=None, fill=None):
        super(Polyline, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.points = _list_of_objs(points, Number, 'points', True)
        self.marker_start = _str(marker_start, 'marker_start', True)
        self.marker_mid = _str(marker_mid, 'marker_mid', True)
        self.marker_end = _str(marker_end, 'marker_end', True)
        self.stroke_linecap = _str_enum(stroke_linecap, LINECAPS, 'stroke_linecap', True)
        self.stroke_linejoin = \
            _str_enum(stroke_linejoin, LINEJOINS, 'stroke_linejoin', True)
        self.stroke_miterlimit = _number(stroke_miterlimit, 'stroke_miterlimit', True)
        self.fill_rule = _str_enum(fill_rule, FILL_RULES, 'fill_rule', True)
        self.fill_opacity = _number(fill_opacity, 'fill_opacity', True)
        self.fill = _str(fill, 'fill', True)


class Polygon(Element, _FigureElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/polygon
    """
    element_name = 'polygon'

    def __init__(self, externalResourcesRequired=None, transform=None, points=None,
                 marker_start=None, marker_mid=None, marker_end=None,
                 stroke_linejoin=None, stroke_miterlimit=None,
                 fill_rule=None, fill_opacity=None, fill=None):
        super(Polygon, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.points = _list_of_objs(points, Number, 'points', True)
        self.marker_start = _str(marker_start, 'marker_start', True)
        self.marker_mid = _str(marker_mid, 'marker_mid', True)
        self.marker_end = _str(marker_end, 'marker_end', True)
        self.stroke_linejoin = \
            _str_enum(stroke_linejoin, LINEJOINS, 'stroke_linejoin', True)
        self.stroke_miterlimit = _number(stroke_miterlimit, 'stroke_miterlimit', True)
        self.fill_rule = _str_enum(fill_rule, FILL_RULES, 'fill_rule', True)
        self.fill_opacity = _number(fill_opacity, 'fill_opacity', True)
        self.fill = _str(fill, 'fill', True)


class _TextElement(
    m.FontSpecification,
    m.TextContentElements,
    m.Color,
    m.GraphicsElementEvents,
    m.Graphics,
    m.FillStroke,
):

    def __init__(self, paint_order=None, class_=None, vector_effect=None,
                 visibility=None, fill_opacity=None, fill=None):
        super(_TextElement, self).__init__()
        self.paint_order = _str_enum(paint_order, self.PAINT_ORDERS, 'paint_order', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.vector_effect = _str_enum(vector_effect, VECTOR_EFFECTS, 'vector_effect', True)
        self.visibility = _str_enum(visibility, VISIBILITIES, 'visibility', True)
        self.fill_opacity = _number(fill_opacity, 'fill_opacity', True)
        self.fill = _str(fill, 'fill', True)


class Text(Element, _TextElement):
    """The SVG <text> element draws a graphics element consisting of text.

    It's possible to apply a gradient, pattern, clipping path, mask, or filter to <text>,
    like any other SVG graphics element.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/text
    """
    RENDERINGS = set(('auto', 'optimizeSpeed', 'optimizeLegibility', 'geometricPrecision'))
    element_name = 'text'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 x=None, y=None, dx=None, dy=None, textLength=None, lengthAdjust=None,
                 writing_mode=None, text_rendering=None, stroke_linecap=None,
                 stroke_linejoin=None, stroke_miterlimit=None, fill_rule=None,
                 mask=None, opacity=None, clip_path=None, overflow=None):
        super(Text, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.x = _number_or_length(x, 'x', True)
        self.y = _number_or_length(y, 'y', True)
        self.dx = _number_or_length(dx, 'width', True)
        self.dy = _number_or_length(dy, 'height', True)
        self.textLength = _number_or_length(textLength, 'textLength', True)
        self.lengthAdjust = _str_enum(lengthAdjust, LENGTH_ADJUSTS, 'lengthAdjust', True)
        self.writing_mode = _str_enum(writing_mode, WRITING_MODES, 'writing_mode', True)
        self.text_rendering = _str_enum(text_rendering, self.RENDERINGS, 'text_rendering', True)
        self.stroke_linecap = _str_enum(stroke_linecap, LINECAPS, 'stroke_linecap', True)
        self.stroke_linejoin = \
            _str_enum(stroke_linejoin, LINEJOINS, 'stroke_linejoin', True)
        self.stroke_miterlimit = _number(stroke_miterlimit, 'stroke_miterlimit', True)
        self.fill_rule = _str_enum(fill_rule, FILL_RULES, 'fill_rule', True)
        self.mask = _str(mask, 'mask', True)
        self.opacity = _number(opacity, 'opacity', True)
        self.clip_path = _str(clip_path, 'clip_path', True)
        self.overflow = _str_enum(overflow, OVERFLOWS, 'overflow', True)


class TSpan(Element, _TextElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/tspan
    """
    ALIGNMENTS = set(('baseline', 'top', 'before-edge', 'text-top',
                      'text-before-edge', 'middle', 'bottom',
                      'after-edge', 'text-bottom', 'text-after-edge', 'ideographic',
                      'lower', 'hanging', 'mathematical', 'inherit'))
    SHIFTS = set(('baseline', 'sub', 'super', 'inherit'))
    element_name = 'tspan'

    def __init__(self, externalResourcesRequired=None,
                 x=None, y=None, dx=None, dy=None, textLength=None, lengthAdjust=None,
                 writing_mode=None, alignment_baseline=None, baseline_shift=None,
                 stroke_linecap=None, stroke_linejoin=None, stroke_miterlimit=None,
                 fill_rule=None, opacity=None):
        super(Text, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.x = _number_or_length(x, 'x', True)
        self.y = _number_or_length(y, 'y', True)
        self.dx = _number_or_length(dx, 'width', True)
        self.dy = _number_or_length(dy, 'height', True)
        self.textLength = _number_or_length(textLength, 'rx', True)
        self.lengthAdjust = _str_enum(lengthAdjust, LENGTH_ADJUSTS, 'lengthAdjust', True)
        self.writing_mode = _str_enum(writing_mode, WRITING_MODES, 'writing_mode', True)
        self.alignment_baseline = \
            _str_enum(alignment_baseline, self.ALIGNMENTS, 'alignment_baseline', True)
        self.baseline_shift = \
            _str_enum(baseline_shift, self.SHIFTS, 'baseline_shift', True)
        self.stroke_linecap = _str_enum(stroke_linecap, LINECAPS, 'stroke_linecap', True)
        self.stroke_linejoin = \
            _str_enum(stroke_linejoin, LINEJOINS, 'stroke_linejoin', True)
        self.stroke_miterlimit = _number(stroke_miterlimit, 'stroke_miterlimit', True)
        self.fill_rule = _str_enum(fill_rule, FILL_RULES, 'fill_rule', True)
        self.opacity = _number(opacity, 'opacity', True)


class TextPath(Element, _TextElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath
    """
    METHODS = set(('align', 'stretch'))
    SPACINGS = set(('auto', 'exact'))
    SIDES = set(('left', 'right'))
    ALIGNMENTS = set(('baseline', 'top', 'before-edge', 'text-top',
                      'text-before-edge', 'middle', 'bottom',
                      'after-edge', 'text-bottom', 'text-after-edge', 'ideographic',
                      'lower', 'hanging', 'mathematical', 'inherit'))
    SHIFTS = set(('baseline', 'sub', 'super', 'inherit'))
    element_name = 'textPath'

    def __init__(self, externalResourcesRequired=None,
                 startOffset=None, textLength=None, lengthAdjust=None,
                 method=None, spacing=None, href=None, path=None, side=None,
                 writing_mode=None, alignment_baseline=None, baseline_shift=None,
                 stroke_linecap=None, stroke_linejoin=None, stroke_miterlimit=None,
                 fill_rule=None, opacity=None):
        super(TextPath, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.startOffset = _str(startOffset, 'startOffset', True)
        self.textLength = _number_or_length(textLength, 'rx', True)
        self.lengthAdjust = _str_enum(lengthAdjust, LENGTH_ADJUSTS, 'lengthAdjust', True)
        self.method = _str_enum(method, self.METHODS, 'method', True)
        self.spacing = _str_enum(spacing, self.SPACINGS, 'spacing', True)
        self.href = _str(href, 'href', True)
        self.path = _str(path, 'path', True)
        self.side = _str_enum(side, self.SIDES, 'side', True)
        self.writing_mode = _str_enum(writing_mode, WRITING_MODES, 'writing_mode', True)
        self.alignment_baseline = \
            _str_enum(alignment_baseline, self.ALIGNMENTS, 'alignment_baseline', True)
        self.baseline_shift = \
            _str_enum(baseline_shift, self.SHIFTS, 'baseline_shift', True)
        self.stroke_linecap = _str_enum(stroke_linecap, LINECAPS, 'stroke_linecap', True)
        self.stroke_linejoin = \
            _str_enum(stroke_linejoin, LINEJOINS, 'stroke_linejoin', True)
        self.stroke_miterlimit = _number(stroke_miterlimit, 'stroke_miterlimit', True)
        self.fill_rule = _str_enum(fill_rule, FILL_RULES, 'fill_rule', True)
        self.opacity = _number(opacity, 'opacity', True)


class Marker(Element, m.Color, m.GraphicsElementEvents, m.Graphics):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker
    """
    UNITS = set(('strokeWidth', 'userSpaceOnUse', 'userSpace'))
    element_name = 'marker'

    def __init__(self, externalResourcesRequired=None,
                 viewBox=None, preserveAspectRatio=None, refX=None, refY=None,
                 markerUnits=None, markerWidth=None, markerHeight=None, orient=None,
                 opacity=None, clip_path=None, class_=None, mask=None, overflow=None):
        super(Marker, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.viewBox = _obj(viewBox, ViewBoxSpec, 'viewBox', True)
        self.preserveAspectRatio = \
            _obj(preserveAspectRatio, PreserveAspectRatio, 'preserveAspectRatio', True)
        self.refX = _number_or_length(refX, 'refX', True)
        self.refY = _number_or_length(refY, 'refY', True)
        self.markerUnits = _str_enum(markerUnits, self.UNITS, 'markerUnits', True)
        self.markerWidth = _number_or_length(markerWidth, 'markerWidth', True)
        self.markerHeight = _number_or_length(markerHeight, 'markerHeight', True)
        self.orient = _str(orient, 'orient', True)
        self.opacity = _number(opacity, 'opacity', True)
        self.clip_path = _str(clip_path, 'clip_path', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.mask = _str(mask, 'mask', True)
        self.overflow = _str_enum(overflow, OVERFLOWS, 'overflow', True)


class _Gradient:
    UNITS = set(('userSpaceOnUse', 'objectBoundingBox'))
    SPREAD_METHODS = set(('pad', 'reflect', 'repeat'))

    def __init__(self, externalResourcesRequired=None,
                 gradientUnits=None, gradientTransform=None, spreadMethod=None,
                 href=None, class_=None):
        super(_Gradient, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.gradientUnits = _str_enum(gradientUnits, self.UNITS, 'gradientUnits', True)
        self.gradientTransform = \
            _list_of_objs(gradientTransform, Transform, 'gradientTransform', True)
        self.spreadMethod = _str_enum(spreadMethod, self.SPREAD_METHODS, 'spreadMethod', True)
        self.href = _str(href, 'href', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)


class LinearGradient(Element, _Gradient, m.Color, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/linearGradient
    """
    element_name = 'linearGradient'

    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        super(LinearGradient, self).__init__()
        self.x1 = _number_or_length(x1, 'x1', True)
        self.y1 = _number_or_length(y1, 'y1', True)
        self.x2 = _number_or_length(x2, 'x2', True)
        self.y2 = _number_or_length(y2, 'y2', True)


class RadialGradient(Element, _Gradient, m.Color, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/radialGradient
    """
    element_name = 'radialGradient'

    def __init__(self, cx=None, cy=None, r=None, fr=None, fx=None, fy=None):
        super(RadialGradient, self).__init__()
        self.cx = _number_or_length(cx, 'cx', True)
        self.cy = _number_or_length(cy, 'cy', True)
        self.r = _number_or_length(r, 'r', True)
        self.fr = _number_or_length(fr, 'fr', True)
        self.fx = _number_or_length(fx, 'fx', True)
        self.fy = _number_or_length(fy, 'fy', True)


class Stop(Element, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/stop
    """
    element_name = 'stop'

    def __init__(self, offset=None, stop_opacity=None, stop_color=None, class_=None):
        super(Stop, self).__init__()
        self.offset = _number_or_length(offset, 'offset', True)
        self.stop_opacity = _number(stop_opacity, 'stop_opacity', True)
        self.stop_color = _str(stop_color, 'stop_color', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)


class ClipPath(Element, m.Color, m.Graphics):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/clipPath
    """
    UNITS = set(('userSpaceOnUse', 'objectBoundingBox'))
    element_name = 'clipPath'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 clipPathUnits=None, class_=None, mask=None, clip_path=None):
        super(ClipPath, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.clipPathUnits = _str_enum(clipPathUnits, self.UNITS, 'clipPathUnits', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.mask = _str(mask, 'mask', True)
        self.clip_path = _str(clip_path, 'clip_path', True)


class Mask(Element, m.Color, m.Graphics):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/mask
    """
    UNITS = set(('userSpaceOnUse', 'objectBoundingBox'))
    element_name = 'mask'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 maskUnits=None, x=None, y=None, width=None, height=None,
                 maskContentUnits=None, class_=None, mask=None, clip_path=None):
        super(ClipPath, self).__init__()
        self.externalResourcesRequired = bool(externalResourcesRequired) \
            if externalResourcesRequired is not None else None
        self.transform = _list_of_objs(transform, Transform, 'transform', True)
        self.maskUnits = _str_enum(maskUnits, self.UNITS, 'maskUnits', True)
        self.x = _number_or_length(x, 'x', True)
        self.y = _number_or_length(y, 'y', True)
        self.width = _number_or_length(width, 'width', True)
        self.height = _number_or_length(height, 'height', True)
        self.maskContentUnits = \
            _str_enum(maskContentUnits, self.UNITS, 'maskContentUnits', True)
        self.class_ = _list_of_objs(class_, str, 'class_', True)
        self.mask = _str(mask, 'mask', True)
        self.clip_path = _str(clip_path, 'clip_path', True)
