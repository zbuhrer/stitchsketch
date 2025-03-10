import os
from typing import Callable, Optional
from src.photogrammetry import colmap_wrapper  # Import colmap_wrapper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


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
    ply_path = os.path.join(sparse_dir, "model.ply")

    try:
        if progress_callback:
            progress_callback(0, "Creating empty COLMAP database...")
        colmap_wrapper.create_empty_colmap_database(database_path)

        if progress_callback:
            progress_callback(10, "Running COLMAP reconstruction...")
        colmap_wrapper.run_colmap(image_dir, database_path, sparse_dir, progress_callback=progress_callback)

        if os.path.exists(ply_path):
            if progress_callback:
                progress_callback(100, f"Reconstruction complete. Model saved to: {ply_path}")
            return ply_path
        else:
            logging.warning("Reconstruction failed: model.ply not found.")
            if progress_callback:
                progress_callback(0, "Reconstruction failed: model.ply not found.")
            return None

    except colmap_wrapper.COLMAPError as e:
        logging.error(f"COLMAP reconstruction failed: {e}")
        if progress_callback:
            progress_callback(0, f"COLMAP reconstruction failed: {e}")
        return None
    except Exception as e:
        logging.exception(f"An unexpected error occurred during reconstruction: {e}", exc_info=True)
        if progress_callback:
            progress_callback(0, f"An unexpected error occurred during reconstruction: {e}")
        return None
