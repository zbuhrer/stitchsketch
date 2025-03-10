import streamlit as st
import time
from src.task_queue import submit_task, get_task_status, get_task_result, generate_task_id
from src.photogrammetry import reconstruction  # Import reconstruction.py
from src.photogrammetry.colmap_wrapper import COLMAPError
from typing import Callable, Optional
import os
import tempfile
import shutil
import logging
from pathlib import Path

MESH_PERSISTENCE_DIR = "persistent_meshes"


def perform_long_running_task(task_id: str, user_data_dir: str, colmap_temp_dir: str, progress_callback: Optional[Callable[[float, str], None]] = None):
    """Runs the COLMAP reconstruction pipeline within a temporary directory."""
    logging.info("perform_long_running_task started")
    image_dir = os.path.join(user_data_dir, "images")
    database_path = os.path.join(colmap_temp_dir, "database.db")  # Create db in temp dir
    sparse_dir = os.path.join(colmap_temp_dir, "sparse")          # Create sparse in temp dir
    os.makedirs(sparse_dir, exist_ok=True)                         # Ensure sparse dir exists

    try:
        logging.info(f"Calling reconstruction.run_reconstruction with image_dir={image_dir}, database_path={database_path}, sparse_dir={sparse_dir}")
        result = reconstruction.run_reconstruction(image_dir, database_path, sparse_dir, progress_callback)
        if result:
            logging.info(f"Reconstruction succeeded, result={result}")

            # Create the persistence directory
            task_persistence_dir = os.path.join(MESH_PERSISTENCE_DIR, task_id)
            os.makedirs(task_persistence_dir, exist_ok=True)

            # Construct the path to the persisted .ply file
            persisted_ply_path = os.path.join(task_persistence_dir, "model.ply") # No longer nested in "sparse"

            # Copy only the .ply file to the persistence directory
            ply_src_path = os.path.join(sparse_dir, "model.ply")
            try:
                shutil.copy2(ply_src_path, persisted_ply_path)
            except Exception as e:
                logging.error(f"Error copying {ply_src_path} to {persisted_ply_path}: {e}")

            logging.info(f"Model persisted to {persisted_ply_path}")
            return persisted_ply_path  # Return the path in the persistent directory
        else:
            logging.warning("Reconstruction returned None")
            return None

    except COLMAPError as e:
        logging.error(f"COLMAP Reconstruction failed: {e}")
        if progress_callback:
            progress_callback(0, f"COLMAP Reconstruction failed: {e}")  # Notify UI
        return None # Return None in case of failure
    except Exception as e:
        logging.exception(f"Reconstruction failed: {e}")
        if progress_callback:
            progress_callback(0, f"Reconstruction failed: {e}")  # Notify UI
        return None # Return None in case of failure
    finally:
        logging.info("perform_long_running_task finished")

def show():
    st.header("3D Reconstruction")

    # --- Display uploaded images ---
    if "uploaded_files" in st.session_state and st.session_state.uploaded_files:
        st.subheader("Uploaded Images")
        cols = st.columns(4)
        num_images = len(st.session_state.uploaded_files)
        for i, file_path in enumerate(st.session_state.uploaded_files[:8]):  # Limit to 8 images
            cols[i % 4].image(file_path, width=150)

        if num_images > 8:
            st.write(f"Showing the first 8 of {num_images} images.")
    else:
        st.info("No images uploaded yet. Please upload images on the 'Upload Images/Video' page.")
    # --- End display uploaded images ---

    if "reconstruction_task_id" not in st.session_state:
        st.session_state.reconstruction_task_id = None

    # Disable the button if no images are uploaded or a task is running
    disable_start = not st.session_state.get("uploaded_files") or st.session_state.reconstruction_task_id is not None

    # Create persistent mesh directory if it doesn't exist
    os.makedirs(MESH_PERSISTENCE_DIR, exist_ok=True)

    # Submit task
    if st.button("Start Reconstruction", disabled=disable_start):
        logging.info("Submitting task...")

        # Clean up previous temp dir if it exists
        if st.session_state.get("colmap_temp_dir") and Path(st.session_state.colmap_temp_dir).exists():
            logging.info(f"Cleaning up previous temp dir: {st.session_state.colmap_temp_dir}")
            shutil.rmtree(st.session_state.colmap_temp_dir)

        # create a temp dir at session state
        temp_dir = tempfile.mkdtemp()
        st.session_state.colmap_temp_dir = temp_dir

        # Generate a unique task ID
        st.session_state.task_id = generate_task_id()

        task_id = submit_task(
            perform_long_running_task,
            [st.session_state.task_id, str(st.session_state.user_data_dir), st.session_state.colmap_temp_dir],
            {}
        )

        st.session_state.reconstruction_task_id = task_id

        logging.info(f"Task submitted with id: {st.session_state.reconstruction_task_id}")
        st.rerun()

    # **Display task status for *this* user session only**
    st.subheader("Task Status")  # Added section for task status
    with st.container():  # Use a container for layout
        if st.session_state.reconstruction_task_id:  # Check if task_id is not None
            display_task_status(st.session_state.reconstruction_task_id)
        else:
            st.write("No reconstruction task submitted yet.")


def display_task_status(task_id: str):
    """Displays task status information."""
    logging.info(f"display_task_status called with task_id: {task_id}")
    if task_id:
        status = get_task_status(task_id)
        logging.info(f"Task status: {status}")

        # Show only tasks from this session
        if status and status["user_session_id"] == st.session_state.session_id:
            st.write(f"Task ID: {task_id}")
            st.write(f"Status: {status['status']}")
            st.progress(status['progress'])
            st.write(f"Message: {status['message']}")

            if status["status"] == "completed":
                result = get_task_result(task_id)
                if result:
                    st.success(f"Reconstruction complete! Model saved to: {result}")
                    st.session_state.mesh_path = result  # Store the mesh path
                    st.session_state.mesh_id = "some_mesh_id"  # Fake ID, but non-null

                    # Clean up any old runs, or failed attempts, for this session.
                    if st.session_state.get("colmap_temp_dir") and Path(st.session_state.colmap_temp_dir).exists():
                        logging.info(f"Cleaning up temp dir: {st.session_state.colmap_temp_dir}")
                        shutil.rmtree(st.session_state.colmap_temp_dir)

                else:
                    st.error("Reconstruction failed to produce a model.")

                # Enable next step button, display results, etc.
                st.session_state.reconstruction_task_id = None  # Clear task id
                if st.session_state.get("last_status") != status["status"]:
                    st.session_state["last_status"] = status["status"]

            elif status["status"] == "failed":
                st.error(f"Reconstruction failed: {status['message']}")

                # Clean up any old runs, or failed attempts, for this session.
                if st.session_state.get("colmap_temp_dir") and Path(st.session_state.colmap_temp_dir).exists():
                    logging.info(f"Cleaning up temp dir: {st.session_state.colmap_temp_dir}")
                    shutil.rmtree(st.session_state.colmap_temp_dir)

                st.session_state.reconstruction_task_id = None  # Clear task id
                if st.session_state.get("last_status") != status["status"]:
                    st.session_state["last_status"] = status["status"]

            else:
                time.sleep(1)  # Poll every second
                st.rerun()
        elif status:
            # Indicate task ownership
            st.warning("This task belongs to a different session.")
        else:
            st.warning("Task status not found.")
