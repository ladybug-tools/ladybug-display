# coding=utf-8
"""Class for the entire SVG object."""
import os
from ladybug.config import folders

from . import _mixins as m
from ._types import PreserveAspectRatio, ViewBoxSpec, _number, _number_or_length, \
    _str, _str_enum, _obj, _list_of_objs
from .element import Element, OVERFLOWS


class SVG(
    Element,
    m.GraphicsElementEvents,
    m.Color,
    m.Graphics,
):
    """The svg element is a container that defines a new coordinate system and viewport.

    It is used as the outermost element of SVG documents, but it can also be used
    to embed an SVG fragment inside an SVG or HTML document.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/svg
    """
    OVERFLOWS = OVERFLOWS
    element_name = 'svg'

    def __init__(self, xmlns=None, viewBox=None, preserveAspectRatio=None,
                 x=None, y=None, width=None, height=None, class_=None,
                 mask=None, opacity=None, clip_path=None, overflow=None,
                 onunload=None, onabort=None, onerror=None, onresize=None,
                 onscroll=None, onzoom=None):
        super(SVG, self).__init__()
        self.xmlns = xmlns
        self.viewBox = viewBox
        self.preserveAspectRatio = preserveAspectRatio
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.class_ = class_
        self.mask = mask
        self.opacity = opacity
        self.clip_path = clip_path
        self.overflow = overflow
        self.onunload = onunload
        self.onabort = onabort
        self.onerror = onerror
        self.onresize = onresize
        self.onscroll = onscroll
        self.onzoom = onzoom

    @property
    def xmlns(self):
        """[str]"""
        return self._xmlns

    @xmlns.setter
    def xmlns(self, value):
        self._xmlns = _str(value, 'xmlns') \
            if value is not None else 'http://www.w3.org/2000/svg'

    @property
    def viewBox(self):
        """[obj]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/viewBox
        """
        return self._viewBox

    @viewBox.setter
    def viewBox(self, value):
        self._viewBox = _obj(value, ViewBoxSpec, 'viewBox', True)

    @property
    def preserveAspectRatio(self):
        """[obj]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/preserveAspectRatio
        """
        return self._preserveAspectRatio

    @preserveAspectRatio.setter
    def preserveAspectRatio(self, value):
        self._preserveAspectRatio = _obj(
            value, PreserveAspectRatio, 'preserveAspectRatio', True)

    @property
    def x(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/x
        """
        return self._x

    @x.setter
    def x(self, value):
        self._x = _number_or_length(value, 'x', True)

    @property
    def y(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/y
        """
        return self._y

    @y.setter
    def y(self, value):
        self._y = _number_or_length(value, 'y', True)

    @property
    def width(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/width
        """
        return self._width

    @width.setter
    def width(self, value):
        self._width = _number_or_length(value, 'width', True)

    @property
    def height(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/height
        """
        return self._height

    @height.setter
    def height(self, value):
        self._height = _number_or_length(value, 'height', True)

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
    def overflow(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/overflow
        """
        return self._overflow

    @overflow.setter
    def overflow(self, value):
        self._overflow = _str_enum(value, OVERFLOWS, 'overflow', True)

    @property
    def onunload(self):
        """[str]"""
        return self._onunload

    @onunload.setter
    def onunload(self, value):
        self._onunload = _str(value, 'onunload', True)

    @property
    def onabort(self):
        """[str]"""
        return self._onabort

    @onabort.setter
    def onabort(self, value):
        self._onabort = _str(value, 'onabort', True)

    @property
    def onerror(self):
        """[str]"""
        return self._onerror

    @onerror.setter
    def onerror(self, value):
        self._onerror = _str(value, 'onerror', True)

    @property
    def onresize(self):
        """[str]"""
        return self._onresize

    @onresize.setter
    def onresize(self, value):
        self._onresize = _str(value, 'onresize', True)

    @property
    def onscroll(self):
        """[str]"""
        return self._onscroll

    @onscroll.setter
    def onscroll(self, value):
        self._onscroll = _str(value, 'onscroll', True)

    @property
    def onzoom(self):
        """[str]"""
        return self._onzoom

    @onzoom.setter
    def onzoom(self, value):
        self._onzoom = _str(value, 'onzoom', True)

    def to_file(self, name='Unnamed', folder=None):
        """Write SVG object to a file.

        Args:
            name: A text string for the name of the SVG file. (Default: Unnamed).
            folder: A text string for the directory where the file will be written.
                If unspecified, a svg subdirectory with default_epw_folder will
                be used. This is usually at
                "C:\\Users\\USERNAME\\APPDATA\\Roaming\\ladybug_tools\\weather."
        """
        # set up a name and folder for the SVG
        if name is None:
            name = self.identifier
        file_name = name if name.lower().endswith('.svg') else '{}.svg'.format(name)
        folder = folder if folder is not None else \
            os.path.join(folders.default_epw_folder, 'svg')
        if not os.path.isdir(folder):
            os.makedirs(folder)
        svg_file = os.path.join(folder, file_name)
        # write SVG
        with open(svg_file, 'w') as fp:
            fp.write(str(self))
        return svg_file
