"""SVG TextPath class."""
from ._types import _number, _number_or_length, _str, _str_enum
from .element import Element, _TextElement, \
    LENGTH_ADJUSTS, WRITING_MODES, LINECAPS, LINEJOINS, FILL_RULES


class TextPath(Element, _TextElement):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/textPath
    """
    LENGTH_ADJUSTS = LENGTH_ADJUSTS
    WRITING_MODES = WRITING_MODES
    LINECAPS = LINECAPS
    LINEJOINS = LINEJOINS
    FILL_RULES = FILL_RULES
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
        self.externalResourcesRequired = externalResourcesRequired
        self.startOffset = startOffset
        self.textLength = textLength
        self.lengthAdjust = lengthAdjust
        self.method = method
        self.spacing = spacing
        self.href = href
        self.path = path
        self.side = side
        self.writing_mode = writing_mode
        self.alignment_baseline = alignment_baseline
        self.baseline_shift = baseline_shift
        self.stroke_linecap = stroke_linecap
        self.stroke_linejoin = stroke_linejoin
        self.stroke_miterlimit = stroke_miterlimit
        self.fill_rule = fill_rule
        self.opacity = opacity

    @property
    def externalResourcesRequired(self):
        """[bool]"""
        return self._externalResourcesRequired

    @externalResourcesRequired.setter
    def externalResourcesRequired(self, value):
        self._externalResourcesRequired = bool(value) if value is not None else None

    @property
    def startOffset(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/startOffset
        """
        return self._startOffset

    @startOffset.setter
    def startOffset(self, value):
        self._startOffset = _str(value, 'startOffset', True)

    @property
    def textLength(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/textLength
        """
        return self._textLength

    @textLength.setter
    def textLength(self, value):
        self._textLength = _number_or_length(value, 'rx', True)

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
    def method(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/method
        """
        return self._method

    @method.setter
    def method(self, value):
        self._method = _str_enum(value, self.METHODS, 'method', True)

    @property
    def spacing(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/spacing
        """
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self._spacing = _str_enum(value, self.SPACINGS, 'spacing', True)

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
    def path(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/path
        """
        return self._path

    @path.setter
    def path(self, value):
        self._path = _str(value, 'path', True)

    @property
    def side(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/side
        """
        return self._side

    @side.setter
    def side(self, value):
        self._side = _str_enum(value, self.SIDES, 'side', True)

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
    def alignment_baseline(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/alignment-baseline
        """
        return self._alignment_baseline

    @alignment_baseline.setter
    def alignment_baseline(self, value):
        self._alignment_baseline = \
            _str_enum(value, self.ALIGNMENTS, 'alignment_baseline', True)

    @property
    def baseline_shift(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/baseline-shift
        """
        return self._baseline_shift

    @baseline_shift.setter
    def baseline_shift(self, value):
        self._baseline_shift = _str_enum(value, self.SHIFTS, 'baseline_shift', True)

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
    def opacity(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/opacity
        """
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = _number(value, 'opacity', True)
