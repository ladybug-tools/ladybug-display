"""Classes for special types relating to SVG."""
Number = (float, int)


class Length(object):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Content_type#length
    """
    UNITS = set(('em', 'ex', 'px', 'pt', 'pc', 'cm', 'mm', 'in', '%'))
    __slots__ = ('value', 'unit')

    def __init__(self, value, unit):
        assert isinstance(value, Number), \
            'Expected number for value. Got {}.'.format(type(value))
        assert unit in self.UNITS, \
            'Got "{}" for units. Must be one of the following {}.'.format(unit, self.UNITS)
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return f'{self.value}{self.unit}'


class PreserveAspectRatio(object):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/preserveAspectRatio
    """
    ALIGNMENTS = set(('none', 'xMinYMin', 'xMidYMin', 'xMaxYMin', 'xMinYMid',
                      'xMidYMid', 'xMaxYMid', 'xMinYMax', 'xMidYMax', 'xMaxYMax'))
    SCALE_TYPES = set(('meet', 'slice'))
    __slots__ = ('alignment', 'scale_type')

    def __init__(self, alignment='xMidYMid', scale_type='meet'):
        assert alignment in self.ALIGNMENTS, 'Got "{}" for alignment. Must be one of ' \
            'the following {}.'.format(alignment, self.ALIGNMENTS)
        assert scale_type in self.SCALE_TYPES, 'Got "{}" for scale_type. Must be one ' \
            'of the following {}.'.format(scale_type, self.SCALE_TYPES)
        self.alignment = alignment
        self.scale_type = scale_type

    def __str__(self) -> str:
        return f'{self.alignment} {self.scale_type}'


class ViewBoxSpec(object):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox
    """
    __slots__ = ('min_x', 'min_y', 'width', 'height')

    def __init__(self, min_x, min_y, width, height):
        assert isinstance(min_x, Number), \
            'Expected number for min_x. Got {}.'.format(type(min_x))
        assert isinstance(min_y, Number), \
            'Expected number for min_y. Got {}.'.format(type(min_y))
        assert isinstance(width, Number), \
            'Expected number for width. Got {}.'.format(type(width))
        assert isinstance(height, Number), \
            'Expected number for height. Got {}.'.format(type(height))
        self.min_x = min_x
        self.min_y = min_y
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f'{self.min_x} {self.min_y} {self.width} {self.height}'
