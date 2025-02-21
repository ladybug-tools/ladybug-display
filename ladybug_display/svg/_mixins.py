"""Base classes from which many SVG elements inherit properties."""
from ._types import Length, Number


class AttrsMixin:
    pass


class GraphicsElementEvents(AttrsMixin):
    __slots__ = ('onfocusin', 'onfocusout', 'onactivate', 'onclick',
                 'onmousedown', 'onmouseup', 'onmouseover', 'onmousemove',
                 'onmouseout', 'onload')

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


class Color(AttrsMixin):
    INTERPOLATIONS = set(('auto', 'sRGB', 'linearRGB', 'inherit'))
    __slots__ = ('value', 'unit')

    def __init__(self, color=None, color_interpolation=None):
        if color_interpolation is not None:
            assert color_interpolation in self.INTERPOLATIONS, \
                'Got "{}" for color_interpolation. Must be one of the ' \
                'following {}.'.format(color_interpolation, self.INTERPOLATIONS)
        self.color = color
        self.color_interpolation = color_interpolation


class FillStroke(AttrsMixin):
    __slots__ = ('stroke', 'stroke_dasharray', 'stroke_dashoffset',
                 'stroke_opacity', 'stroke_width')

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
        if stroke_dashoffset is not None and stroke_dashoffset != 'none':
            assert isinstance(stroke_dashoffset, (Length, Number)), \
                'Expected length or number for stroke_dashoffset. ' \
                'Got {}.'.format(type(stroke_dashoffset))
        if stroke_opacity is not None:
            assert isinstance(stroke_opacity, Number), 'Expected number for ' \
                'stroke_opacity. Got {}.'.format(type(stroke_opacity))
        if stroke_width is not None:
            assert isinstance(stroke_width, (Length, Number)), 'Expected length or ' \
                'number for stroke_width. Got {}.'.format(type(stroke_opacity))
        self.stroke = stroke
        self.stroke_dasharray = stroke_dasharray
        self.stroke_dashoffset = stroke_dashoffset
        self.stroke_opacity = stroke_opacity
        self.stroke_width = stroke_width


class FontSpecification(AttrsMixin):
    STRETCHES = set(('normal', 'wider', 'narrower',
                     'ultra-condensed', 'extra-condensed', 'semi-condensed',
                     'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded',
                     'inherit'))
    STYLES = set(('normal', 'italic', 'oblique', 'inherit'))
    VARIANTS = set(('normal', 'small-caps', 'inherit'))
    WEIGHTS = set(('normal', 'bold', 'bolder', 'lighter', 'inherit',
                  '100', '200', '300', '400', '500', '600', '700', '800', '900'))
    __slots__ = (('font_family', 'font_size', 'font_size_adjust', 'font_stretch',
                 'font_style', 'font_variant', 'font_weight'))

    def __init__(self, font_family=None, font_size=None, font_size_adjust=None,
                 font_stretch=None, font_style=None, font_variant=None,
                 font_weight=None):
        if font_size is not None:
            assert isinstance(font_size, (Length, Number)), 'Expected length or ' \
                'number for font_size. Got {}.'.format(type(font_size))
        if font_size_adjust is not None and font_size_adjust != 'none':
            assert isinstance(font_size_adjust, Number), 'Expected number for ' \
                'font_size_adjust. Got {}.'.format(type(font_size_adjust))
        if font_stretch is not None:
            assert font_stretch in self.STRETCHES, 'Got "{}" for font_stretch. Must ' \
                'be one of the following {}.'.format(font_stretch, self.STRETCHES)
        if font_style is not None:
            assert font_style in self.STYLES, 'Got "{}" for font_style. Must ' \
                'be one of the following {}.'.format(font_style, self.STYLES)
        if font_variant is not None:
            assert font_variant in self.VARIANTS, 'Got "{}" for font_variant. Must ' \
                'be one of the following {}.'.format(font_variant, self.VARIANTS)
        if font_weight is not None:
            assert font_weight in self.WEIGHTS, 'Got "{}" for font_weight. Must ' \
                'be one of the following {}.'.format(font_weight, self.WEIGHTS)
        self.font_family = font_family
        self.font_size = font_size
        self.font_size_adjust = font_size_adjust
        self.font_stretch = font_stretch
        self.font_style = font_style
        self.font_variant = font_variant
        self.font_weight = font_weight


