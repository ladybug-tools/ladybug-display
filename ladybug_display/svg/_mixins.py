# coding=utf-8
"""Base classes from which many SVG elements inherit properties."""
from ._types import Length, Number, _number, _number_or_length, _str_enum, _str


class AttrsMixin:
    pass


class GraphicsElementEvents(AttrsMixin):

    def __init__(self, onfocusin=None, onfocusout=None, onactivate=None, onclick=None,
                 onmousedown=None, onmouseup=None, onmouseover=None, onmousemove=None,
                 onmouseout=None, onload=None):
        self.onfocusin = onfocusin
        self.onfocusout = onfocusout
        self.onactivate = onactivate
        self.onclick = onclick
        self.onmousedown = onmousedown
        self.onmouseup = onmouseup
        self.onmouseover = onmouseover
        self.onmousemove = onmousemove
        self.onmouseout = onmouseout
        self.onload = onload

    @property
    def onfocusin(self):
        """[str]"""
        return self._onfocusin

    @onfocusin.setter
    def onfocusin(self, value):
        self._onfocusin = _str(value, 'onfocusin', True)

    @property
    def onfocusout(self):
        """[str]"""
        return self._onfocusout

    @onfocusout.setter
    def onfocusout(self, value):
        self._onfocusout = _str(value, 'onfocusout', True)

    @property
    def onactivate(self):
        """[str]"""
        return self._onactivate

    @onactivate.setter
    def onactivate(self, value):
        self._onactivate = _str(value, 'onactivate', True)

    @property
    def onclick(self):
        """[str]"""
        return self._onclick

    @onclick.setter
    def onclick(self, value):
        self._onclick = _str(value, 'onclick', True)

    @property
    def onmousedown(self):
        """[str]"""
        return self._onmousedown

    @onmousedown.setter
    def onmousedown(self, value):
        self._onmousedown = _str(value, 'onmousedown', True)

    @property
    def onmouseup(self):
        """[str]"""
        return self._onmouseup

    @onmouseup.setter
    def onmouseup(self, value):
        self._onmouseup = _str(value, 'onmouseup', True)

    @property
    def onmouseover(self):
        """[str]"""
        return self._onmouseover

    @onmouseover.setter
    def onmouseover(self, value):
        self._onmouseover = _str(value, 'onmouseover', True)

    @property
    def onmousemove(self):
        """[str]"""
        return self._onmousemove

    @onmousemove.setter
    def onmousemove(self, value):
        self._onmousemove = _str(value, 'onmousemove', True)

    @property
    def onmouseout(self):
        """[str]"""
        return self._onmouseout

    @onmouseout.setter
    def onmouseout(self, value):
        self._onmouseout = _str(value, 'onmouseout', True)

    @property
    def onload(self):
        """[str]"""
        return self._onload

    @onload.setter
    def onload(self, value):
        self._onload = _str(value, 'onload', True)


