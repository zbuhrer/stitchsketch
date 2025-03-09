import os
from typing import Callable, Optional
from src.photogrammetry import colmap_wrapper  # Import colmap_wrapper


def run_reconstruction(image_dir: str, database_path: str, sparse_dir: str, progress_callback: Optional[Callable[[float, str], None]] = None) -> Optional[str]:
    """
    Runs the COLMAP reconstruction pipeline.

    Args:
        image_dir: Path to the directory containing the images.
        database_path: Path to the COLMAP database.
        sparse_dir: Path to the directory where the sparse reconstruction will be stored.
        progress_callback: Optional callback function to report progress.

    Returns:
        Path to the generated model.ply file, or None if reconstruction fails.
    """
    ply_path = os.path.join(sparse_dir, "model.ply") # Define ply_path here

    try:
        colmap_wrapper.create_empty_colmap_database(database_path)
        colmap_wrapper.run_colmap(image_dir, database_path, sparse_dir, progress_callback=progress_callback)

        if os.path.exists(ply_path):
            return ply_path
        else:
            return None

    except colmap_wrapper.COLMAPError as e:
        print(f"Reconstruction failed: {e}")
        return None
    except Exception as e:
        print(f"Reconstruction failed: {e}")
        return None
