"""Wrapper for COLMAP functionality."""

import subprocess
import shutil
from pathlib import Path
from typing import Optional
import logging
import os
import streamlit as st  # Import streamlit

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class COLMAPError(Exception):
    """Custom exception for COLMAP errors."""
    pass


def run_colmap(
    image_dir: str,
    database_path: str,
    sparse_dir: str,
    feature_type: str = "sift",
    vocab_tree_path: Optional[str] = None,
    camera_model: str = "perspective",
) -> None:
    """
    Runs the COLMAP pipeline.

    Args:
        image_dir: Path to the directory containing the images.
        database_path: Path to the COLMAP database.
        sparse_dir: Path to the directory where the sparse reconstruction will be stored.
        feature_type: Feature type to use (e.g., "sift", "orb").
        vocab_tree_path: Path to the vocabulary tree file (required for vocab_tree matching).
        camera_model: Camera model to use (e.g., "perspective", "radial").

    Raises:
        COLMAPError: If any COLMAP command fails.
    """

    # --- HARDCODED PATHS FOR TESTING (TASK 1.1) - REMOVE LATER ---
    image_dir = os.path.join(st.session_state.user_data_dir, "images")
    database_path = os.path.join(st.session_state.user_data_dir, "database.db")
    sparse_dir = os.path.join(st.session_state.user_data_dir, "sparse")
    logging.info(f"Using hardcoded paths for testing: image_dir={image_dir}, database_path={database_path}, sparse_dir={sparse_dir}")
    # --------------------------------------------------------------

    # Create sparse directory if it doesn't exist
    os.makedirs(sparse_dir, exist_ok=True)

    # Feature extraction settings
    feature_extractor_args = ["--ImageReader.camera_model", camera_model]
    if feature_type == "sift":
        pass  # Use default SIFT settings
    elif feature_type == "orb":
        feature_extractor_args += ["--SiftExtraction.use_gpu", "0",  # Disable GPU for more consistent operation
                                   "--SiftExtraction.num_octaves", "3",
                                   "--SiftExtraction.first_octave", "0",
                                   "--SiftExtraction.peak_threshold", "0.01",
                                   "--SiftExtraction.edge_threshold", "10"]
    else:
        raise ValueError(f"Unsupported feature type: {feature_type}")

    # Feature matching settings
    feature_matcher_args = []
    if vocab_tree_path:
        feature_matcher_args += ["--VocabTreeMatching.vocab_tree_path",
                                 str(vocab_tree_path)]

    # COLMAP commands
    commands = [
        (
            "Feature extraction",
            [
                "colmap",
                "feature_extractor",
                "--database_path",
                database_path,
                "--image_path",
                image_dir,
                *feature_extractor_args
            ],
        ),
        (
            "Vocabulary tree matching" if vocab_tree_path else "Sequential matching",
            [
                "colmap",
                "matcher",
                "--database_path",
                database_path,
                *feature_matcher_args
            ],
        ),
        (
            "Map creation",
            [
                "colmap",
                "map_creator",
                "--database_path",
                database_path,
                "--image_path",
                image_dir,
                "--output_path",
                sparse_dir,
            ],
        ),
        (
            "Bundle adjustment",
            [
                "colmap",
                "bundle_adjuster",
                "--input_path",
                os.path.join(sparse_dir, "0"),
                "--output_path",
                os.path.join(sparse_dir, "0"),
                "--database_path",
                database_path,
            ],
        ),
        (
            "Mapper",
            [
                "colmap",
                "mapper",
                "--database_path",
                database_path,
                "--image_path",
                image_dir,
                "--output_path",
                sparse_dir,
                "--Mapper.init_ba_refine_focal_length",
                "1",
                "--Mapper.ba_refine_principal_point",
                "1",
                "--Mapper.ba_refine_extra_params",
                "1"
            ],
        ),
        (
            "Merge models",
            [
                "colmap",
                "model_merger",
                "--input_path",
                sparse_dir,
                "--output_path",
                os.path.join(sparse_dir, "merged"),
            ],
        ),
        (
            "Bundle adjustment (merged)",
            [
                "colmap",
                "bundle_adjuster",
                "--input_path",
                os.path.join(sparse_dir, "merged"),
                "--output_path",
                os.path.join(sparse_dir, "merged"),
                "--database_path",
                database_path,
            ],
        ),
        (
            "Model filtering",
            [
                "colmap",
                "model_filterer",
                "--input_path",
                os.path.join(sparse_dir, "merged"),
                "--output_path",
                os.path.join(sparse_dir, "filtered"),
                "--database_path",
                database_path,
            ],
        ),
        (
            "Point triangulation",
            [
                "colmap",
                "point_triangulator",
                "--input_path",
                os.path.join(sparse_dir, "filtered"),
                "--output_path",
                os.path.join(sparse_dir, "filtered"),
                "--database_path",
                database_path,
            ],
        ),
        (
            "Model aligning",
            [
                "colmap",
                "model_aligner",
                "--input_path",
                os.path.join(sparse_dir, "filtered"),
                "--output_path",
                os.path.join(sparse_dir, "aligned"),
                "--ref_images_path",
                image_dir
            ],
        ),
        (
            "Model to ply",
            [
                "colmap",
                "model_converter",
                "--input_path",
                os.path.join(sparse_dir, "aligned"),
                "--output_path",
                os.path.join(sparse_dir, "aligned", "model.ply"),
                "--output_type",
                "PLY"
            ],
        ),
    ]

    # Execute COLMAP commands
    for name, command in commands:
        logging.info(f"Running COLMAP command: {name}")
        logging.info(f"Command: {' '.join(command)}")  # Log the full command
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            logging.info(result.stdout)  # Log standard output
        except subprocess.CalledProcessError as e:
            logging.error(e.stderr)  # Log standard error
            raise COLMAPError(f"COLMAP command '{name}' failed: {e}")


