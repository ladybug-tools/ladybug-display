# coding=utf-8
"""Order planar SVG geometry without sampling its projected overlap."""
from copy import copy

from ladybug_geometry.geometry3d import Face3D, Mesh3D, Polyface3D, Point3D, \
    LineSegment3D, Polyline3D
from .geometry3d import DisplayFace3D
import ladybug_display.svg as svg


def geometry_elements(geometry, element, display_mode=None):
    """Pair unprojected geometry with its already styled SVG elements."""
    raw = getattr(geometry, 'geometry', geometry)
    mode = display_mode or getattr(geometry, 'display_mode', 'Surface')
    if mode == 'Points':
        points = raw.face_centroids if isinstance(raw, Mesh3D) else \
            raw.vertices if isinstance(raw, (Face3D, Polyface3D)) else None
        if points is not None:
            circles = [e for e in element.elements if isinstance(e, svg.Circle)]
            return [(p, _group_child(element, e)) for p, e in zip(points, circles)], [
                e for e in element.elements if isinstance(e, svg.Style)]
    if isinstance(raw, Face3D):
        if mode in ('Wireframe', 'SurfaceWithEdges'):
            groups = []
            outlines = element.elements
            if mode == 'SurfaceWithEdges':
                groups.append((raw, _group_child(element, outlines[0])))
                outlines = outlines[1:]
            for boundary, outline in zip([raw.boundary] + list(raw.holes or []), outlines):
                for line, child in _outline_edges(boundary, outline):
                    groups.append((line, _group_child(element, child)))
            return groups, []
        return [(raw, element)], []
    if isinstance(raw, Mesh3D):
        children = [e for e in element.elements if not isinstance(e, svg.Style)]
        faces = [Face3D(vertices) for vertices in raw.face_vertices]
        groups = []
        for face, child in zip(faces, children):
            if mode != 'Wireframe':
                fill = copy(child)
                fill.stroke = None
                groups.append((face, _group_child(element, fill)))
            if mode in ('Wireframe', 'SurfaceWithEdges'):
                for line, edge in _outline_edges(face.boundary, child):
                    groups.append((line, _group_child(element, edge)))
        return groups, [e for e in element.elements if isinstance(e, svg.Style)]
    if isinstance(raw, Polyface3D):
        groups, start = [], 0
        for face in raw.faces:
            count = len(DisplayFace3D.face3d_to_svg(face, mode).elements)
            group = copy(element)
            group.elements = element.elements[start:start + count] + [
                e for e in element.elements if isinstance(e, svg.Title)]
            groups.extend(geometry_elements(face, group, mode)[0])
            start += count
        return groups, []
    if isinstance(raw, (LineSegment3D, Point3D)):
        return [(raw, element)], []
    if isinstance(raw, Polyline3D) and not raw.interpolated:
        segments = []
        for i, segment in enumerate(raw.segments):
            line = svg.Line(x1=element.points[2 * i], y1=element.points[2 * i + 1],
                            x2=element.points[2 * i + 2], y2=element.points[2 * i + 3])
            for attribute in ('stroke', 'stroke_width', 'stroke_dasharray', 'opacity'):
                setattr(line, attribute, getattr(element, attribute, None))
            segments.append((segment, line))
        return segments, []
    # Curves and text keep their reference-point depth; 2D graphics remain overlays.
    anchor = getattr(raw, 'center', getattr(getattr(raw, 'plane', None), 'o', None))
    if isinstance(anchor, Point3D):
        return [(anchor, element)], []
    return [], [element]


def _group_child(parent, child):
    group = copy(parent)
    group.elements = [child] + [e for e in parent.elements if isinstance(e, svg.Title)]
    return group


def _outline_edges(boundary, outline):
    """Keep boundary edges as 3D lines, including faces seen edge-on."""
    points = list(zip(outline.points[::2], outline.points[1::2]))
    for i, point in enumerate(boundary):
        j = (i + 1) % len(boundary)
        segment = LineSegment3D.from_end_points(point, boundary[j])
        line = svg.Line(x1=points[i][0], y1=points[i][1],
                        x2=points[j][0], y2=points[j][1])
        for attribute in ('stroke', 'stroke_width', 'stroke_dasharray', 'opacity'):
            setattr(line, attribute, getattr(outline, attribute, None))
        yield segment, line


