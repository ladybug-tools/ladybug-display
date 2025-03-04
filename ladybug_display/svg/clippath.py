# coding=utf-8
"""SVG ClipPath class."""
from . import _mixins as m
from ._transforms import Transform
from ._types import _str, _str_enum, _list_of_objs
from .element import Element


class ClipPath(Element, m.Color, m.Graphics):
    """
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/clipPath
    """
    UNITS = set(('userSpaceOnUse', 'objectBoundingBox'))
    element_name = 'clipPath'

    def __init__(self, externalResourcesRequired=None, transform=None,
                 clipPathUnits=None, class_=None, mask=None, clip_path=None):
        super(ClipPath, self).__init__()
        self.externalResourcesRequired = externalResourcesRequired
        self.transform = transform
        self.clipPathUnits = clipPathUnits
        self.class_ = class_
        self.mask = mask
        self.clip_path = clip_path

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
    def clipPathUnits(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/clipPathUnits
        """
        return self._clipPathUnits

    @clipPathUnits.setter
    def clipPathUnits(self, value):
        self._clipPathUnits = _str_enum(value, self.UNITS, 'clipPathUnits', True)

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
    def clip_path(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/clip-path
        """
        return self._clip_path

    @clip_path.setter
    def clip_path(self, value):
        self._clip_path = _str(value, 'clip_path', True)
