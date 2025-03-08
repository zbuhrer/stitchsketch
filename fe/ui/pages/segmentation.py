import streamlit as st
from ui.components import placeholder_3d_viewer


def show():
    """Display the mesh segmentation page"""
    st.header("Mesh Segmentation")

    # Check if a mesh has been loaded
    if "mesh_id" not in st.session_state or not st.session_state.mesh_id:
        st.warning("Please upload and reconstruct a 3D model first.")
        return

    # Display the mesh (replace with actual 3D viewer component)
    st.subheader("3D Mesh")
    placeholder_3d_viewer(mesh_path=st.session_state.get("mesh_path"))

    # Mesh segmentation tools
    st.subheader("Segmentation Tools")

    # Region selection
    st.subheader("Region Selection")
    selected_regions = st.multiselect(
        "Select regions on the mesh",
        # Replace with actual region names
        ["Region 1", "Region 2", "Region 3"],
        default=st.session_state.get("selected_regions", [])
    )

    # Update session state
    st.session_state.selected_regions = selected_regions

    # Next Step
    if st.button("Proceed to Pattern Generation"):
        st.session_state.current_page = "Pattern Generation"
        st.rerun()
