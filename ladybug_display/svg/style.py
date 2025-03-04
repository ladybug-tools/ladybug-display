# coding=utf-8
"""SVG Style class."""
from . import _mixins as m
from ._types import _str, _list_of_objs
from .element import Element


class Style(Element, m.GraphicsElementEvents):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/style
    """
    element_name = 'style'

    def __init__(self, type=None, media=None, title=None):
        super(Style, self).__init__()
        self.type = type
        self.media = media
        self.title = title

    @property
    def type(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/type
        """
        return self._type

    @type.setter
    def type(self, value):
        self._type = _str(value, 'type', True)

    @property
    def media(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/media
        """
        return self._media

    @media.setter
    def media(self, value):
        self._media = _list_of_objs(value, str, 'media', True)

    @property
    def title(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/title
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = _str(value, 'title', True)
