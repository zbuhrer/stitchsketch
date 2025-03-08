import os
import subprocess
from typing import List, Optional, Tuple
import numpy as np
import pyvista as pv


def create_point_cloud(points: np.ndarray, colors: Optional[np.ndarray] = None) -> pv.PolyData:
    """
    Creates a PyVista point cloud from a NumPy array of points.

    Args:
        points: A NumPy array of shape (N, 3) representing the point coordinates.
        colors: An optional NumPy array of shape (N, 3) representing the point colors (RGB).

    Returns:
        A PyVista PolyData object representing the point cloud.
    """
    point_cloud = pv.PolyData(points)
    if colors is not None:
        point_cloud['colors'] = colors
        point_cloud.active_scalars_name = 'colors'
    return point_cloud


def create_mesh_from_points(points: np.ndarray, algorithm: str = "delaunay_3d") -> pv.PolyData:
    """
    Creates a mesh from a NumPy array of points using a specified meshing algorithm.

    Args:
        points: A NumPy array of shape (N, 3) representing the point coordinates.
        algorithm: The meshing algorithm to use. Options: "delaunay_3d", "alpha_shape".

    Returns:
        A PyVista PolyData object representing the mesh.
    """
    if algorithm == "delaunay_3d":
        cloud = pv.PolyData(points)
        mesh = cloud.delaunay_3d(alpha=1.0)  # Adjust alpha as needed
        return mesh
    elif algorithm == "alpha_shape":
        #  alpha shape meshing logic
        alpha = 0.5  # Tune this parameter
        mesh = pv.wrap(alpha_shape(points, alpha))
        return mesh
    else:
        raise ValueError(f"Unsupported meshing algorithm: {algorithm}")


def estimate_normals(mesh: pv.PolyData, point_cloud: pv.PolyData, orientation_point: Optional[np.ndarray] = None) -> pv.PolyData:
    """
    Estimates vertex normals for a PyVista mesh, orienting them consistently.

    Args:
        mesh: The PyVista mesh to estimate normals for.
        point_cloud: PyVista point cloud to base the normal orientation on.
        orientation_point: An optional point to orient all normals towards. If None, normals are oriented consistently
                           across the mesh.

    Returns:
        The PyVista mesh with estimated and oriented vertex normals.
    """
    mesh.compute_normals(cell_normals=False, point_normals=True, inplace=True)
    if orientation_point is not None:
        mesh.orient_normals(point=orientation_point, inplace=True)

    # Check normal orientation based on point cloud
    if point_cloud is not None and mesh.n_points > 0:
        dot_products = mesh.extract_points(range(min(1000, mesh.n_points))).compute_normals(
            cell_normals=False, point_normals=True).point_normals @ (point_cloud.center - mesh.center)
        if np.mean(dot_products) < 0:
            mesh.flip_normals(inplace=True)

    return mesh


def simplify_mesh(mesh: pv.PolyData, reduction: float = 0.5) -> pv.PolyData:
    """
    Simplifies a PyVista mesh by reducing the number of faces.

    Args:
        mesh: The PyVista mesh to simplify.
        reduction: The fraction of faces to remove (e.g., 0.5 removes 50% of the faces).

    Returns:
        The simplified PyVista mesh.
    """
    return mesh.decimate(target_reduction=reduction)


def smooth_mesh(mesh: pv.PolyData, iterations: int = 15) -> pv.PolyData:
    """
    Smooths a PyVista mesh using the Taubin smoothing algorithm.

    Args:
        mesh: The PyVista mesh to smooth.
        iterations: The number of smoothing iterations.

    Returns:
        The smoothed PyVista mesh.
    """
    return mesh.smooth(n_iter=iterations, pass_band=0.1)


def repair_mesh(mesh: pv.PolyData) -> pv.PolyData:
    """
    Repairs a mesh to remove self-intersections and other artifacts.
    """
    return mesh.eliminate_invalid_cells()


def export_mesh(mesh: pv.PolyData, filename: str) -> None:
    """
    Exports a PyVista mesh to a file.

    Args:
        mesh: The PyVista mesh to export.
        filename: The name of the file to export to (e.g., "mesh.stl", "mesh.obj").
    """
    mesh.save(filename)


def alpha_shape(points: np.ndarray, alpha: float) -> pv.UnstructuredGrid:
    """
    Compute the alpha shape (concave hull) of a set of points.
    """
    from scipy.spatial import Delaunay

    tri = Delaunay(points)
    tetrahedra = points[tri.simplices]
    # Find circumradius of each tetrahedron
    radii = np.array([circumradius(tetra) for tetra in tetrahedra])
    # Filter tetrahedra by radius
    alpha_shape_simplices = tri.simplices[radii < alpha]

    # Construct pyvista unstructured grid from remaining simplices
    alpha_shape = pv.UnstructuredGrid(points, alpha_shape_simplices)
    return alpha_shape


def circumradius(tetra: np.ndarray) -> float:
    """
    Calculates the circumradius of a tetrahedron.
    """
    a, b, c, d = tetra
    aa = np.sum((a - d)**2)
    bb = np.sum((b - d)**2)
    cc = np.sum((c - d)**2)
    # This should always be 0, but included for completeness
    dd = np.sum((d - d)**2)

    a_coeff = np.linalg.det(np.vstack((b-d, c-d, aa*np.ones(3))).T)
    b_coeff = np.linalg.det(np.vstack((c-d, a-d, bb*np.ones(3))).T)
    c_coeff = np.linalg.det(np.vstack((a-d, b-d, cc*np.ones(3))).T)
    # again, this is 0.
    d_coeff = np.linalg.det(np.vstack((a-d, c-d, dd*np.ones(3))).T)

    volume = np.linalg.det(np.vstack((a-d, b-d, c-d)).T)

    # handle degenerate cases
    if volume == 0:
        return np.inf

    circumradius = np.sqrt(
        (a_coeff**2 + b_coeff**2 + c_coeff**2 + d_coeff**2) / (36 * volume**2))
    return circumradius
