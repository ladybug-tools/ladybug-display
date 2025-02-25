"""SVG Switch class."""
from . import _mixins as m
from ._transforms import Transform
from ._types import _number, _str, _list_of_objs
from .element import Element


class Switch(Element, m.Color, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/switch
    """
    element_name = 'switch'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 opacity=None, class_=None, pointer_events=None):
        super(Switch, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.transform = transform
        self.opacity = opacity
        self.class_ = class_
        self.pointer_events = pointer_events

    @property
    def externalResourcesRequired(self):
        """[bool]"""
        return self._externalResourcesRequired

    @externalResourcesRequired.setter
    def externalResourcesRequired(self, value):
        self._externalResourcesRequired = bool(value) if value is not None else None

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
    def opacity(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/opacity
        """
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = _number(value, 'opacity', True)

    @property
    def class_(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/class-
        """
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = _list_of_objs(value, str, 'class_', True)

    @property
    def pointer_events(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/pointer-events
        """
        return self._pointer_events

    @pointer_events.setter
    def pointer_events(self, value):
        self._pointer_events = _str(value, 'pointer_events', True)
