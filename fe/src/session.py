import streamlit as st
from pathlib import Path
import tempfile
import os
import shutil
import uuid  # Import uuid


def initialize_session():
    """Initialize session state variables"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(
            uuid.uuid4())  # Generate a session ID

    if "user_data_dir" not in st.session_state:
        # Create temporary directory for user data
        temp_dir = Path(tempfile.mkdtemp())
        st.session_state.user_data_dir = temp_dir

        # Create subdirectories
        (temp_dir / "images").mkdir(exist_ok=True)
        (temp_dir / "reconstructions").mkdir(exist_ok=True)
        (temp_dir / "patterns").mkdir(exist_ok=True)

    # Initialize key state variables
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if "reconstruction_task_id" not in st.session_state:
        st.session_state.reconstruction_task_id = None

    if "mesh_id" not in st.session_state:
        st.session_state.mesh_id = None

    if "selected_regions" not in st.session_state:
        st.session_state.selected_regions = []

    if "patterns" not in st.session_state:
        st.session_state.patterns = []


def cleanup_session():
    """Clean up session data when session ends"""
    if "user_data_dir" in st.session_state:
        try:
            shutil.rmtree(st.session_state.user_data_dir)
        except Exception as e:
            print(f"Error cleaning up session data: {e}")
