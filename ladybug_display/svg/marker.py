# coding=utf-8
"""SVG Marker class."""
from . import _mixins as m
from ._types import PreserveAspectRatio, ViewBoxSpec, \
    _number, _number_or_length, _str, _str_enum, _obj, _list_of_objs
from .element import Element, OVERFLOWS


class Marker(Element, m.Color, m.GraphicsElementEvents, m.Graphics):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker
    """
    UNITS = set(('strokeWidth', 'userSpaceOnUse', 'userSpace'))
    element_name = 'marker'

    def __init__(self, externalResourcesRequired=None,
                 viewBox=None, preserveAspectRatio=None, refX=None, refY=None,
                 markerUnits=None, markerWidth=None, markerHeight=None, orient=None,
                 opacity=None, clip_path=None, class_=None, mask=None, overflow=None):
        super(Marker, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.viewBox = viewBox
        self.preserveAspectRatio = preserveAspectRatio
        self.refX = refX
        self.refY = refY
        self.markerUnits = markerUnits
        self.markerWidth = markerWidth
        self.markerHeight = markerHeight
        self.orient = orient
        self.opacity = opacity
        self.clip_path = clip_path
        self.class_ = class_
        self.mask = mask
        self.overflow = overflow

    @property
    def externalResourcesRequired(self):
        """[bool]"""
        return self._externalResourcesRequired

    @externalResourcesRequired.setter
    def externalResourcesRequired(self, value):
        self._externalResourcesRequired = bool(value) if value is not None else None

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
        self._preserveAspectRatio = \
            _obj(value, PreserveAspectRatio, 'preserveAspectRatio', True)

    @property
    def refX(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/refX
        """
        return self._refX

    @refX.setter
    def refX(self, value):
        self._refX = _number_or_length(value, 'refX', True)

    @property
    def refY(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/refY
        """
        return self._refY

    @refY.setter
    def refY(self, value):
        self._refY = _number_or_length(value, 'refY', True)

    @property
    def markerUnits(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/markerUnits
        """
        return self._markerUnits

    @markerUnits.setter
    def markerUnits(self, value):
        self._markerUnits = _str_enum(value, self.UNITS, 'markerUnits', True)

    @property
    def markerWidth(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/markerWidth
        """
        return self._markerWidth

    @markerWidth.setter
    def markerWidth(self, value):
        self._markerWidth = _number_or_length(value, 'markerWidth', True)

    @property
    def markerHeight(self):
        """[number or length]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/markerHeight
        """
        return self._markerHeight

    @markerHeight.setter
    def markerHeight(self, value):
        self._markerHeight = _number_or_length(value, 'markerHeight', True)

    @property
    def orient(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/orient
        """
        return self._orient

    @orient.setter
    def orient(self, value):
        self._orient = _str(value, 'orient', True)

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
    def class_(self):
        """[list of objs]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/class-
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
    def overflow(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/overflow
        """
        return self._overflow

    @overflow.setter
    def overflow(self, value):
        self._overflow = _str_enum(value, OVERFLOWS, 'overflow', True)
