"""Wrapper for COLMAP functionality."""

import subprocess
import shutil
from pathlib import Path
from typing import Optional, Callable
import logging
import os
import tempfile

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
    camera_model: str = "SIMPLE_RADIAL",
    progress_callback: Optional[Callable[[float, str], None]] = None,
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
        progress_callback: Optional callback function to report progress.  Takes a float (0-100) and a message string.

    Raises:
        COLMAPError: If any COLMAP command fails.
    """

    # Create temporary directory for COLMAP processing
    with tempfile.TemporaryDirectory() as colmap_temp_dir:
        colmap_temp_path = Path(colmap_temp_dir)

        # Use the temporary directory for the database and sparse reconstruction
        database_path = str(colmap_temp_path / "colmap.db")
        sparse_dir = str(colmap_temp_path / "sparse")

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
            matcher_command = "vocab_tree_matcher"
        else:
            matcher_command = "exhaustive_matcher"

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
                    matcher_command,
                    "--database_path",
                    database_path,
                    *feature_matcher_args
                ],
            ),
            (
                "Map creation",
                [
                    "colmap",
                    "mapper",
                    "--database_path",
                    database_path,
                    "--image_path",
                    image_dir,
                    "--output_path",
                    sparse_dir,
                ],
            ),
            (
                "Model to ply",
                [
                    "colmap",
                    "model_converter",
                    "--input_path",
                    os.path.join(sparse_dir, "0"),
                    "--output_path",
                    os.path.join(sparse_dir, "model.ply"),
                    "--output_type",
                    "PLY"
                ],
            ),
        ]

        # Execute COLMAP commands
        for name, command in commands:
            logging.info(f"Running COLMAP command: {name}")
            logging.info(f"Command: {' '.join(command)}")  # Log the full command
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                logging.error(result.stderr)  # Log standard error
                raise COLMAPError(
                    f"COLMAP command '{name}' failed with return code {result.returncode}: {result.stderr}")
            logging.info(result.stdout)  # Log standard output


def create_empty_colmap_database(database_path: str) -> None:
    """Creates an empty COLMAP database."""
    try:
        result = subprocess.run(
            ["colmap", "database_creator",
                "--database_path", database_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise COLMAPError(
                f"Failed to create empty COLMAP database: {result.stderr}")

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
