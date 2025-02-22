"""Classes for special types relating to SVG."""
Number = (float, int)


class Length(object):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Content_type#length
    """
    UNITS = set(('em', 'ex', 'px', 'pt', 'pc', 'cm', 'mm', 'in', '%'))
    __slots__ = ('value', 'unit')

    def __init__(self, value, unit):
        self.value = _number(value, 'value')
        self.unit = _str_enum(unit, self.UNITS, 'units')

    @classmethod
    def from_str(cls, length_str):
        """Initialize Length from a length string."""
        for unit in cls.UNITS:
            if length_str.endswith(unit):
                return cls(float(length_str.replace(length_str, '')), unit)

    def __str__(self):
        return '{}{}'.format(self.value, self.unit)


class PreserveAspectRatio(object):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/preserveAspectRatio
    """
    ALIGNMENTS = set(('none', 'xMinYMin', 'xMidYMin', 'xMaxYMin', 'xMinYMid',
                      'xMidYMid', 'xMaxYMid', 'xMinYMax', 'xMidYMax', 'xMaxYMax'))
    SCALE_TYPES = set(('meet', 'slice'))
    __slots__ = ('alignment', 'scale_type')

    def __init__(self, alignment='xMidYMid', scale_type='meet'):
        self.alignment = _str_enum(alignment, self.ALIGNMENTS, 'alignment')
        self.scale_type = _str_enum(scale_type, self.SCALE_TYPES, 'scale_type')

    def __str__(self):
        return '{} {}'.format(self.alignment, self.scale_type)


class ViewBoxSpec(object):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox
    """
    __slots__ = ('min_x', 'min_y', 'width', 'height')

    def __init__(self, min_x, min_y, width, height):
        self.min_x = _number(min_x, 'min_x')
        self.min_y = _number(min_y, 'min_y')
        self.width = _number(width, 'width')
        self.height = _number(height, 'height')

    def __str__(self):
        return '{} {} {} {}'.format(self.min_x, self.min_y, self.width, self.height)


def _float(value, input_name='', accept_none=False, accept_str_none=False):
    """Check if value is a float."""
    if accept_none:
        if value is None:
            return value
        elif accept_str_none and value == 'none':
            return value
    if not isinstance(value, float):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise TypeError('Input {} must be a float. Got {}: {}.'.format(
                input_name, type(value), value))
    return value


def _int(value, input_name='', accept_none=False, accept_str_none=False):
    """Check if value is a int."""
    if accept_none:
        if value is None:
            return value
        elif accept_str_none and value == 'none':
            return value
    if not isinstance(value, int):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise TypeError('Input {} must be a int. Got {}: {}.'.format(
                input_name, type(value), value))
    return value


def _number(value, input_name='', accept_none=False, accept_str_none=False):
    """Check if value is a Number."""
    if accept_none:
        if value is None:
            return value
        elif accept_str_none and value == 'none':
            return value
    if not isinstance(value, Number):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise TypeError('Input {} must be a number. Got {}: {}.'.format(
                input_name, type(value), value))
    return value


def _length(value, input_name='', accept_none=False, accept_str_none=False):
    """Check if value is a Length."""
    if accept_none:
        if value is None:
            return value
        elif accept_str_none and value == 'none':
            return value
    if not isinstance(value, Length):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise TypeError('Input {} must be a length. Got {}: {}.'.format(
                input_name, type(value), value))
    return value


def _number_or_length(value, input_name='', accept_none=False, accept_str_none=False):
    """Check if value is a Length or Number."""
    if accept_none:
        if value is None:
            return value
        elif accept_str_none and value == 'none':
            return value
    if not isinstance(value, (Length, Number)):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise TypeError('Input {} must be a length or number. Got {}: {}.'.format(
                input_name, type(value), value))
    return value


def _str_enum(value, enumeration_set, input_name='', accept_none=False):
    """Check if a value is a string in a particular enumeration_set."""
    if accept_none and value is None:
        return value
    assert value in enumeration_set, 'Got "{}" for {}. Must be one of ' \
        'the following {}.'.format(value, input_name, enumeration_set)
    return value


def _str(value, input_name='', accept_none=False):
    """Check if a value is a string."""
    if accept_none and value is None:
        return value
    if not isinstance(value, str):
        try:
            value = str(value)
        except (ValueError, TypeError):
            raise TypeError('Input {} must be a string. Got {}: {}.'.format(
                input_name, type(value), value))
    return value


def _obj(value, obj_class, input_name='', accept_none=False):
    """Check if a value is a list of a certain a certain obj_class."""
    if accept_none and value is None:
        return value
    assert isinstance(value, obj_class), 'Input {} must be a {}. ' \
        'Got {}.'.format(input_name, obj_class.__name__, type(value))
    return value


def _list_of_objs(value, obj_class, input_name='', accept_none=False):
    """Check if a value is a list of a certain a certain obj_class."""
    if accept_none and value is None:
        return value
    assert isinstance(value, list), 'Input {} must be a list. Got {}.'.format(
        input_name, type(value))
    for val in value:
        assert isinstance(val, obj_class), 'Input {} must be a list of {}. ' \
            'Got list of {}.'.format(input_name, obj_class.__name__, type(val))
    return value


def _dict(value, input_name='', accept_none=False):
    """Check if a value is a dict."""
    if accept_none and value is None:
        return value
    assert isinstance(value, dict), \
        'Input {} must be a dict. Got {}: {}.'.format(input_name, type(value), value)
    return value