class Color(AttrsMixin):
    INTERPOLATIONS = set(('auto', 'sRGB', 'linearRGB', 'inherit'))

    def __init__(self, color=None, color_interpolation=None):
        self.color = color
        self.color_interpolation = color_interpolation

    @property
    def color(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/color
        """
        return self._color

    @color.setter
    def color(self, value):
        self._color = _str(value, 'color', True)

    @property
    def color_interpolation(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/color-interpolation
        """
        return self._color_interpolation

    @color_interpolation.setter
    def color_interpolation(self, value):
        self._color_interpolation = _str_enum(
            value, self.INTERPOLATIONS, 'color_interpolation', True)


class FillStroke(AttrsMixin):

    def __init__(self, stroke=None, stroke_dasharray=None, stroke_dashoffset=None,
                 stroke_opacity=None, stroke_width=None):
        self.stroke_dasharray = stroke_dasharray
        self.stroke = stroke
        self.stroke_dashoffset = stroke_dashoffset
        self.stroke_opacity = stroke_opacity
        self.stroke_width = stroke_width

    @property
    def stroke_dasharray(self):
        """[list of numbers]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dasharray
        """
        return self._stroke_dasharray

    @stroke_dasharray.setter
    def stroke_dasharray(self, value):
        if value is not None and value != 'none' \
                and not isinstance(value, Length):
            assert isinstance(value, list), \
                'Expected length or list of numbers for stroke_dasharray. ' \
                'Got {}.'.format(type(value))
            for val in value:
                assert isinstance(val, Number), \
                    'Expected length or list of numbers for stroke_dasharray. ' \
                    'Got {}.'.format(type(val))
        self._stroke_dasharray = value

    @property
    def stroke(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke
        """
        return self._stroke

    @stroke.setter
    def stroke(self, value):
        self._stroke = _str(value, 'stroke', True)

    @property
    def stroke_dashoffset(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dashoffset
        """
        return self._stroke_dashoffset

    @stroke_dashoffset.setter
    def stroke_dashoffset(self, value):
        self._stroke_dashoffset = _number_or_length(value, 'stroke_dashoffset', True, True)

    @property
    def stroke_opacity(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-opacity
        """
        return self._stroke_opacity

    @stroke_opacity.setter
    def stroke_opacity(self, value):
        self._stroke_opacity = _number(value, 'stroke_opacity', True)

    @property
    def stroke_width(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-width
        """
        return self._stroke_width

    @stroke_width.setter
    def stroke_width(self, value):
        self._stroke_width = _number_or_length(value, 'stroke_width', True)


class FontSpecification(AttrsMixin):
    STRETCHES = set(('normal', 'wider', 'narrower',
                     'ultra-condensed', 'extra-condensed', 'semi-condensed',
                     'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded',
                     'inherit'))
    STYLES = set(('normal', 'italic', 'oblique', 'inherit'))
    VARIANTS = set(('normal', 'small-caps', 'inherit'))
    WEIGHTS = set(('normal', 'bold', 'bolder', 'lighter', 'inherit',
                  '100', '200', '300', '400', '500', '600', '700', '800', '900'))

    def __init__(self, font_family=None, font_size=None, font_size_adjust=None,
                 font_stretch=None, font_style=None, font_variant=None,
                 font_weight=None):
        self.font_family = font_family
        self.font_size = font_size
        self.font_size_adjust = font_size_adjust
        self.font_stretch = font_stretch
        self.font_style = font_style
        self.font_variant = font_variant
        self.font_weight = font_weight

    @property
    def font_family(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-family
        """
        return self._font_family

    @font_family.setter
    def font_family(self, value):
        self._font_family = _str(value, 'font_family', True)

    @property
    def font_size(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-size
        """
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = _number_or_length(value, 'font_size', True)

    @property
    def font_size_adjust(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-size-adjust
        """
        return self._font_size_adjust

    @font_size_adjust.setter
    def font_size_adjust(self, value):
        self._font_size_adjust = _number(value, 'font_size_adjust', True, True)

    @property
    def font_stretch(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-stretch
        """
        return self._font_stretch

    @font_stretch.setter
    def font_stretch(self, value):
        self._font_stretch = _str_enum(value, self.STRETCHES, 'font_stretch', True)

    @property
    def font_style(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-style
        """
        return self._font_style

    @font_style.setter
    def font_style(self, value):
        self._font_style = _str_enum(value, self.STYLES, 'font_style', True)

    @property
    def font_variant(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-variant
        """
        return self._font_variant

    @font_variant.setter
    def font_variant(self, value):
        self._font_variant = _str_enum(value, self.VARIANTS, 'font_variant', True)

    @property
    def font_weight(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/font-weight
        """
        return self._font_weight

    @font_weight.setter
    def font_weight(self, value):
        self._font_weight = _str_enum(value, self.WEIGHTS, 'font_weight', True)


class Graphics(AttrsMixin):
    RULES = set(('evenodd', 'nonzero', 'inherit'))
    CURSORS = set(('auto', 'crosshair', 'default', 'pointer', 'move',
                   'e-resize', 'ne-resize', 'nw-resize', 'n-resize',
                   'se-resize', 'sw-resize', 's-resize', 'w-resize',
                   'text', 'wait', 'help', 'inherit'))
    EVENTS = set(('bounding-box', 'visiblePainted', 'visibleFill', 'visibleStroke',
                  'visible', 'painted', 'fill', 'stroke', 'all', 'none'))

    def __init__(self, clip_rule=None, cursor=None, display=None, filter=None,
                 pointer_events=None):
        self.clip_rule = clip_rule
        self.cursor = cursor
        self.display = display
        self.filter = filter
        self.pointer_events = pointer_events

    @property
    def clip_rule(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/clip-rule
        """
        return self._clip_rule

    @clip_rule.setter
    def clip_rule(self, value):
        self._clip_rule = _str_enum(value, self.RULES, 'clip_rule', True)

    @property
    def cursor(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/cursor
        """
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = _str_enum(value, self.CURSORS, 'cursor', True)

    @property
    def display(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/display
        """
        return self._display

    @display.setter
    def display(self, value):
        self._display = _str(value, 'display', True)

    @property
    def filter(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/filter
        """
        return self._filter

    @filter.setter
    def filter(self, value):
        self._filter = _str(value, 'filter', True)

    @property
    def pointer_events(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/pointer-events
        """
        return self._pointer_events

    @pointer_events.setter
    def pointer_events(self, value):
        self._pointer_events = _str_enum(value, self.EVENTS, 'pointer_events', True)


class TextContentElements(AttrsMixin):
    DIRECTIONS = set(('ltr', 'rtl', 'inherit'))
    BASELINES = set(('auto', 'autosense-script', 'no-change', 'reset', 'ideographic',
                     'lower', 'hanging', 'mathematical', 'inherit',
                     'text-bottom', 'alphabetic', 'middle', 'central', 'text-top'))
    SPACINGS = set(('auto', 'exact'))
    ANCHORS = set(('start', 'middle', 'end', 'inherit'))
    DECORATIONS = set(('none', 'underline', 'overline', 'line-through'))
    BIDIS = set(('normal', 'embed', 'isolate', 'bidi-override', 'isolate-override',
                 'plaintext'))

    def __init__(self, direction=None, dominant_baseline=None, letter_spacing=None,
                 text_anchor=None, text_decoration=None, unicode_bidi=None,
                 word_spacing=None):
        self.direction = direction
        self.dominant_baseline = dominant_baseline
        self.letter_spacing = letter_spacing
        self.text_anchor = text_anchor
        self.text_decoration = text_decoration
        self.unicode_bidi = unicode_bidi
        self.word_spacing = word_spacing

    @property
    def direction(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/direction
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = _str_enum(value, self.DIRECTIONS, 'direction', True)

    @property
    def dominant_baseline(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/dominant-baseline
        """
        return self._dominant_baseline

    @dominant_baseline.setter
    def dominant_baseline(self, value):
        self._dominant_baseline = _str_enum(value, self.BASELINES, 'dominant_baseline', True)

    @property
    def letter_spacing(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/letter-spacing
        """
        return self._letter_spacing

    @letter_spacing.setter
    def letter_spacing(self, value):
        self._letter_spacing = _str_enum(value, self.SPACINGS, 'letter_spacing', True)

    @property
    def text_anchor(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-anchor
        """
        return self._text_anchor

    @text_anchor.setter
    def text_anchor(self, value):
        self._text_anchor = _str_enum(value, self.ANCHORS, 'text_anchor', True)

    @property
    def text_decoration(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-decoration
        """
        return self._text_decoration

    @text_decoration.setter
    def text_decoration(self, value):
        self._text_decoration = _str_enum(value, self.DECORATIONS, 'text_decoration', True)

    @property
    def unicode_bidi(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/unicode-bidi
        """
        return self._unicode_bidi

    @unicode_bidi.setter
    def unicode_bidi(self, value):
        self._unicode_bidi = _str_enum(value, self.BIDIS, 'unicode_bidi', True)

    @property
    def word_spacing(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/word-spacing
        """
        return self._word_spacing

    @word_spacing.setter
    def word_spacing(self, value):
        self._word_spacing = _str_enum(value, self.SPACINGS, 'word_spacing', True)