class Graphics(AttrsMixin):
    RULES = set(('evenodd', 'nonzero', 'inherit'))
    CURSORS = set(('auto', 'crosshair', 'default', 'pointer', 'move',
                   'e-resize', 'ne-resize', 'nw-resize', 'n-resize',
                   'se-resize', 'sw-resize', 's-resize', 'w-resize',
                   'text', 'wait', 'help', 'inherit'))
    EVENTS = set(('bounding-box', 'visiblePainted', 'visibleFill', 'visibleStroke',
                  'visible', 'painted', 'fill', 'stroke', 'all', 'none'))
    __slots__ = ('clip_rule', 'cursor', 'display', 'filter', 'pointer_events')

    def __init__(self, clip_rule=None, cursor=None, display=None, filter=None,
                 pointer_events=None):
        if clip_rule is not None:
            assert clip_rule in self.RULES, 'Got "{}" for clip_rule. Must ' \
                'be one of the following {}.'.format(clip_rule, self.RULES)
        if cursor is not None:
            assert cursor in self.CURSORS, 'Got "{}" for cursor. Must ' \
                'be one of the following {}.'.format(cursor, self.CURSORS)
        if pointer_events is not None:
            assert pointer_events in self.EVENTS, 'Got "{}" for pointer_events. Must ' \
                'be one of the following {}.'.format(cursor, self.EVENTS)
        self.clip_rule = clip_rule
        self.cursor = cursor
        self.display = display
        self.filter = filter
        self.pointer_events = pointer_events


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
    __slots__ = ('direction', 'dominant_baseline', 'letter_spacing', 'text_anchor',
                 'text_decoration', 'unicode_bidi', 'word_spacing')

    def __init__(self, direction=None, dominant_baseline=None, letter_spacing=None,
                 text_anchor=None, text_decoration=None, unicode_bidi=None,
                 word_spacing=None):
        if direction is not None:
            assert direction in self.DIRECTIONS, 'Got "{}" for direction. Must ' \
                'be one of the following {}.'.format(direction, self.DIRECTIONS)
        if dominant_baseline is not None:
            assert dominant_baseline in self.BASELINES, 'Got "{}" for ' \
                'dominant_baseline. Must be one of the following {}.'.format(
                    dominant_baseline, self.BASELINES)
        if letter_spacing is not None:
            assert letter_spacing in self.SPACINGS, 'Got "{}" for letter_spacing. ' \
                'Must be one of the following {}.'.format(letter_spacing, self.SPACINGS)
        if text_anchor is not None:
            assert text_anchor in self.ANCHORS, 'Got "{}" for text_anchor. ' \
                'Must be one of the following {}.'.format(text_anchor, self.ANCHORS)
        if text_decoration is not None:
            assert text_decoration in self.DECORATIONS, 'Got "{}" for text_decoration. ' \
                'Must be one of the following {}.'.format(
                    text_decoration, self.DECORATIONS)
        if unicode_bidi is not None:
            assert unicode_bidi in self.BIDIS, 'Got "{}" for unicode_bidi. ' \
                'Must be one of the following {}.'.format(unicode_bidi, self.BIDIS)
        if word_spacing is not None:
            assert word_spacing in self.SPACINGS, 'Got "{}" for word_spacing. ' \
                'Must be one of the following {}.'.format(word_spacing, self.SPACINGS)
        self.direction = direction
        self.dominant_baseline = dominant_baseline
        self.letter_spacing = letter_spacing
        self.text_anchor = text_anchor
        self.text_decoration = text_decoration
        self.unicode_bidi = unicode_bidi
        self.word_spacing = word_spacing


class FilterPrimitive(AttrsMixin):
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        assert isinstance(x, (Length, Number)), \
            'Expected number for min_x. Got {}.'.format(type(x))
        assert isinstance(y, (Length, Number)), \
            'Expected number for min_y. Got {}.'.format(type(y))
        self.x = x
        self.y = y


class ComponentTransferFunction(AttrsMixin):
    TYPES = set(('identity', 'table', 'discrete', 'linear', 'gamma'))
    __slots__ = ('type', 'tableValues', 'intercept', 'amplitude',
                 'exponent', 'offset')

    def __init__(self, type, tableValues=None, intercept=None,
                 amplitude=None, exponent=None, offset=None):
        if type is not None:
            assert type in self.TYPES, 'Got "{}" for type. ' \
                'Must be one of the following {}.'.format(type, self.TYPES)
        if intercept is not None:
            assert isinstance(intercept, float), \
                'Expected float for intercept. Got {}.'.format(type(intercept))
        if amplitude is not None:
            assert isinstance(amplitude, float), \
                'Expected float for amplitude. Got {}.'.format(type(amplitude))
        if exponent is not None:
            assert isinstance(exponent, float), \
                'Expected float for exponent. Got {}.'.format(type(exponent))
        if offset is not None:
            assert isinstance(offset, float), \
                'Expected float for offset. Got {}.'.format(type(offset))
        self.type = type
        self.tableValues = tableValues
        self.intercept = intercept
        self.amplitude = amplitude
        self.exponent = exponent
        self.offset = offset
