"""SVG Stop class for gradients."""
from . import _mixins as m
from ._types import _number, _number_or_length, _str, _list_of_objs
from .element import Element


class Stop(Element, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/stop
    """
    element_name = 'stop'

    def __init__(self, offset=None, stop_opacity=None, stop_color=None, class_=None):
        super(Stop, self).__init__()
        self.offset = offset
        self.stop_opacity = stop_opacity
        self.stop_color = stop_color
        self.class_ = class_

    @property
    def offset(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/offset
        """
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = _number_or_length(value, 'offset', True)

    @property
    def stop_opacity(self):
        """[number]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stop-opacity
        """
        return self._stop_opacity

    @stop_opacity.setter
    def stop_opacity(self, value):
        self._stop_opacity = _number(value, 'stop_opacity', True)

    @property
    def stop_color(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stop-color
        """
        return self._stop_color

    @stop_color.setter
    def stop_color(self, value):
        self._stop_color = _str(value, 'stop_color', True)

    @property
    def class_(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/class
        """
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = _list_of_objs(value, str, 'class_', True)
