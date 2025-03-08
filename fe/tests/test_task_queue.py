"""
Tests for the task_queue module.
"""

import unittest
import time
import threading
import queue

import streamlit as st
from src import task_queue  # Import the task_queue module


class TestTaskQueue(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        # Clear session state before each test
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.session_id = "test_session_id"

        # Clear task queue and status before each test
        with task_queue.status_lock:
            task_queue.task_queue = queue.Queue()
            task_queue.task_status = {}
            task_queue.task_results = {}

        # Initialize worker threads
        self.num_workers = 2
        self.workers = task_queue.start_workers(num_workers=self.num_workers)

    def tearDown(self):
        """Tear down after test methods."""
        # Signal workers to stop
        for _ in range(self.num_workers):
            task_queue.task_queue.put(None)

        # Wait for workers to finish
        for worker in self.workers:
            worker.join()

        # Clean up task queue and status
        with task_queue.status_lock:
            task_queue.task_queue = queue.Queue()
            task_queue.task_status = {}
            task_queue.task_results = {}

    def test_submit_task(self):
        """Test that submit_task adds a task to the queue and returns a task ID."""
        def test_func():
            return "Task completed"

        task_id = task_queue.submit_task(test_func, [], {})
        self.assertIsNotNone(task_id)
        self.assertIsInstance(task_id, str)

        with task_queue.status_lock:
            self.assertIn(task_id, task_queue.task_status)
            self.assertEqual(
                task_queue.task_status[task_id]["status"], "queued")
            # Test session id
            self.assertEqual(
                task_queue.task_status[task_id]["user_session_id"], "test_session_id")

    def test_task_execution(self):
        """Test that the worker function executes a task and stores the result."""
        def test_func():
            time.sleep(0.1)  # Give the worker a chance to pick it up
            return "Task completed"

        task_id = task_queue.submit_task(test_func, [], {})
        time.sleep(0.2)  # Give the worker a chance to pick it up and complete

        with task_queue.status_lock:
            self.assertEqual(
                task_queue.task_status[task_id]["status"], "completed")
            self.assertEqual(
                task_queue.task_results[task_id], "Task completed")

    def test_update_and_get_task_status(self):
        """Test that update_task_status correctly updates the status of a task."""
        def test_func():
            return "Task completed"

        task_id = task_queue.submit_task(test_func, [], {})
        task_queue.update_task_status(
            task_id, "running", 50, "Task in progress")

        status = task_queue.get_task_status(task_id)
        self.assertEqual(status["status"], "running")
        self.assertEqual(status["progress"], 50)
        self.assertEqual(status["message"], "Task in progress")

    def test_get_task_result(self):
        """Test that get_task_result retrieves the correct result."""
        def test_func():
            return "Task completed"

        task_id = task_queue.submit_task(test_func, [], {})
        time.sleep(0.2)

        result = task_queue.get_task_result(task_id)
        self.assertEqual(result, "Task completed")

    def test_cleanup_old_tasks(self):
        """Test that cleanup_old_tasks removes old completed/failed tasks."""
        def test_func():
            return "Task completed"

        task_id = task_queue.submit_task(test_func, [], {})
        time.sleep(0.2)

        # Wait for the task to complete
        with task_queue.status_lock:
            # Set task to be 1 hour old
            task_queue.task_status[task_id]["updated_at"] = time.time() - 3600
        # Set max age to be very small
        task_queue.cleanup_old_tasks(max_age_hours=0.01)

        with task_queue.status_lock:
            self.assertNotIn(task_id, task_queue.task_status)
            self.assertNotIn(task_id, task_queue.task_results)

    def test_worker_exception_handling(self):
        """Test that the worker correctly handles exceptions raised by tasks."""
        def failing_task():
            raise ValueError("Intentional task failure")

        task_id = task_queue.submit_task(failing_task, [], {})
        time.sleep(0.2)

        with task_queue.status_lock:
            self.assertEqual(
                task_queue.task_status[task_id]["status"], "failed")
            self.assertIn("Intentional task failure",
                          task_queue.task_status[task_id]["message"])


if __name__ == '__main__':
    unittest.main()
