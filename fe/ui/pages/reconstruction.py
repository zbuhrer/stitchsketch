import streamlit as st
import time
# Or Celery equivalents
from src.task_queue import submit_task, get_task_status, get_task_result


def perform_long_running_task(progress_callback=None):
    """Simulates a long-running task with progress updates."""
    for i in range(10):
        time.sleep(0.5)
        progress = (i + 1) * 10
        if progress_callback:
            progress_callback(progress, f"Step {i+1}/10")
    return "Task completed successfully!"


def show():
    st.header("3D Reconstruction")

    if "reconstruction_task_id" not in st.session_state:
        st.session_state.reconstruction_task_id = None

    # Submit task
    if st.button("Start Reconstruction", disabled=st.session_state.reconstruction_task_id is not None):
        st.session_state.reconstruction_task_id = submit_task(
            perform_long_running_task, [], {})
        st.rerun()

    # **Display task status for *this* user session only**
    st.subheader("Task Status")  # Added section for task status
    with st.container():  # Use a container for layout
        display_task_status(st.session_state.reconstruction_task_id)


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
                st.success(f"Reconstruction complete! Result: {result}")
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
