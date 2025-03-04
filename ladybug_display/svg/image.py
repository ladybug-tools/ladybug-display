# coding=utf-8
"""SVG Image class."""
from . import _mixins as m
from ._transforms import Transform
from ._types import PreserveAspectRatio, _number, _number_or_length, _str, _str_enum, \
    _obj, _list_of_objs
from .element import Element, OVERFLOWS, VECTOR_EFFECTS, VISIBILITIES


class Image(
    Element,
    m.Color,
    m.Graphics,
    m.GraphicsElementEvents,
):
    """The <image> SVG element includes images inside SVG documents.

    The only image formats SVG software must support are JPEG, PNG, and other SVG files.
    Animated GIF behavior is undefined.

    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/image
    """
    OVERFLOWS = OVERFLOWS
    VECTOR_EFFECTS = VECTOR_EFFECTS
    VISIBILITIES = VISIBILITIES
    RENDERINGS = set(('auto', 'optimizeSpeed', 'optimizeQuality'))
    element_name = 'image'

    def __init__(self, href=None, transform=None, x=None, y=None, width=None, height=None,
                 preserveAspectRatio=None, image_rendering=None, class_=None,
                 vector_effect=None, visibility=None, mask=None, opacity=None,
                 clip_path=None, overflow=None):
        super(Image, self).__init__()
        self.href = href
        self.transform = transform
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.preserveAspectRatio = preserveAspectRatio
        self.image_rendering = image_rendering
        self.class_ = class_
        self.vector_effect = vector_effect
        self.visibility = visibility
        self.mask = mask
        self.opacity = opacity
        self.clip_path = clip_path
        self.overflow = overflow

    @property
    def href(self):
        """[str]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/href
        """
        return self._href

    @href.setter
    def href(self, value):
        self._href = _str(value, 'href', True)

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
    def image_rendering(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/image-rendering
        """
        return self._image_rendering

    @image_rendering.setter
    def image_rendering(self, value):
        self._image_rendering = _str_enum(
            value, self.RENDERINGS, 'image_rendering', True)

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
    def vector_effect(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/vector-effect
        """
        return self._vector_effect

    @vector_effect.setter
    def vector_effect(self, value):
        self._vector_effect = _str_enum(value, VECTOR_EFFECTS, 'vector_effect', True)

    @property
    def visibility(self):
        """[str enum]

        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/visibility
        """
        return self._visibility

    @visibility.setter
    def visibility(self, value):
        self._visibility = _str_enum(value, VISIBILITIES, 'visibility', True)

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
