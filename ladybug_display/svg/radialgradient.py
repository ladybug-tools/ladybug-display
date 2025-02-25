"""SVG RadialGradient class."""
from . import _mixins as m
from ._types import _number_or_length
from .element import Element, _Gradient


class RadialGradient(Element, _Gradient, m.Color, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/radialGradient
    """
    element_name = 'radialGradient'

    def __init__(self, cx=None, cy=None, r=None, fr=None, fx=None, fy=None):
        super(RadialGradient, self).__init__()
        self.cx = cx
        self.cy = cy
        self.r = r
        self.fr = fr
        self.fx = fx
        self.fy = fy

    @property
    def cx(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/cx
        """
        return self._cx

    @cx.setter
    def cx(self, value):
        self._cx = _number_or_length(value, 'cx', True)

    @property
    def cy(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/cy
        """
        return self._cy

    @cy.setter
    def cy(self, value):
        self._cy = _number_or_length(value, 'cy', True)

    @property
    def r(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/r
        """
        return self._r

    @r.setter
    def r(self, value):
        self._r = _number_or_length(value, 'r', True)

    @property
    def fr(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fr
        """
        return self._fr

    @fr.setter
    def fr(self, value):
        self._fr = _number_or_length(value, 'fr', True)

    @property
    def fx(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fx
        """
        return self._fx

    @fx.setter
    def fx(self, value):
        self._fx = _number_or_length(value, 'fx', True)

    @property
    def fy(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fy
        """
        return self._fy

    @fy.setter
    def fy(self, value):
        self._fy = _number_or_length(value, 'fy', True)
