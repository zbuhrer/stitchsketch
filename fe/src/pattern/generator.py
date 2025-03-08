import numpy as np


class PatternGenerationError(Exception):
    """Custom exception for pattern generation errors."""
    pass


def generate_cuttable_pattern(mesh_data, region_indices, scale=1.0):
    """
    Generates a cuttable pattern from a selected region of a 3D mesh.

    Args:
        mesh_data (dict): A dictionary containing mesh data, including:
            - vertices (np.ndarray): A numpy array of vertex coordinates (Nx3).
            - faces (np.ndarray): A numpy array of face indices (Mx3).
        region_indices (list): A list of face indices representing the selected region.
        scale (float): Scaling factor for the pattern.

    Returns:
        list: A list of 2D points representing the cuttable pattern.
              Returns an empty list if the region is invalid or the mesh data is incomplete.

    Raises:
        PatternGenerationError: If there are issues with the input data or during pattern generation.
    """
    if not isinstance(mesh_data, dict):
        raise PatternGenerationError("mesh_data must be a dictionary.")

    if "vertices" not in mesh_data or "faces" not in mesh_data:
        raise PatternGenerationError(
            "mesh_data must contain 'vertices' and 'faces' keys.")

    vertices = mesh_data["vertices"]
    faces = mesh_data["faces"]

    if not isinstance(vertices, np.ndarray) or not isinstance(faces, np.ndarray):
        raise PatternGenerationError(
            "Vertices and faces must be numpy arrays.")

    if len(region_indices) == 0:
        raise PatternGenerationError("No region indices provided.")

    # Extract the vertices and faces for the selected region.
    region_faces = faces[region_indices]

    # Find unique vertices in the selected region
    region_vertex_indices = np.unique(region_faces.flatten())
    region_vertices = vertices[region_vertex_indices]

    # Simple placeholder for pattern generation: Scale vertices and project to 2D (XY plane)
    pattern = region_vertices[:, :2] * scale

    # Convert to list of lists for easier handling in Streamlit
    pattern_list = pattern.tolist()

    return pattern_list
