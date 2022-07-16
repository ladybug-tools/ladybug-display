"""Collection of methods for type input checking."""
import math

try:
    INFPOS = math.inf
    INFNEG = -1 * math.inf
except AttributeError:
    # python 2
    INFPOS = float('inf')
    INFNEG = float('-inf')


def _number_check(value, input_name):
    """Check if value is a number."""
    try:
        number = float(value)
    except (ValueError, TypeError):
        raise TypeError('Input {} must be a number. Got {}: {}.'.format(
            input_name, type(value), value))
    return number


def float_in_range(value, mi=INFNEG, ma=INFPOS, input_name=''):
    """Check a float value to be between minimum and maximum."""
    number = _number_check(value, input_name)
    assert mi <= number <= ma, 'Input number {} must be between {} and {}. ' \
        'Got {}'.format(input_name, mi, ma, value)
    return number


def float_in_range_excl(value, mi=INFNEG, ma=INFPOS, input_name=''):
    """Check a float value to be greater than minimum and less than maximum."""
    number = _number_check(value, input_name)
    assert mi < number < ma, 'Input number {} must be greater than {} ' \
        'and less than {}. Got {}'.format(input_name, mi, ma, value)
    return number


def float_in_range_excl_incl(value, mi=INFNEG, ma=INFPOS, input_name=''):
    """Check a float value to be greater than minimum and less than/equal to maximum."""
    number = _number_check(value, input_name)
    assert mi < number <= ma, 'Input number {} must be greater than {} and less than ' \
        'or equal to {}. Got {}'.format(input_name, mi, ma, value)
    return number


def float_in_range_incl_excl(value, mi=INFNEG, ma=INFPOS, input_name=''):
    """Check a float value to be greater than/equal to minimum and less than maximum."""
    number = _number_check(value, input_name)
    assert mi <= number < ma, 'Input number {} must be greater than or equal to {} ' \
        'and less than {}. Got {}'.format(input_name, mi, ma, value)
    return number


def int_in_range(value, mi=INFNEG, ma=INFPOS, input_name=''):
    """Check an integer value to be between minimum and maximum."""
    try:
        number = int(value)
    except ValueError:
        # try to convert to float and then digit if possible
        try:
            number = int(float(value))
        except (ValueError, TypeError):
            raise TypeError('Input {} must be an integer. Got {}: {}.'.format(
                input_name, type(value), value))
    except (ValueError, TypeError):
        raise TypeError('Input {} must be an integer. Got {}: {}.'.format(
            input_name, type(value), value))
    assert mi <= number <= ma, 'Input integer {} must be between {} and {}. ' \
        'Got {}.'.format(input_name, mi, ma, value)
    return number


def float_positive(value, input_name=''):
    """Check a float value to be positive."""
    return float_in_range_excl(value, 0, INFPOS, input_name)


def int_positive(value, input_name=''):
    """Check if an integer value is positive."""
    return int_in_range(value, 0, INFPOS, input_name)


def tuple_with_length(value, length=3, item_type=float, input_name=''):
    """Try to create a tuple with a certain value."""
    try:
        value = tuple(item_type(v) for v in value)
    except (ValueError, TypeError):
        raise TypeError('Input {} must be a {}.'.format(
            input_name, item_type))
    assert len(value) == length, 'Input {} length must be {} not {}'.format(
        input_name, length, len(value))
    return value


def list_with_length(value, length=3, item_type=float, input_name=''):
    """Try to create a list with a certain value."""
    try:
        value = [item_type(v) for v in value]
    except (ValueError, TypeError):
        raise TypeError('Input {} must be a {}.'.format(
            input_name, item_type))
    assert len(value) == length, 'Input {} length must be {} not {}'.format(
        input_name, length, len(value))
    return value
