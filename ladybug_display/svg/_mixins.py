"""Base classes from which many SVG elements inherit properties."""
from ._types import Length, Number, _float, _number, _number_or_length, _str_enum, _str


class AttrsMixin:
    pass


class GraphicsElementEvents(AttrsMixin):

    def __init__(self, onfocusin=None, onfocusout=None, onactivate=None, onclick=None,
                 onmousedown=None, onmouseup=None, onmouseover=None, onmousemove=None,
                 onmouseout=None, onload=None):
        self.onfocusin = _str(onfocusin, 'onfocusin', True)
        self.onfocusout = _str(onfocusout, 'onfocusout', True)
        self.onactivate = _str(onactivate, 'onactivate', True)
        self.onclick = _str(onclick, 'onclick', True)
        self.onmousedown = _str(onmousedown, 'onmousedown', True)
        self.onmouseup = _str(onmouseup, 'onmouseup', True)
        self.onmouseover = _str(onmouseover, 'onmouseover', True)
        self.onmousemove = _str(onmousemove, 'onmousemove', True)
        self.onmouseout = _str(onmouseout, 'onmouseout', True)
        self.onload = _str(onload, 'onload', True)


class Color(AttrsMixin):
    INTERPOLATIONS = set(('auto', 'sRGB', 'linearRGB', 'inherit'))

    def __init__(self, color=None, color_interpolation=None):
        self.color = _str(color, 'color', True)
        self.color_interpolation = _str_enum(
            color_interpolation, self.INTERPOLATIONS, 'color_interpolation', True)


class FillStroke(AttrsMixin):

    def __init__(self, stroke=None, stroke_dasharray=None, stroke_dashoffset=None,
                 stroke_opacity=None, stroke_width=None):
        if stroke_dasharray is not None and stroke_dasharray != 'none' \
                and not isinstance(stroke_dasharray, Length):
            assert isinstance(stroke_dasharray, list), \
                'Expected length or list of numbers for stroke_dasharray. ' \
                'Got {}.'.format(type(stroke_dasharray))
            for val in stroke_dasharray:
                assert isinstance(val, Number), \
                    'Expected length or list of numbers for stroke_dasharray. ' \
                    'Got {}.'.format(type(stroke_dasharray))
        self.stroke = _str(stroke, 'stroke', True)
        self.stroke_dasharray = stroke_dasharray
        self.stroke_dashoffset = _number_or_length(
            stroke_dashoffset, 'stroke_dashoffset', True, True)
        self.stroke_opacity = _number(stroke_opacity, 'stroke_opacity', True)
        self.stroke_width = _number_or_length(stroke_width, 'stroke_width', True)


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
        self.font_family = _str(font_family, 'font_family', True)
        self.font_size = _number_or_length(font_size, 'font_size', True)
        self.font_size_adjust = _number(font_size_adjust, 'font_size_adjust', True, True)
        self.font_stretch = _str_enum(font_stretch, self.STRETCHES, 'font_stretch', True)
        self.font_style = _str_enum(font_style, self.STYLES, 'font_style', True)
        self.font_variant = _str_enum(font_variant, self.VARIANTS, 'font_variant', True)
        self.font_weight = _str_enum(font_weight, self.WEIGHTS, 'font_weight', True)


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
        self.clip_rule = _str_enum(clip_rule, self.RULES, 'clip_rule', True)
        self.cursor = _str_enum(cursor, self.CURSORS, 'cursor', True)
        self.display = _str(display, 'display', True)
        self.filter = _str(filter, 'filter', True)
        self.pointer_events = _str_enum(
            pointer_events, self.EVENTS, 'pointer_events', True)


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
        self.direction = _str_enum(direction, self.DIRECTIONS, 'direction', True)
        self.dominant_baseline = _str_enum(
            dominant_baseline, self.BASELINES, 'dominant_baseline', True)
        self.letter_spacing = _str_enum(
            letter_spacing, self.SPACINGS, 'letter_spacing', True)
        self.text_anchor = _str_enum(text_anchor, self.ANCHORS, 'text_anchor', True)
        self.text_decoration = _str_enum(
            text_decoration, self.DECORATIONS, 'text_decoration', True)
        self.unicode_bidi = _str_enum(unicode_bidi, self.BIDIS, 'unicode_bidi', True)
        self.word_spacing = _str_enum(word_spacing, self.SPACINGS, 'word_spacing', True)


class FilterPrimitive(AttrsMixin):

    def __init__(self, x, y):
        self.x = _number_or_length(x, 'x')
        self.y = _number_or_length(y, 'y')


class ComponentTransferFunction(AttrsMixin):
    TYPES = set(('identity', 'table', 'discrete', 'linear', 'gamma'))

    def __init__(self, type, tableValues=None, intercept=None,
                 amplitude=None, exponent=None, offset=None):
        self.type = _str_enum(type, self.TYPES, 'type', True)
        self.tableValues = _str(tableValues, 'tableValues', True)
        self.intercept = _float(intercept, 'intercept', True)
        self.amplitude = _float(amplitude, 'amplitude', True)
        self.exponent = _float(exponent, 'exponent', True)
        self.offset = _float(offset, 'offset', True)
