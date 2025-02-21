"""Classes for representing Path data."""
from ._types import _number


class PathData:
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d
    """
    __slots__ = ()

    def __str__(self):
        points = []
        attr = (getattr(self, prop) for prop in self.__slots__)
        for p in attr:
            if isinstance(p, bool):
                p = int(p)
            points.append(str(p))
        joined = ' '.join(points)
        return '{} {}'.format(self.command, joined)


class MoveTo(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#moveto_path_commands
    """
    command = 'M'
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = _number(x, 'x')
        self.y = _number(y, 'y')


class MoveToRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#moveto_path_commands
    """
    command = 'm'
    __slots__ = ('dx', 'dy')

    def __init__(self, dx, dy):
        self.dx = _number(dx, 'dx')
        self.dy = _number(dy, 'dy')


class LineTo(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'L'
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = _number(x, 'x')
        self.y = _number(y, 'y')


class LineToRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'l'
    __slots__ = ('dx', 'dy')

    def __init__(self, dx, dy):
        self.dx = _number(dx, 'dx')
        self.dy = _number(dy, 'dy')


class HorizontalLineTo(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'H'
    __slots__ = ('x',)

    def __init__(self, x):
        self.x = _number(x, 'x')


class HorizontalLineToRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'h'
    __slots__ = ('dx',)

    def __init__(self, dx):
        self.dx = _number(dx, 'dx')


class VerticalLineTo(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'V'
    __slots__ = ('y',)

    def __init__(self, y):
        self.y = _number(y, 'y')


class VerticalLineToRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#lineto_path_commands
    """
    command = 'v'
    __slots__ = ('dy',)

    def __init__(self, dy):
        self.dy = _number(dy, 'dy')


class CubicBezier(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#cubic_b%C3%A9zier_curve
    """
    command = 'C'
    __slots__ = ('x1', 'y1', 'x2', 'y2', 'x', 'y')

    def __init__(self, x1, y1, x2, y2, x, y):
        self.x1 = _number(x1, 'x1')
        self.y1 = _number(y1, 'y1')
        self.x2 = _number(x2, 'x2')
        self.y2 = _number(y2, 'y2')
        self.x = _number(x, 'x')
        self.y = _number(y, 'x')


class CubicBezierRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#cubic_b%C3%A9zier_curve
    """
    command = 'c'
    __slots__ = ('dx1', 'dy1', 'dx2', 'dy2', 'dx', 'dy')

    def __init__(self, dx1, dy1, dx2, dy2, dx, dy):
        self.dx1 = _number(dx1, 'dx1')
        self.dy1 = _number(dy1, 'dy1')
        self.dx2 = _number(dx2, 'dx2')
        self.dy2 = _number(dy2, 'dy2')
        self.dx = _number(dx, 'dx')
        self.dy = _number(dy, 'dy')


class SmoothCubicBezier(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#cubic_b%C3%A9zier_curve
    """
    command = 'S'
    __slots__ = ('x2', 'y2', 'x', 'y')

    def __init__(self, x2, y2, x, y):
        self.x2 = _number(x2, 'x2')
        self.y2 = _number(y2, 'y2')
        self.x = _number(x, 'x')
        self.y = _number(y, 'x')


class SmoothCubicBezierRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#cubic_b%C3%A9zier_curve
    """
    command = 's'
    __slots__ = ('dx2', 'dy2', 'dx', 'dy')

    def __init__(self, dx2, dy2, dx, dy):
        self.dx2 = _number(dx2, 'dx2')
        self.dy2 = _number(dy2, 'dy2')
        self.dx = _number(dx, 'dx')
        self.dy = _number(dy, 'dy')


class QuadraticBezier(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#quadratic_b%C3%A9zier_curve
    """
    command = 'Q'
    __slots__ = ('x1', 'y1', 'x', 'y')

    def __init__(self, x1, y1, x, y):
        self.x1 = _number(x1, 'x1')
        self.y1 = _number(y1, 'y1')
        self.x = _number(x, 'x')
        self.y = _number(y, 'x')


class QuadraticBezierRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#quadratic_b%C3%A9zier_curve
    """
    command = 'q'
    __slots__ = ('dx1', 'dy1', 'dx', 'dy')

    def __init__(self, dx1, dy1, dx, dy):
        self.dx1 = _number(dx1, 'dx1')
        self.dy1 = _number(dy1, 'dy1')
        self.dx = _number(dx, 'dx')
        self.dy = _number(dy, 'dy')


class SmoothQuadraticBezier(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#quadratic_b%C3%A9zier_curve
    """
    command = 'T'
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = _number(x, 'x')
        self.y = _number(y, 'x')


class SmoothQuadraticBezierRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#quadratic_b%C3%A9zier_curve
    """
    command = 't'
    __slots__ = ('dx', 'dy')

    def __init__(self, dx, dy):
        self.dx = _number(dx, 'dx')
        self.dy = _number(dy, 'dy')


class Arc(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#elliptical_arc_curve
    """
    command = 'A'
    __slots__ = ('rx', 'ry', 'angle', 'large_arc', 'sweep', 'x', 'y')

    def __init__(self, rx, ry, angle, large_arc, sweep, x, y):
        self.rx = _number(rx, 'rx')
        self.ry = _number(ry, 'rx')
        self.angle = _number(angle, 'angle')
        self.large_arc = bool(large_arc)
        self.sweep = bool(sweep)
        self.x = _number(x, 'x')
        self.y = _number(y, 'x')


class ArcRel(PathData):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#elliptical_arc_curve
    """
    command = 'a'
    __slots__ = ('rx', 'ry', 'angle', 'large_arc', 'sweep', 'dx', 'dy')

    def __init__(self, rx, ry, angle, large_arc, sweep, dx, dy):
        self.rx = _number(rx, 'rx')
        self.ry = _number(ry, 'rx')
        self.angle = _number(angle, 'angle')
        self.large_arc = bool(large_arc)
        self.sweep = bool(sweep)
        self.dx = _number(dx, 'dx')
        self.dy = _number(dy, 'dy')


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
