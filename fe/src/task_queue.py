import streamlit as st
import threading
import queue
import time
import uuid
from typing import Dict, Any, List, Optional, Callable
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global task queue
task_queue = queue.Queue()

# Task status tracking
task_status: Dict[str, Dict[str, Any]] = {}
task_results: Dict[str, Any] = {}

# Lock for synchronizing access to task_status and task_results
status_lock = threading.Lock()


def generate_task_id() -> str:
    """Generate a unique task ID"""
    return str(uuid.uuid4())


def submit_task(func: Callable, args: List, kwargs: Dict[str, Any]) -> str:
    """
    Submit a task to the background queue

    Args:
        func: Function to execute
        args: Positional arguments
        kwargs: Keyword arguments

    Returns:
        task_id: Unique ID for tracking the task
    """
    task_id = generate_task_id()
    logging.info(f"Submitting task with id: {task_id}, function: {func.__name__}")

    with status_lock:
        task_status[task_id] = {
            "status": "queued",
            "progress": 0,
            "message": "Task queued",
            "created_at": time.time(),
            # Track user session
            "user_session_id": st.session_state.session_id if "session_id" in st.session_state else "unknown"
        }

    task_queue.put({
        "id": task_id,
        "func": func,
        "args": args,
        "kwargs": kwargs
    })

    return task_id


def update_task_status(task_id: str, status: str, progress: float, message: str):
    """Update the status of a task"""
    with status_lock:
        if task_id in task_status:
            logging.info(f"Updating task {task_id} status to: {status}, progress: {progress}, message: {message}")
            task_status[task_id].update({
                "status": status,
                "progress": progress,
                "message": message,
                "updated_at": time.time()
            })


def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """Get the current status of a task"""
    with status_lock:
        status = task_status.get(task_id)
        logging.info(f"Getting task status for {task_id}: {status}")
        return status


def get_task_result(task_id: str) -> Optional[Any]:
    """Get the result of a completed task"""
    with status_lock:
        result = task_results.get(task_id)
        logging.info(f"Getting task result for {task_id}: {result}")
        return result


def worker():
    """Worker thread to process tasks from the queue"""
    while True:
        try:
            task = task_queue.get()
            if task is None:
                logging.info("Worker received shutdown signal.")
                break  # Shutdown signal

            task_id = task["id"]
            func = task["func"]
            args = task["args"]
            kwargs = task["kwargs"]

            logging.info(f"Worker started processing task: {task_id}, function: {func.__name__}")

            # Update status to running
            update_task_status(task_id, "running", 0, "Task started")

            try:
                # Add progress callback to kwargs, if the function accepts it
                import inspect
                if 'progress_callback' in inspect.signature(func).parameters:
                    def progress_callback(p, msg=""):
                        update_task_status(task_id, "running", p, msg)

                    kwargs["progress_callback"] = progress_callback

                # Execute the task
                result = func(*args, **kwargs)

                # Store result
                with status_lock:
                    task_results[task_id] = result
                update_task_status(task_id, "completed", 100, "Task completed")
                logging.info(f"Task {task_id} completed successfully.")

            except Exception as e:
                # Handle errors
                update_task_status(task_id, "failed", 0, f"Error: {str(e)}")
                # Add logging for debugging
                logging.error(f"Task {task_id} failed: {e}", exc_info=True)

        except Exception as e:
            logging.error(f"Worker error: {e}", exc_info=True)
        finally:
            task_queue.task_done()

def start_workers(num_workers=2):
    """Start worker threads"""
    workers = []
    for i in range(num_workers):
        t = threading.Thread(target=worker, daemon=True, name=f"worker-{i}")
        t.start()
        workers.append(t)
        logging.info(f"Started worker thread: {t.name}")
    return workers


def cleanup_old_tasks(max_age_hours=24):
    """Clean up old completed tasks"""
    current_time = time.time()
    with status_lock:
        for task_id in list(task_status.keys()):
            status = task_status[task_id]
            if status["status"] in ["completed", "failed"]:
                task_age = current_time - \
                    status.get("updated_at", current_time)
                if task_age > max_age_hours * 3600:
                    # Remove old tasks
                    # Only clean up tasks associated with the current session
                    if status.get("user_session_id") == st.session_state.get("session_id"):
                        task_status.pop(task_id, None)
                        task_results.pop(task_id, None)
                        logging.info(f"Cleaned up old task: {task_id}")
