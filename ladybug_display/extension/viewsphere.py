"""Method to draw a ViewSphere as a VisualizationSet."""
from ladybug_geometry.geometry3d import Point3D, Ray3D, Mesh3D
from ladybug.legend import LegendParameters
from ladybug.color import Colorset
from ladybug.datatype.distance import Distance

from ..geometry3d.ray import DisplayRay3D
from ..visualization import VisualizationSet, AnalysisGeometry, VisualizationData, \
    ContextGeometry


def view_sphere_to_vis_set(
        view_sphere, view_type='HorizontalRadial', resolution=1,
        center_point=Point3D(0, 0, 0), context_intersect_dist=None,
        dist_units='m', radius=1, legend_parameters=None, draw_view_rays=True):
    """Translate a Ladybug ViewSphere object into Display geometry.

    Args:
        view_sphere: A Ladybug ViewSphere object to be converted to display geometry.
        view_type: Text for the type of view analysis to conduct. Choose from
            the following options. (Default: HorizontalRadial)

            * HorizontalRadial - The percentage of the 360 horizontal view
                plane that is not blocked by the context geometry.
            * Horizontal30DegreeOffset - The percentage of the 360 horizontal
                view band bounded on top and bottom by a 30 degree offset from
                the horizontal plane. 30 degrees corresponds roughly to the
                vertical limit of human peripheral vision.
            * Spherical - The percentage of the sphere surrounding each of
                the test points that is not blocked by context geometry. This
                is equivalent to a solid angle and gives equal weight to all
                portions of the sphere.
            * SkyExposure - The percentage of the sky that is visible from
                each of the the test points.

        resolution: A positive integer for the number of times that the original
            view vectors are subdivided. For a circle, 1 indicates that 72
            evenly-spaced vectors are used to describe a circle, 2 indicates
            that 144 vectors describe a circle, and each successive value will
            roughly double the number of view vectors used. For a dome, 1 indicates
            that 1225 are used to describe the dome, 2 indicates that 5040
            view vectors describe the some and each successive value will
            roughly quadruple the number of view vectors used. Setting this to
            a high value will result in a more accurate analysis but will take
            longer to run. (Default: 1).
        center_point: Point3D for the center of the view Sphere. (Default: (0, 0, 0)).
        context_intersect_dist: An optional list of positive numbers that align with
            the number of view vectors in the View Sphere, given the input view_type
            and resolution. If supplied, these will be used to color the view sphere
            with the distances to context geometry surrounding the center_point.
            This produces a graphic showing how open the view is around the center
            point. If None, the view sphere will have all one color and it will be
            assumed that the view sphere is being displayed primarily as a way
            to illustrate the view_type. (Default: None).
        dist_units: Text for the abbreviation of the units to be used in the
            view sphere visualization. (Default: m).
        radius: A number for the radius of the view sphere in Rhino model units.
            When a context_intersect_dist is supplied, this should be the maximum
            value of this list or the distance at which context is no longer
            able to block the view from the center point. (Default: 1).
        legend_parameters: Optional legend parameters that will be used to customize
            the display of the context_intersect_dist. (Default: None).
        draw_view_rays: Boolean to note whether a ContextGeometry should be included
            with the rays that are used to evaluate the view. (Default: True).

    Returns:
        A VisualizationSet with the ViewSphere represented as an AnalysisGeometry
        (and optionally a ContextGeometry if draw_view_rays is True). This includes these
        objects in the following order.

        -   View_Analysis -- A AnalysisGeometry for the View Sphere geometry. This will
            be colored with distances if context_intersect_dist is supplied.

        -   View_Rays -- A ContextGeometry for the rays used to evaluate view if
            draw_view_rays is True.

     """
    # get the view method from the view type
    center_types = ('HorizontalRadial', 'Horizontal30DegreeOffset')
    if view_type == 'HorizontalRadial':
        view_method = view_sphere.horizontal_circle_view_mesh
    elif view_type == 'Horizontal30DegreeOffset':
        view_method = view_sphere.horizontal_radial_view_mesh
    elif view_type == 'Spherical':
        view_method = view_sphere.sphere_view_mesh
    elif view_type in ('SkyExposure', 'SkyView'):
        view_method = view_sphere.dome_view_mesh
    else:
        raise ValueError('"{}" is not a recognized view type'.format(view_type))
    
    # compute the altitude and azimuth count from the resolution
    az_count = 72 * resolution
    alt_count = 6 * resolution if view_type == 'Horizontal30DegreeOffset' \
        else 18 * resolution

    # get the view vectors and mesh based on the inputs
    if view_type == 'HorizontalRadial':
        study_mesh, view_vecs = view_method(
            center_point=center_point, radius=radius, azimuth_count=az_count)
    else:
        study_mesh, view_vecs = view_method(
            center_point=center_point, radius=radius,
            azimuth_count=az_count, altitude_count=alt_count)

    # if a context_intersect_dist is supplied, adjust the mesh based on the distance
    if context_intersect_dist is not None:
        results = context_intersect_dist
        move_vecs = [vec * -(radius - dist) for vec, dist, in zip(view_vecs, results)]
        new_verts = [center_point] if view_type in center_types else []
        iter_verts = study_mesh.vertices[1:] if view_type in center_types \
            else study_mesh.vertices
        for pt, mv in zip(iter_verts, move_vecs):
            new_verts.append(pt.move(mv))
        study_mesh = Mesh3D(new_verts, study_mesh.faces)
    else:
        results = [radius] * len(view_vecs)

    # add a value at the start to align with the vertices
    if view_type in center_types:
        avg_val = sum(results) / len(results)
        results.insert(0, avg_val)
    
    # create the AnalysisGeometry with the view sphere mesh
    l_par = LegendParameters() if legend_parameters is None else legend_parameters
    if l_par.are_colors_default:
        base_colors = Colorset.view_study()
        l_par.colors = base_colors if context_intersect_dist is not None else \
            [base_colors[-1], base_colors[-1]]
    vis_data = VisualizationData(results, l_par, Distance(), dist_units)
    mesh_geo = AnalysisGeometry('View_Analysis', [study_mesh], [vis_data])
    mesh_geo.display_name = 'View Analysis'
    vis_set = VisualizationSet('View_Rose', [mesh_geo])
    vis_set.display_name = 'View Rose'

    # add a context geometry for the view rays if requested
    if draw_view_rays:
        mesh_geo.display_mode = 'SurfaceWithEdges'
        base_pts = study_mesh.vertices[1:] if view_type in center_types \
            else study_mesh.vertices
        ray_len = radius / 10
        rays = []
        for pt, vec in zip(base_pts, view_vecs):
            rays.append(DisplayRay3D(Ray3D(pt, vec * ray_len)))
        ray_geo = ContextGeometry('View_Rays', rays)
        ray_geo.display_name = 'View Rays'
        vis_set.add_geometry(ray_geo)

    return vis_set