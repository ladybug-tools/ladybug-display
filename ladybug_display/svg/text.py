"""SVG Text class."""
from ._transforms import Transform
from ._types import _number, _number_or_length, _str, _str_enum, _list_of_objs
from .element import Element, _TextElement, \
    LENGTH_ADJUSTS, WRITING_MODES, LINECAPS, LINEJOINS, FILL_RULES, OVERFLOWS


class Text(Element, _TextElement):
    """The SVG <text> element draws a graphics element consisting of text.

    It's possible to apply a gradient, pattern, clipping path, mask, or filter to <text>,
    like any other SVG graphics element.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/text
    """
    LENGTH_ADJUSTS = LENGTH_ADJUSTS
    WRITING_MODES = WRITING_MODES
    LINECAPS = LINECAPS
    LINEJOINS = LINEJOINS
    FILL_RULES = FILL_RULES
    OVERFLOWS = OVERFLOWS
    RENDERINGS = set(('auto', 'optimizeSpeed', 'optimizeLegibility', 'geometricPrecision'))
    element_name = 'text'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 x=None, y=None, dx=None, dy=None, textLength=None, lengthAdjust=None,
                 writing_mode=None, text_rendering=None, stroke_linecap=None,
                 stroke_linejoin=None, stroke_miterlimit=None, fill_rule=None,
                 mask=None, opacity=None, clip_path=None, overflow=None):
        super(Text, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.transform = transform
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.textLength = textLength
        self.lengthAdjust = lengthAdjust
        self.writing_mode = writing_mode
        self.text_rendering = text_rendering
        self.stroke_linecap = stroke_linecap
        self.stroke_linejoin = stroke_linejoin
        self.stroke_miterlimit = stroke_miterlimit
        self.fill_rule = fill_rule
        self.mask = mask
        self.opacity = opacity
        self.clip_path = clip_path
        self.overflow = overflow

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
    def dx(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/dx
        """
        return self._dx

    @dx.setter
    def dx(self, value):
        self._dx = _number_or_length(value, 'width', True)

    @property
    def dy(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/dy
        """
        return self._dy

    @dy.setter
    def dy(self, value):
        self._dy = _number_or_length(value, 'height', True)

    @property
    def textLength(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/textLength
        """
        return self._textLength

    @textLength.setter
    def textLength(self, value):
        self._textLength = _number_or_length(value, 'textLength', True)

    @property
    def lengthAdjust(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/lengthAdjust
        """
        return self._lengthAdjust

    @lengthAdjust.setter
    def lengthAdjust(self, value):
        self._lengthAdjust = _str_enum(value, LENGTH_ADJUSTS, 'lengthAdjust', True)

    @property
    def writing_mode(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/writing-mode
        """
        return self._writing_mode

    @writing_mode.setter
    def writing_mode(self, value):
        self._writing_mode = _str_enum(value, WRITING_MODES, 'writing_mode', True)

    @property
    def text_rendering(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-rendering
        """
        return self._text_rendering

    @text_rendering.setter
    def text_rendering(self, value):
        self._text_rendering = _str_enum(value, self.RENDERINGS, 'text_rendering', True)

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
