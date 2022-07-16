"""Objects used as alternatives to various numerical properties."""


class _AltNumber(object):
    __slots__ = ()

    def __init__(self):
        pass

    @property
    def name(self):
        return self.__class__.__name__

    def to_dict(self):
        """Get the object as a dictionary."""
        return {'type': self.name}

    def ToString(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.name


class Default(_AltNumber):
    """Object to signify when the default value of a visual interface should be used."""
    __slots__ = ()
    pass


default = Default()
