"""Classes for representing Path data."""
from ._types import Number


class PathData:
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d
    """
    __slots__ = ()

    def __str__(self) -> str:
        points = []
        attr = (getattr(self, prop) for prop in self.__slots__)
        for p in attr:
            if isinstance(p, bool):
                p = int(p)
            points.append(str(p))
        joined = ' '.join(points)
        return f'{self.command} {joined}'


class MoveTo(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#moveto_path_commands
    """
    command = 'M'
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.x = x
        self.y = y


class MoveToRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#moveto_path_commands
    """
    command = 'm'
    __slots__ = ('dx', 'dy')

    def __init__(self, dx, dy):
        assert isinstance(dx, Number), 'Expected number for dx. Got {}.'.format(type(dx))
        assert isinstance(dy, Number), 'Expected number for dy. Got {}.'.format(type(dy))
        self.dx = dx
        self.dy = dy


class LineTo(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'L'
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.x = x
        self.y = y


class LineToRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'l'
    __slots__ = ('dx', 'dy')

    def __init__(self, dx, dy):
        assert isinstance(dx, Number), 'Expected number for dx. Got {}.'.format(type(dx))
        assert isinstance(dy, Number), 'Expected number for dy. Got {}.'.format(type(dy))
        self.dx = dx
        self.dy = dy


class HorizontalLineTo(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'H'
    __slots__ = ('x',)

    def __init__(self, x):
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        self.x = x


class HorizontalLineToRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'h'
    __slots__ = ('dx',)

    def __init__(self, dx):
        assert isinstance(dx, Number), 'Expected number for dx. Got {}.'.format(type(dx))
        self.dx = dx


class VerticalLineTo(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'V'
    __slots__ = ('y',)

    def __init__(self, y):
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.y = y


class VerticalLineToRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'v'
    __slots__ = ('dy',)

    def __init__(self, dy):
        assert isinstance(dy, Number), 'Expected number for dy. Got {}.'.format(type(dy))
        self.dy = dy


class CubicBezier(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#cubic_b%C3%A9zier_curve
    """
    command = 'C'
    __slots__ = ('x1', 'y1', 'x2', 'y2', 'x', 'y')

    def __init__(self, x1, y1, x2, y2, x, y):
        assert isinstance(x1, Number), 'Expected number for x1. Got {}.'.format(type(x1))
        assert isinstance(y1, Number), 'Expected number for y1. Got {}.'.format(type(y1))
        assert isinstance(x2, Number), 'Expected number for x2. Got {}.'.format(type(x2))
        assert isinstance(y2, Number), 'Expected number for y2. Got {}.'.format(type(y2))
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x = x
        self.y = y


class CubicBezierRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#cubic_b%C3%A9zier_curve
    """
    command = 'c'
    __slots__ = ('dx1', 'dy1', 'dx2', 'dy2', 'dx', 'dy')

    def __init__(self, dx1, dy1, dx2, dy2, dx, dy):
        assert isinstance(dx1, Number), 'Expected number for dx1. Got {}.'.format(type(dx1))
        assert isinstance(dy1, Number), 'Expected number for dy1. Got {}.'.format(type(dy1))
        assert isinstance(dx2, Number), 'Expected number for dx2. Got {}.'.format(type(dx2))
        assert isinstance(dy2, Number), 'Expected number for dy2. Got {}.'.format(type(dy2))
        assert isinstance(dx, Number), 'Expected number for dx. Got {}.'.format(type(dx))
        assert isinstance(dy, Number), 'Expected number for dy. Got {}.'.format(type(dy))
        self.dx1 = dx1
        self.dy1 = dy1
        self.dx2 = dx2
        self.dy2 = dy2
        self.dx = dx
        self.dy = dy


class SmoothCubicBezier(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#cubic_b%C3%A9zier_curve
    """
    command = 'S'
    __slots__ = ('x2', 'y2', 'x', 'y')

    def __init__(self, x2, y2, x, y):
        assert isinstance(x2, Number), 'Expected number for x2. Got {}.'.format(type(x2))
        assert isinstance(y2, Number), 'Expected number for y2. Got {}.'.format(type(y2))
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.x2 = x2
        self.y2 = y2
        self.x = x
        self.y = y


class SmoothCubicBezierRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#cubic_b%C3%A9zier_curve
    """
    command = 's'
    __slots__ = ('dx2', 'dy2', 'dx', 'dy')

    def __init__(self, dx2, dy2, dx, dy):
        assert isinstance(dx2, Number), 'Expected number for dx2. Got {}.'.format(type(dx2))
        assert isinstance(dy2, Number), 'Expected number for dy2. Got {}.'.format(type(dy2))
        assert isinstance(dx, Number), 'Expected number for dx. Got {}.'.format(type(dx))
        assert isinstance(dy, Number), 'Expected number for dy. Got {}.'.format(type(dy))
        self.dx2 = dx2
        self.dy2 = dy2
        self.dx = dx
        self.dy = dy


class QuadraticBezier(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#quadratic_b%C3%A9zier_curve
    """
    command = 'Q'
    __slots__ = ('x1', 'y1', 'x', 'y')

    def __init__(self, x1, y1, x, y):
        assert isinstance(x1, Number), 'Expected number for x1. Got {}.'.format(type(x1))
        assert isinstance(y1, Number), 'Expected number for y1. Got {}.'.format(type(y1))
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.x1 = x1
        self.y1 = y1
        self.x = x
        self.y = y


class QuadraticBezierRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#quadratic_b%C3%A9zier_curve
    """
    command = 'q'
    __slots__ = ('dx1', 'dy1', 'dx', 'dy')

    def __init__(self, dx1, dy1, dx, dy):
        assert isinstance(dx1, Number), 'Expected number for dx1. Got {}.'.format(type(dx1))
        assert isinstance(dy1, Number), 'Expected number for dy1. Got {}.'.format(type(dy1))
        assert isinstance(dx, Number), 'Expected number for dx. Got {}.'.format(type(dx))
        assert isinstance(dy, Number), 'Expected number for dy. Got {}.'.format(type(dy))
        self.dx1 = dx1
        self.dy1 = dy1
        self.dx = dx
        self.dy = dy


class SmoothQuadraticBezier(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#quadratic_b%C3%A9zier_curve
    """
    command = 'T'
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.x = x
        self.y = y


class SmoothQuadraticBezierRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#quadratic_b%C3%A9zier_curve
    """
    command = 't'
    __slots__ = ('dx', 'dy')

    def __init__(self, dx, dy):
        assert isinstance(dx, Number), 'Expected number for dx. Got {}.'.format(type(dx))
        assert isinstance(dy, Number), 'Expected number for dy. Got {}.'.format(type(dy))
        self.dx = dx
        self.dy = dy


class Arc(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#elliptical_arc_curve
    """
    command = 'A'
    __slots__ = ('rx', 'ry', 'angle', 'large_arc', 'sweep', 'x', 'y')

    def __init__(self, rx, ry, angle, large_arc, sweep, x, y):
        assert isinstance(rx, Number), 'Expected number for rx. Got {}.'.format(type(rx))
        assert isinstance(ry, Number), 'Expected number for ry. Got {}.'.format(type(ry))
        assert isinstance(angle, Number), 'Expected number for angle. Got {}.'.format(type(angle))
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.rx = rx
        self.ry = ry
        self.angle = angle
        self.large_arc = bool(large_arc)
        self.sweep = bool(sweep)
        self.x = x
        self.y = y


class ArcRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#elliptical_arc_curve
    """
    command = 'a'
    __slots__ = ('rx', 'ry', 'angle', 'large_arc', 'sweep', 'x', 'y')

    def __init__(self, rx, ry, angle, large_arc, sweep, x, y):
        assert isinstance(rx, Number), 'Expected number for rx. Got {}.'.format(type(rx))
        assert isinstance(ry, Number), 'Expected number for ry. Got {}.'.format(type(ry))
        assert isinstance(angle, Number), 'Expected number for angle. Got {}.'.format(type(angle))
        assert isinstance(x, Number), 'Expected number for x. Got {}.'.format(type(x))
        assert isinstance(y, Number), 'Expected number for y. Got {}.'.format(type(y))
        self.rx = rx
        self.ry = ry
        self.angle = angle
        self.large_arc = bool(large_arc)
        self.sweep = bool(sweep)
        self.x = x
        self.y = y


class ClosePath(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#closepath
    """
    command = 'Z'


# aliases
M = MoveTo
m = MoveToRel
L = LineTo
l = LineToRel  # noqa: E741
H = HorizontalLineTo
h = HorizontalLineToRel
V = VerticalLineTo
v = VerticalLineToRel
C = CubicBezier
c = CubicBezierRel
S = SmoothCubicBezier
s = SmoothCubicBezierRel
Q = QuadraticBezier
q = QuadraticBezierRel
T = SmoothQuadraticBezier
t = SmoothQuadraticBezierRel
A = Arc
a = ArcRel
Z = ClosePath
