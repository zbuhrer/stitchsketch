import streamlit as st


def display_text(text: str):
    """Displays a simple text string."""
    st.write(text)


def display_button(label: str, key: str = None) -> bool:
    """Displays a button and returns True if clicked."""
    return st.button(label, key=key)


def file_uploader(label: str, type: list) -> st.runtime.uploaded_file_manager.UploadedFile:
    """Displays a file uploader."""
    return st.file_uploader(label, type=type)

# Example of a more complex component (Placeholder for 3D Viewer)


def placeholder_3d_viewer(mesh_path: str = None):
    """Placeholder for a 3D viewer component."""
    st.write("Placeholder for 3D Viewer")
    if mesh_path:
        st.write(f"Displaying mesh: {mesh_path}")
    else:
        st.write("No mesh selected.")
