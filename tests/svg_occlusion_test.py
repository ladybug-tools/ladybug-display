# coding=utf-8
"""Check visible SVG fills at known overlaps, not just successful serialization."""
import pytest
from xml.etree import ElementTree

from ladybug.color import Color
from ladybug_geometry.geometry3d import Face3D, Point3D, Vector3D, Mesh3D, Plane, Ray3D, \
    LineSegment3D
from ladybug_geometry.geometry2d import Point2D
from ladybug_display.context import ContextGeometry
from ladybug_display.geometry3d import DisplayFace3D, DisplayMesh3D, DisplayLineSegment3D
from ladybug_display.visualization import VisualizationSet
from ladybug_display.analysis import AnalysisGeometry, VisualizationData
import ladybug_display.svg as svg


def _face(points, color):
    return DisplayFace3D(Face3D(tuple(Point3D(*p) for p in points)), Color(*color))


def _inside(points, x, y):
    inside = False
    for a, b in zip(points, points[1:] + points[:1]):
        if (a[1] > y) != (b[1] > y):
            if x < a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]):
                inside = not inside
    return inside


def _contains(element, x, y):
    if isinstance(element, svg.Polygon):
        return _inside(list(zip(element.points[::2], element.points[1::2])), x, y)
    if isinstance(element, svg.Path):
        rings = []
        for command in element.d:
            if isinstance(command, svg.MoveTo):
                rings.append([])
            if isinstance(command, (svg.MoveTo, svg.LineTo)):
                rings[-1].append((command.x, command.y))
        return sum(_inside(ring, x, y) for ring in rings) % 2 == 1
    return any(_contains(child, x, y) for child in element.elements or [])


