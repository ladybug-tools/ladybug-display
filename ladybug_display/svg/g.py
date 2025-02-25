"""Class for SVG group."""
from . import _mixins as m
from ._transforms import Transform
from ._types import _number, _str, _str_enum, _list_of_objs
from .element import Element, FILL_RULES


class G(
    Element,
    m.GraphicsElementEvents,
    m.Color,
    m.Graphics,
):
    """The <g> SVG element is a container used to group other SVG elements.

    Transformations applied to the <g> element are performed on its child elements,
    and its attributes are inherited by its children. It can also group multiple elements
    to be referenced later with the <use> element.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/g
    """
    FILL_RULES = FILL_RULES
    element_name = 'g'

    def __init__(self, transform=None, class_=None, mask=None, opacity=None,
                 clip_path=None, fill_rule=None, fill_opacity=None, fill=None):
        super(G, self).__init__()
        self.transform = transform
        self.class_ = class_
        self.mask = mask
        self.opacity = opacity
        self.clip_path = clip_path
        self.fill_rule = fill_rule
        self.fill_opacity = fill_opacity
        self.fill = fill

    @property
    def transform(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
        """
        return self._transform

    @transform.setter
    def transform(self, value):
        self._transform = _list_of_objs(value, Transform, 'transform', True)

    @property
    def class_(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/class
        """
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = _list_of_objs(value, str, 'class_', True)

    @property
    def mask(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/mask
        """
        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = _str(value, 'mask', True)

    @property
    def opacity(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/opacity
        """
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = _number(value, 'opacity', True)

    @property
    def clip_path(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/clip-path
        """
        return self._clip_path

    @clip_path.setter
    def clip_path(self, value):
        self._clip_path = _str(value, 'clip_path', True)

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
    def fill_opacity(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-opacity
        """
        return self._fill_opacity

    @fill_opacity.setter
    def fill_opacity(self, value):
        self._fill_opacity = _number(value, 'fill_opacity', True)

    @property
    def fill(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill
        """
        return self._fill

    @fill.setter
    def fill(self, value):
        self._fill = _str(value, 'fill', True)