def ordered_geometry(items, direction, tolerance):
    """Yield back-to-front geometry from an iterative binary space partition.

    A partition plane separates complete polygons, including pairs whose overlap
    contains none of their vertices. Polygons crossing a partition are split with
    their partition plane. This also breaks cyclic occlusion and intersections.
    Coplanar fills keep their input paint order, followed by their visible edges.
    """
    # Edge-on fills cover no screen area; their separately collected edges stay.
    items = [item for item in _planar_geometry(items, tolerance)
             if not isinstance(item[0], Face3D) or item[0].normal.dot(direction) != 0]
    stack = [(items, False)]
    while stack:
        current, emit = stack.pop()
        if emit or len(current) < 2:
            for item in current:
                yield item
            continue
        faces = [(i, item[0]) for i, item in enumerate(current)
                 if isinstance(item[0], Face3D)]
        if not faces:
            for item in sorted(current, key=lambda item: sum(
                    p.dot(direction) for p in _vertices(item[0])) / len(_vertices(item[0]))):
                yield item
            continue
        # Large projected faces reduce unnecessary cuts; break ties at the middle
        # to keep already ordered parallel surfaces from building a deep tree.
        middle = len(current) // 2
        splitter = max(faces, key=lambda pair: (
            abs(pair[1].normal.dot(direction)) * pair[1].area,
            -abs(pair[0] - middle)))[1]
        plane = splitter.plane
        front, back, coplanar = [], [], []
        for geometry, element in current:
            if geometry is splitter:
                coplanar.append((geometry, element))
                continue
            distances = _plane_distances(_vertices(geometry), plane)
            low, high = min(distances), max(distances)
            if low < -tolerance and high > tolerance:
                if isinstance(geometry, LineSegment3D):
                    ratio = distances[0] / (distances[0] - distances[1])
                    point = geometry.p1 + geometry.v * ratio
                    parts = [(LineSegment3D.from_end_points(geometry.p1, point),
                              distances[0] > 0),
                             (LineSegment3D.from_end_points(point, geometry.p2),
                              distances[1] > 0)]
                else:
                    parts = _split_face(geometry, plane, tolerance)
                for part, positive in parts:
                    side = front if positive else back
                    side.append((part, element))
            elif low >= -tolerance and high <= tolerance:
                if isinstance(geometry, Face3D):
                    coplanar.append((geometry, element))
                else:
                    # Shared boundary edges must also follow coplanar faces in
                    # the near subtree, not just the faces at this partition.
                    side = front if plane.n.dot(direction) >= 0 else back
                    side.append((geometry, element))
            elif low >= -tolerance:
                front.append((geometry, element))
            else:
                back.append((geometry, element))
        far, near = (back, front) if plane.n.dot(direction) >= 0 else (front, back)
        stack.append((near, False))
        stack.append((coplanar, True))
        stack.append((far, False))


def _planar_geometry(items, tolerance):
    """Derive partition planes from vertices, not rounded serialized metadata."""
    result = []
    for geometry, element in items:
        if isinstance(geometry, Face3D) and not geometry.check_planar(tolerance, False):
            geometry = Face3D(geometry.boundary, holes=geometry.holes)
            if not geometry.check_planar(tolerance, False):
                # Use SDK triangle indices with original 3D vertices; projecting
                # a genuinely warped face onto its plane would change its depth.
                vertices = {geometry.plane.xyz_to_xy(p): p for p in geometry.vertices}
                mesh = geometry.triangulated_mesh2d
                for indices in mesh.faces:
                    triangle = Face3D(tuple(vertices[mesh.vertices[i]] for i in indices))
                    result.append((triangle, element))
                continue
        result.append((geometry, element))
    return result


def _vertices(geometry):
    if isinstance(geometry, Face3D):
        return geometry.boundary
    if isinstance(geometry, LineSegment3D):
        return (geometry.p1, geometry.p2)
    return (geometry,)


def _plane_distances(vertices, plane):
    """Evaluate signed distances without allocating a vector for every vertex."""
    nx, ny, nz = plane.n
    ox, oy, oz = plane.o
    return [(p.x - ox) * nx + (p.y - oy) * ny + (p.z - oz) * nz for p in vertices]


def _split_face(face, plane, tolerance):
    """Clip convex boundaries using signed distances, including on-plane vertices.

    The SDK triangulates concave faces and holes before clipping. Direct clipping
    avoids the line-intersection ambiguity at existing collinear boundary vertices.
    """
    boundaries = [face.boundary] if face.is_convex and not face.has_holes else \
        face.triangulated_mesh3d.face_vertices
    for boundary in boundaries:
        distances = _plane_distances(boundary, plane)
        for positive in (False, True):
            sign = 1 if positive else -1
            points = []
            for i, point in enumerate(boundary):
                previous = boundary[i - 1]
                a, b = sign * distances[i - 1], sign * distances[i]
                # Snap classification, not coordinates, within numerical tolerance.
                a = 0 if abs(a) <= tolerance else a
                b = 0 if abs(b) <= tolerance else b
                if (a < 0 < b) or (b < 0 < a):
                    points.append(previous + (point - previous) * (a / (a - b)))
                if b >= 0:
                    points.append(point)
            if len(points) >= 3:
                part = Face3D(points, plane=face.plane)
                if part.area > tolerance * tolerance:
                    yield part, positive


def geometry_clip(geometries, element, project_point, identifier):
    """Clip the original SVG, preserving holes and avoiding artificial cut edges."""
    commands = []
    rings = []
    for geometry in geometries:
        if isinstance(geometry, LineSegment3D):
            x1, y1 = project_point(geometry.p1)
            x2, y2 = project_point(geometry.p2)
            dx, dy = x2 - x1, y2 - y1
            length = (dx * dx + dy * dy) ** 0.5
            stroke = element
            while not isinstance(stroke, svg.Line) and stroke.elements:
                stroke = stroke.elements[0]
            width = (getattr(stroke, 'stroke_width', None) or 1) + 1
            nx, ny = (-dy * width / length, dx * width / length) if length else (width, 0)
            rings.append([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny),
                          (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)])
        else:
            rings.extend([[project_point(p) for p in ring]
                          for ring in [geometry.boundary] + list(geometry.holes or [])])
    for ring in rings:
        for i, (x, y) in enumerate(ring):
            commands.append(svg.MoveTo(x=x, y=y) if i == 0 else svg.LineTo(x=x, y=y))
        commands.append(svg.ClosePath())
    path = svg.Path(d=commands)
    path.clip_rule = 'evenodd'
    clip = svg.ClipPath(clipPathUnits='userSpaceOnUse')
    clip.id = identifier
    clip.elements = [path]
    return clip