def create_empty_colmap_database(database_path: str) -> None:
    """Creates an empty COLMAP database."""
    database_path_path = Path(database_path)
    if database_path_path.exists():
        database_path_path.unlink()  # Remove existing database

    try:
        subprocess.run(
            ["colmap", "database_creator",
                "--database_path", database_path],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise COLMAPError(f"Failed to create empty COLMAP database: {e}")


def get_number_of_registered_images(sparse_dir: str) -> int:
    """
    Gets the number of registered images in the sparse reconstruction.

    Args:
        sparse_dir: Path to the directory containing the sparse reconstruction.

    Returns:
        The number of registered images.
    """
    sparse_dir_path = Path(sparse_dir)
    cameras_path = sparse_dir_path / "cameras.txt"
    images_path = sparse_dir_path / "images.txt"

    if not cameras_path.exists() or not images_path.exists():
        return 0

    num_registered_images = 0
    with open(str(images_path), "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                image_id = int(parts[0])
                if image_id > 0:
                    num_registered_images += 1
            except ValueError:
                continue

    return num_registered_images


def estimate_sparsity(sparse_dir: str) -> float:
    """
    Estimates the sparsity of the reconstructed model.

    Args:
        sparse_dir: Path to the directory containing the sparse reconstruction.

    Returns:
        The sparsity of the model (percentage of unregistered points).
    """
    sparse_dir_path = Path(sparse_dir)
    points3D_path = sparse_dir_path / "points3D.txt"

    if not points3D_path.exists():
        return 1.0  # Assume completely sparse if no points

    total_points = 0
    registered_points = 0
    with open(str(points3D_path), "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            total_points += 1
            parts = line.split()
            if len(parts) > 8:
                track_length = int(parts[7])
                if track_length > 0:
                    registered_points += 1

    if total_points == 0:
        return 1.0

    sparsity = 1.0 - (registered_points / total_points)
    return sparsity


def copy_colmap_model(src_dir: str, dst_dir: str) -> None:
    """
    Copies a COLMAP model from the source directory to the destination directory.

    Args:
        src_dir: Path to the source directory containing the COLMAP model.
        dst_dir: Path to the destination directory.
    """
    src_dir_path = Path(src_dir)
    dst_dir_path = Path(dst_dir)

    os.makedirs(dst_dir, exist_ok=True)

    files_to_copy = ["cameras.txt", "images.txt", "points3D.txt"]
    for file in files_to_copy:
        src_file = src_dir_path / file
        dst_file = dst_dir_path / file
        if src_file.exists():
            shutil.copy(str(src_file), str(dst_file))


def delete_colmap_model(model_dir: str) -> None:
    """
    Deletes a COLMAP model directory.

    Args:
        model_dir: Path to the directory containing the COLMAP model.
    """
    model_dir_path = Path(model_dir)
    if model_dir_path.exists():
        shutil.rmtree(model_dir)
