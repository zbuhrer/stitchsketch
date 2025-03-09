import unittest
from unittest.mock import patch
from src.photogrammetry import colmap_wrapper  # Assuming this is the correct path
import tempfile
import os

class TestColmapWrapper(unittest.TestCase):

    @patch('src.photogrammetry.colmap_wrapper.subprocess.run')  # Correct the path here
    def test_run_colmap_sift(self, mock_run):
        with tempfile.TemporaryDirectory() as image_dir, \
             tempfile.TemporaryDirectory() as sparse_dir:
            database_path = os.path.join(image_dir, "database.db")

            colmap_wrapper.run_colmap(image_dir, database_path, sparse_dir)

            # Assert that subprocess.run was called with the correct arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            command = args[0]  # The command is the first argument

            self.assertEqual(command[0], "colmap")
            self.assertEqual(command[1], "feature_extractor")
            self.assertIn("--database_path", command)
            self.assertIn(database_path, command)
            self.assertIn("--image_path", command)
            self.assertIn(image_dir, command)
            self.assertNotIn("--SiftExtraction.use_gpu", command) # Ensure sift doesn't have gpu flags
            self.assertEqual(command[2], "--database_path")
            self.assertEqual(command[4], "--image_path")

    @patch('src.photogrammetry.colmap_wrapper.subprocess.run')  # Correct the path here
    def test_run_colmap_orb(self, mock_run):
        with tempfile.TemporaryDirectory() as image_dir, \
             tempfile.TemporaryDirectory() as sparse_dir:
            database_path = os.path.join(image_dir, "database.db")

            colmap_wrapper.run_colmap(image_dir, database_path, sparse_dir, feature_type="orb")

            # Assert that subprocess.run was called with the correct arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            command = args[0]  # The command is the first argument

            self.assertEqual(command[0], "colmap")
            self.assertEqual(command[1], "feature_extractor")
            self.assertIn("--database_path", command)
            self.assertIn(database_path, command)
            self.assertIn("--image_path", command)
            self.assertIn(image_dir, command)
            self.assertIn("--SiftExtraction.use_gpu", command) # Ensure orb has gpu flags
            self.assertIn("0", command)
            self.assertEqual(command[2], "--database_path")
            self.assertEqual(command[4], "--image_path")

    @patch('src.photogrammetry.colmap_wrapper.subprocess.run')
    def test_create_empty_colmap_database(self, mock_run):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "database.db")
            colmap_wrapper.create_empty_colmap_database(database_path)

            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            command = args[0]

            self.assertEqual(command[0], "colmap")
            self.assertEqual(command[1], "database_creator")
            self.assertIn("--database_path", command)
            self.assertIn(database_path, command)
            self.assertEqual(command[2], "--database_path")
