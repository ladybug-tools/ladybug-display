# coding=utf-8
"""SVG Defs class."""
from . import _mixins as m
from ._transforms import Transform
from ._types import _str, _list_of_objs
from .element import Element


class Defs(
    Element,
    m.Color,
    m.GraphicsElementEvents,
):
    """The <defs> is used to store graphical objects that will be used at a later time.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/defs
    """
    element_name = 'defs'

    def __init__(self, transform=None, class_=None, pointer_events=None):
        super(Defs, self).__init__()
        self.transform = transform
        self.class_ = class_
        self.pointer_events = pointer_events

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
    def pointer_events(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/pointer-events
        """
        return self._pointer_events

    @pointer_events.setter
    def pointer_events(self, value):
        self._pointer_events = _str(value, 'pointer_events', True)
