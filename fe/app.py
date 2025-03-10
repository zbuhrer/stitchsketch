import streamlit as st
from ui.pages import upload, reconstruction, segmentation, pattern
from src.session import initialize_session
from src.task_queue import start_workers
from ui import state
import shutil
import os

# Initialize session state and start workers


def init():
    try:
        # Initialize session state using src/session.py
        if "initialized" not in st.session_state:
            initialize_session()
            st.session_state.initialized = True

            # Initialize or retrieve number of workers from the session state
            if "num_workers" not in st.session_state:
                st.session_state.num_workers = 2  # Default number of workers

            # Start background workers using src/task_queue.py
            st.session_state.workers = start_workers(
                num_workers=st.session_state.num_workers)
        st.session_state.initialization_successful = True  # Set success flag
    except Exception as e:
        st.error(f"Application initialization failed: {e}")
        st.session_state.initialization_successful = False

# Main application


def main():
    st.set_page_config(
        page_title="Photogrammetry Pattern Generator",
        page_icon="🧵",
        layout="wide",
    )

    init()

    if not st.session_state.get("initialization_successful", True):
        st.warning("Initialization failed")
        return

    # Application header
    st.title("Photogrammetry Pattern Generator")

    # Initialize state
    app_state = state.PageState()

    # Navigation
    pages = {
        "Upload Images/Video": upload,
        "3D Reconstruction": reconstruction,
        "Mesh Segmentation": segmentation,
        "Pattern Generation": pattern
    }

    # Sidebar navigation
    MESH_PERSISTENCE_DIR = "persistent_meshes"

    with st.sidebar:
        st.header("Navigation")
        try:
            if "selected_page" not in st.session_state:
                # Load from PageState default
                st.session_state.selected_page = app_state.current_page
            st.radio("Choose a page", list(pages.keys()), key="selected_page", index=list(
                pages.keys()).index(st.session_state.selected_page))
        except Exception as e:
            st.error(f"Navigation setup in the sidebar failed: {e}")
            return

        # Debugging: Display session state
        with st.expander("Session State (Debug)"):
            st.write(st.session_state)

    # Display current page
    try:
        current_page = pages[st.session_state.selected_page]
        current_page.show()
    except Exception as e:
        st.error(
            f"Displaying page {st.session_state.selected_page} failed: {e}")
        return

    # Session End Cleanup
    if st.session_state.get("is_session_end", False):
        user_session_dir = os.path.join(MESH_PERSISTENCE_DIR, st.session_state.session_id)
        if os.path.exists(user_session_dir):
            shutil.rmtree(user_session_dir, ignore_errors=True)
            print(f"Cleaned up persistent mesh directory: {user_session_dir}")
        else:
            print("No persistent mesh directory found for this session.")

        # Clear only specific session state variables related to reconstruction
        keys_to_clear = [
            "reconstruction_task_id",
            "mesh_path",
            "mesh_id",
            "colmap_temp_dir",
            "last_status",
            "is_session_end"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

        st.stop()  # Stop the Streamlit app after cleanup

    # Add a flag to indicate session end (e.g., when the user closes the browser)
    # For demonstration, a button is used here.  In a real application,
    # you would likely use a different mechanism to detect session end.
    if st.button("End Session and Cleanup"):
        st.session_state["is_session_end"] = True
        st.rerun()


if __name__ == "__main__":
    main()
