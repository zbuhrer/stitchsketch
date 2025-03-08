"""
Tests for the session module.
"""

import unittest
import os
import shutil
import tempfile
import streamlit as st  # Import streamlit
from pathlib import Path
from src import session


class TestSession(unittest.TestCase):
    def setUp(self):
        """Set up for test methods."""
        # Clear session state before each test
        for key in list(st.session_state.keys()):
            del st.session_state[key]

    def test_initialize_session(self):
        """
        Test that initialize_session creates a session ID and user data directory.
        """
        session.initialize_session()

        self.assertIn("session_id", st.session_state)
        self.assertIsInstance(st.session_state.session_id, str)
        # Ensure session ID is not empty
        self.assertTrue(len(st.session_state.session_id) > 0)

        self.assertIn("user_data_dir", st.session_state)
        self.assertIsInstance(st.session_state.user_data_dir, Path)
        self.assertTrue(st.session_state.user_data_dir.exists())

        # Verify subdirectories are created
        expected_subdirs = ["images", "reconstructions", "patterns"]
        for subdir in expected_subdirs:
            subdir_path = st.session_state.user_data_dir / subdir
            self.assertTrue(subdir_path.exists())

    def tearDown(self):
        """Tear down after test methods."""
        # Clean up the user data directory after the test
        if "user_data_dir" in st.session_state:
            try:
                shutil.rmtree(st.session_state.user_data_dir)
            except Exception as e:
                print(f"Error cleaning up test directory: {e}")

# streamlit run tests/test_session.py
# Test fails to run outside of Streamlit
# if __name__ == '__main__':
#     unittest.main()
