import os
from typing import Callable, Optional
from src.photogrammetry import colmap_wrapper  # Import colmap_wrapper
import streamlit as st

def run_reconstruction(image_dir: str, progress_callback: Optional[Callable[[float, str], None]] = None) -> Optional[str]:
    """
    Runs the COLMAP reconstruction pipeline.

    Args:
        image_dir: Path to the directory containing the images.
        progress_callback: Optional callback function to report progress.

    Returns:
        Path to the generated model.ply file, or None if reconstruction fails.
    """
    database_path = os.path.join(st.session_state.user_data_dir, "database.db")
    sparse_dir = os.path.join(st.session_state.user_data_dir, "sparse")
    ply_path = os.path.join(sparse_dir, "aligned", "model.ply") # Define ply_path here

    try:
        if progress_callback:
            progress_callback(5, "Creating COLMAP database...")
        colmap_wrapper.create_empty_colmap_database(database_path)

        if progress_callback:
            progress_callback(10, "Running COLMAP reconstruction...")
        colmap_wrapper.run_colmap(image_dir, database_path, sparse_dir)

        if os.path.exists(ply_path):
            return ply_path
        else:
            return None

    except Exception as e:
        print(f"Reconstruction failed: {e}")
        return None
