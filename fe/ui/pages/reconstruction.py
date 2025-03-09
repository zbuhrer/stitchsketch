import streamlit as st
import time
from src.task_queue import submit_task, get_task_status, get_task_result
from src.photogrammetry import reconstruction  # Import reconstruction.py
from typing import Callable, Optional
import os

def perform_long_running_task(user_data_dir: str, progress_callback: Optional[Callable[[float, str], None]] = None):
    """Runs the COLMAP reconstruction pipeline."""
    image_dir = os.path.join(user_data_dir, "images") # Use os.path.join for string paths
    database_path = os.path.join(user_data_dir, "database.db")
    sparse_dir = os.path.join(user_data_dir, "sparse")
    result = reconstruction.run_reconstruction(image_dir, database_path, sparse_dir, progress_callback)
    return result  # Return the path to the .ply file

def show():
    st.header("3D Reconstruction")

    if "reconstruction_task_id" not in st.session_state:
        st.session_state.reconstruction_task_id = None

    # Submit task
    if st.button("Start Reconstruction", disabled=st.session_state.reconstruction_task_id is not None):
        st.session_state.reconstruction_task_id = submit_task(
            perform_long_running_task, [str(st.session_state.user_data_dir)], {})
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
    if task_id:
        status = get_task_status(task_id)

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
                    st.session_state.mesh_id = "some_mesh_id" # Fake ID, but non-null
                else:
                    st.error("Reconstruction failed to produce a model.")


                # Enable next step button, display results, etc.
                st.session_state.reconstruction_task_id = None  # Clear task id
                st.rerun()

            elif status["status"] == "failed":
                st.error(f"Reconstruction failed: {status['message']}")
                st.session_state.reconstruction_task_id = None  # Clear task id
                st.rerun()
            else:
                time.sleep(1)  # Poll every second
                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
        elif status:
            # Indicate task ownership
            st.warning("This task belongs to a different session.")
        else:
            st.warning("Task status not found.")
