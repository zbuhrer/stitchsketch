import streamlit as st
from ui.pages import upload, reconstruction, segmentation, pattern
from src.session import initialize_session
from src.task_queue import start_workers
from ui import state

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
    with st.sidebar:
        st.header("Navigation")
        try:
            if "selected_page" not in st.session_state:
                # Load from PageState default
                st.session_state.selected_page = app_state.current_page
            selected_page = st.radio("Choose a page", list(pages.keys()), key="selected_page", index=list(
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


if __name__ == "__main__":
    main()