def _paint_at(canvas, x, y):
    clips = {}

    def find(element):
        if isinstance(element, svg.ClipPath):
            clips[element.id] = element
        for child in element.elements or []:
            find(child)
    find(canvas)
    painted = []

    def draw(element):
        if isinstance(element, (svg.ClipPath, svg.Defs)):
            return
        clip = getattr(element, 'clip_path', None)
        if clip and not _contains(clips[clip[5:-1]], x, y):
            return
        if isinstance(element, (svg.Polygon, svg.Path)):
            fill = getattr(element, 'fill', None)
            if fill and fill != 'none' and _contains(element, x, y):
                painted.append(fill)
        stroke = getattr(element, 'stroke', None)
        if stroke and stroke != 'none':
            points = []
            if isinstance(element, svg.Line):
                points = [(element.x1, element.y1), (element.x2, element.y2)]
            elif isinstance(element, (svg.Polygon, svg.Polyline)):
                points = list(zip(element.points[::2], element.points[1::2]))
                if isinstance(element, svg.Polygon):
                    points.append(points[0])
            for a, b in zip(points, points[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                length = dx * dx + dy * dy
                t = min(1, max(0, ((x - a[0]) * dx + (y - a[1]) * dy) / length)) \
                    if length else 0
                distance = ((x - a[0] - t * dx) ** 2 + (y - a[1] - t * dy) ** 2) ** 0.5
                if distance <= (element.stroke_width or 1) / 2:
                    painted.append(stroke)
        for child in element.elements or []:
            draw(child)
    draw(canvas)
    return painted[-1] if painted else None


@pytest.mark.parametrize('offset', [(0, 0, 0), (100, -200, 300)])
@pytest.mark.parametrize('mesh', [False, True])
def test_small_overlap(offset, mesh):
    """Perimeter rays miss a narrow overlap away from sampled vertices."""
    a = _face([(0, 7, 5), (10, 7, 5), (10, 8, 5), (0, 8, 5)], (255, 0, 0))
    b = _face([(2, 0, 0), (3, 0, 0), (3, 10, 10), (2, 10, 10)], (0, 0, 255))
    geometry = [a, b]
    if mesh:
        geometry = [DisplayMesh3D(Mesh3D(g.geometry.vertices, [(0, 1, 2, 3)]),
                                  g.color) for g in geometry]
    for g in geometry:
        g.move(Vector3D(*offset))
    vis = VisualizationSet('overlap', [ContextGeometry('strips', geometry)])
    before = vis.to_dict()
    result = vis.to_svg(100, 100, margin=0)
    assert _paint_at(result, 25, 25) == '#0000ff'
    assert vis.to_dict() == before


def test_intersecting_faces():
    """One whole-face order cannot show both sides of a crossing correctly."""
    a = _face([(0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5)], (255, 0, 0))
    b = _face([(2, 0, 0), (3, 0, 0), (3, 10, 10), (2, 10, 10)], (0, 0, 255))
    vis = VisualizationSet('crossing', [ContextGeometry('planes', [a, b])])
    result = vis.to_svg(100, 100, margin=0)
    assert _paint_at(result, 25, 25) == '#0000ff'
    assert _paint_at(result, 25, 75) == '#ff0000'


def test_serialized_plane_offset_does_not_control_visibility():
    """A stale plane origin must not reorder vertices or trap the partition loop."""
    points = tuple(Point3D(x, y, 5) for x, y in [(0, 0), (10, 0), (10, 10), (0, 10)])
    red = DisplayFace3D(Face3D(points, plane=Plane(o=Point3D(0, 0, 50))), Color(255, 0, 0))
    blue = _face([(0, 0, 6), (10, 0, 6), (10, 10, 6), (0, 10, 6)], (0, 0, 255))
    vis = VisualizationSet('plane_origin', [ContextGeometry('faces', [red, blue])])
    before = vis.to_dict()
    assert _paint_at(vis.to_svg(100, 100, margin=0), 25, 25) == '#0000ff'
    assert vis.to_dict() == before


def test_warped_quad_retains_vertex_depths():
    """Triangulating a warped quad must retain its unflattened 3D vertices."""
    red = _face([(0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5)], (255, 0, 0))
    blue = _face([(0, 0, 0), (10, 0, 0), (10, 10, 10), (0, 10, 0)], (0, 0, 255))
    vis = VisualizationSet('warped', [ContextGeometry('faces', [red, blue])])
    result = vis.to_svg(100, 100, margin=0)
    assert _paint_at(result, 75, 25) == '#0000ff'
    assert _paint_at(result, 25, 25) == '#ff0000'


def test_split_face_with_hole():
    """A cut through a holed face must leave its opening transparent."""
    red = _face([(0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5)], (255, 0, 0))
    red = DisplayFace3D(Face3D(red.geometry.boundary, holes=[tuple(
        Point3D(x, y, 5) for x, y in [(4, 4), (6, 4), (6, 6), (4, 6)])]), red.color)
    blue = _face([(0, 0, 0), (10, 0, 10), (10, 10, 10), (0, 10, 0)], (0, 0, 255))
    vis = VisualizationSet('hole', [ContextGeometry('planes', [red, blue])])
    result = vis.to_svg(100, 100, margin=0)
    assert _paint_at(result, 25, 25) == '#ff0000'
    assert _paint_at(result, 45, 55) == '#0000ff'
    assert _paint_at(result, 75, 25) == '#0000ff'


@pytest.mark.parametrize('mesh', [False, True])
def test_edge_on_face_keeps_visible_edges(mesh):
    """A vertical wall's top edge remains visible above an intersecting slab."""
    slab = _face([(0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5)], (255, 0, 0))
    wall = _face([(2, 0, 0), (2, 10, 0), (2, 10, 10), (2, 0, 10)], (0, 0, 255))
    wall.display_mode = 'SurfaceWithEdges'
    if mesh:
        wall = DisplayMesh3D(Mesh3D(wall.geometry.vertices, [(0, 1, 2, 3)]),
                             wall.color, 'SurfaceWithEdges')
    vis = VisualizationSet('edge', [ContextGeometry('wall', [slab, wall])])
    result = vis.to_svg(100, 100, margin=0)
    assert _paint_at(result, 20, 75) == 'black'


def test_line_crosses_surface():
    """Only the part of a line in front of the slab may be visible."""
    slab = _face([(0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5)], (255, 0, 0))
    line = DisplayLineSegment3D(LineSegment3D.from_end_points(
        Point3D(0, 5, 0), Point3D(10, 5, 10)), Color(0, 0, 255))
    vis = VisualizationSet('line', [ContextGeometry('crossing', [slab, line])])
    result = vis.to_svg(100, 100, margin=0)
    assert _paint_at(result, 25, 50) == '#ff0000'
    assert _paint_at(result, 75, 50) == '#0000ff'


def test_separate_coplanar_edges_follow_surface_fills():
    """Honeybee emits independent edges after surfaces in another context layer."""
    slab = _face([(0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5)], (255, 0, 0))
    line = DisplayLineSegment3D(LineSegment3D.from_end_points(
        Point3D(0, 5, 5), Point3D(10, 5, 5)), Color(0, 0, 255))
    vis = VisualizationSet('coplanar', [ContextGeometry('faces', [slab]),
                                       ContextGeometry('edges', [line])])
    assert _paint_at(vis.to_svg(100, 100, margin=0), 25, 50) == '#0000ff'


def test_shared_edge_follows_near_partition_faces():
    """An edge shared by perpendicular planes must follow both visible fills."""
    slab = _face([(0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5)], (255, 0, 0))
    wall = _face([(10, 0, 0), (10, 10, 0), (10, 10, 10), (10, 0, 10)], (0, 255, 0))
    line = DisplayLineSegment3D(LineSegment3D.from_end_points(
        Point3D(10, 0, 5), Point3D(10, 10, 5)), Color(0, 0, 255))
    vis = VisualizationSet('shared', [ContextGeometry('faces', [slab, wall]),
                                     ContextGeometry('edges', [line])])
    plane = vis.VIEW_MAP['NE']
    points = [plane.xyz_to_xy(p) for g in (slab, wall) for p in g.geometry.boundary]
    xmin, xmax = min(-p.x for p in points), max(-p.x for p in points)
    ymin, ymax = min(-p.y for p in points), max(-p.y for p in points)
    scale = 100 / max(xmax-xmin, ymax-ymin)
    p = plane.xyz_to_xy(line.p1 + line.v * 0.371)
    x = (-p.x-xmin)*scale+(100-(xmax-xmin)*scale)/2
    y = (ymax+p.y)*scale+(100-(ymax-ymin)*scale)/2
    assert _paint_at(vis.to_svg(100, 100, margin=0, view='NE'), x, y) == '#0000ff'


def test_line_visible_through_hole():
    """An opaque face hides a rear line except where it passes behind a hole."""
    face = Face3D(tuple(Point3D(x, y, 5) for x, y in
                        [(0, 0), (10, 0), (10, 10), (0, 10)]), holes=[tuple(
        Point3D(x, y, 5) for x, y in [(4, 4), (6, 4), (6, 6), (4, 6)])])
    slab = DisplayFace3D(face, Color(255, 0, 0))
    line = DisplayLineSegment3D(LineSegment3D.from_end_points(
        Point3D(0, 5, 0), Point3D(10, 5, 0)), Color(0, 0, 255))
    result = VisualizationSet('hole_line', [ContextGeometry('scene', [slab, line])]).to_svg(
        100, 100, margin=0)
    assert _paint_at(result, 25, 50) == '#ff0000'
    assert _paint_at(result, 50, 50) == '#0000ff'
    assert _paint_at(result, 75, 50) == '#ff0000'


@pytest.mark.parametrize('view', list(VisualizationSet.VIEW_MAP))
def test_line_visibility_in_all_views(view):
    """Check actual stroke visibility against 3D intersections in each view."""
    slab = _face([(0, 0, 5), (10, 0, 5), (10, 10, 5), (0, 10, 5)], (255, 0, 0))
    line = DisplayLineSegment3D(LineSegment3D.from_end_points(
        Point3D(0, 5, 0), Point3D(10, 5, 10)), Color(0, 0, 255))
    vis = VisualizationSet('line_views', [ContextGeometry('scene', [slab, line])])
    result = vis.to_svg(100, 100, margin=0, view=view)
    plane = VisualizationSet.VIEW_MAP[view]
    sign = 1 if view == 'Top' else -1
    points = [plane.xyz_to_xy(p) for p in
              list(slab.geometry.boundary) + [line.p1, line.p2]]
    xs, ys = [sign * p.x for p in points], [sign * p.y for p in points]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    scale = 100 / max(xmax - xmin, ymax - ymin)
    cx, cy = (100 - (xmax - xmin) * scale) / 2, (100 - (ymax - ymin) * scale) / 2
    for fraction in (0.17, 0.37, 0.67, 0.87):
        point = line.p1 + line.v * fraction
        origin = point + plane.n * 100
        hit = slab.geometry.intersect_line_ray(Ray3D(origin, -plane.n))
        expected = '#ff0000' if hit is not None and \
            origin.distance_to_point(hit) < 100 - 1e-7 else '#0000ff'
        p = plane.xyz_to_xy(point)
        actual = _paint_at(result, (sign * p.x - xmin) * scale + cx,
                           (ymax - sign * p.y) * scale + cy)
        assert actual == expected, (view, fraction, actual, expected)


@pytest.mark.parametrize('mesh', [False, True])
@pytest.mark.parametrize('interactive', [False, True])
def test_analysis_geometry_keeps_values_and_visibility(mesh, interactive):
    """Analysis faces and mesh cells must keep both their colors and hover values."""
    a = _face([(0, 7, 5), (10, 7, 5), (10, 8, 5), (0, 8, 5)], (255, 0, 0)).geometry
    b = _face([(2, 0, 0), (3, 0, 0), (3, 10, 10), (2, 10, 10)], (0, 0, 255)).geometry
    geometry = [a, b]
    if mesh:
        geometry = [Mesh3D(g.vertices, [(0, 1, 2, 3)]) for g in geometry]
    data = VisualizationData([10, 20])
    analysis = AnalysisGeometry('data', geometry, [data])
    vis = VisualizationSet('analysis', [analysis])
    before = vis.to_dict()
    result = vis.to_svg(100, 100, margin=0, interactive=interactive,
                        render_2d_legend=True)
    assert _paint_at(result, 25, 25) == data.value_colors[1].to_hex()
    assert vis.to_dict() == before
    if interactive:
        xml = ElementTree.fromstring(result.as_str())
        assert '20' in [e.text for e in xml.iter('{http://www.w3.org/2000/svg}title')]


@pytest.mark.parametrize('view', list(VisualizationSet.VIEW_MAP))
def test_views_against_ray_intersections(view):
    """Compare SVG visibility to independent 3D intersections over nine views."""
    faces = [
        _face([(0, 0, 3), (10, 0, 3), (10, 10, 3), (0, 10, 3)], (255, 0, 0)),
        _face([(1, 0, 0), (9, 0, 8), (9, 10, 8), (1, 10, 0)], (0, 0, 255)),
        _face([(0, 2, 0), (10, 2, 0), (10, 8, 9), (0, 8, 9)], (0, 255, 0))]
    vis = VisualizationSet('views', [ContextGeometry('planes', faces)])
    result = vis.to_svg(100, 100, margin=0, view=view)
    plane = VisualizationSet.VIEW_MAP[view]
    projected = [plane.xyz_to_xy(p) for f in faces for p in f.geometry.boundary]
    sign = 1 if view == 'Top' else -1
    xs, ys = [sign * p.x for p in projected], [sign * p.y for p in projected]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    scale = 100 / max(xmax - xmin, ymax - ymin)
    cx, cy = (100 - (xmax - xmin) * scale) / 2, (100 - (ymax - ymin) * scale) / 2
    for i in range(9):
        for j in range(9):
            x = xmin + (i + 0.371) * (xmax - xmin) / 9
            y = ymin + (j + 0.619) * (ymax - ymin) / 9
            origin = plane.xy_to_xyz(Point2D(sign * x, sign * y)) + plane.n * 100
            ray = Ray3D(origin, -plane.n)
            hits = []
            for face in faces:
                hit = face.geometry.intersect_line_ray(ray)
                if hit is not None:
                    hits.append((origin.distance_to_point(hit), face.color.to_hex()))
            expected = min(hits)[1] if hits else None
            actual = _paint_at(result, (x - xmin) * scale + cx,
                               (ymax - y) * scale + cy)
            assert actual == expected, (view, x, y, actual, expected)
