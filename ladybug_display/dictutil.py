# coding=utf-8
"""Utilities to convert any Ladybug Display dictionary to Python objects."""

from ladybug_display.geometry2d import DisplayVector2D, DisplayPoint2D, \
    DisplayRay2D, DisplayLineSegment2D, DisplayPolyline2D, DisplayArc2D, \
    DisplayPolygon2D, DisplayMesh2D
from ladybug_display.geometry3d import DisplayVector3D, DisplayPoint3D, \
    DisplayRay3D, DisplayPlane, DisplayLineSegment3D, DisplayPolyline3D, DisplayArc3D, \
    DisplayFace3D, DisplayMesh3D, DisplayPolyface3D, DisplaySphere, DisplayCone, \
    DisplayCylinder, DisplayText3D


def dict_to_object(display_dict, raise_exception=True):
    """
    Args:
        display_dict (dict): A dictionary of any Ladybug Display geometry object.
        raise_exception (bool): Boolean to note whether an exception should be
            raised if the object is not identified as a part of
            ladybug_display. (Default: True).

    Returns:
        A Python object derived from the input display_dict.
    """
    lbt_types = {
        'DisplayVector2D': DisplayVector2D,
        'DisplayPoint2D': DisplayPoint2D,
        'DisplayRay2D': DisplayRay2D,
        'DisplayLineSegment2D': DisplayLineSegment2D,
        'DisplayArc2D': DisplayArc2D,
        'DisplayPolyline2D': DisplayPolyline2D,
        'DisplayPolygon2D': DisplayPolygon2D,
        'DisplayMesh2D': DisplayMesh2D,
        'DisplayVector3D': DisplayVector3D,
        'DisplayPoint3D': DisplayPoint3D,
        'DisplayRay3D': DisplayRay3D,
        'DisplayLineSegment3D': DisplayLineSegment3D,
        'DisplayArc3D': DisplayArc3D,
        'DisplayPolyline3D': DisplayPolyline3D,
        'DisplayMesh3D': DisplayMesh3D,
        'DisplayPlane': DisplayPlane,
        'DisplayPolyface3D': DisplayPolyface3D,
        'DisplayFace3D': DisplayFace3D,
        'DisplaySphere': DisplaySphere,
        'DisplayCone': DisplayCone,
        'DisplayCylinder': DisplayCylinder,
        'DisplayText3D': DisplayText3D
    }

    # Get the ladybug_geometry object 'Type'
    try:
        obj_type = display_dict['type']
    except KeyError:
        raise ValueError('Ladybug dictionary lacks required "type" key.')

    # Build a new Ladybug Python Object based on the "Type"
    try:
        lbt_class = lbt_types[obj_type]
        return lbt_class.from_dict(display_dict)
    except KeyError:
        if raise_exception:
            raise ValueError(
                '{} is not a recognized ladybug display type'.format(obj_type))
        else:
            return None
