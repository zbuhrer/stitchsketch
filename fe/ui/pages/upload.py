import streamlit as st
import os
from pathlib import Path
from src.photogrammetry.video_extractor import extract_frames


def show():
    """Display the upload page"""
    st.header("Upload Images or Video")

    # File uploader for images
    uploaded_images = st.file_uploader(
        "Upload Images",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png"]
    )

    # File uploader for video
    uploaded_video = st.file_uploader(
        "Upload Video",
        type=["mp4", "mov"]
    )

    # Process uploads
    if uploaded_images:
        process_image_uploads(uploaded_images)

    if uploaded_video:
        process_video_upload(uploaded_video)

    # Display uploaded files
    if "uploaded_files" in st.session_state and st.session_state.uploaded_files:
        st.success(f"{len(st.session_state.uploaded_files)
                      } images ready for processing")

        # Show image previews
        st.subheader("Image Previews")
        cols = st.columns(4)
        for i, file_path in enumerate(st.session_state.uploaded_files[:8]):
            cols[i % 4].image(file_path, width=150)

        # Next step button
        if st.button("Proceed to 3D Reconstruction"):
            st.session_state.current_page = "3D Reconstruction"
            st.rerun()


def process_image_uploads(uploaded_images):
    """Process uploaded image files"""
    user_img_dir = st.session_state.user_data_dir / "images"

    # Save images to temp directory
    for uploaded_file in uploaded_images:
        file_path = user_img_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Add to session state
        if str(file_path) not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(str(file_path))


def process_video_upload(uploaded_video):
    """Process uploaded video file"""
    user_img_dir = st.session_state.user_data_dir / "images"
    video_path = user_img_dir / uploaded_video.name

    # Save video to temp directory
    with open(video_path, "wb") as f:
        f.write(uploaded_video.getbuffer())

    # Extract frames
    with st.spinner("Extracting frames from video..."):
        extracted_frames = extract_frames(
            str(video_path),
            str(user_img_dir),
            fps=1  # Extract 1 frame per second
        )

    # Add extracted frames to session state
    for frame_path in extracted_frames:
        if frame_path not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(frame_path)

    st.success(f"Extracted {len(extracted_frames)} frames from video")
