import unittest
from unittest.mock import patch, call
from src.photogrammetry import colmap_wrapper
from src.photogrammetry import reconstruction
import tempfile
import os
import subprocess

class TestColmapWrapper(unittest.TestCase):

    @patch('src.photogrammetry.colmap_wrapper.subprocess.run')
    def test_run_colmap_sift(self, mock_run):
        # Configure mock to return success for all calls
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),  # feature_extractor
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),  # exhaustive_matcher
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),  # mapper
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")   # model_converter
        ]

        with tempfile.TemporaryDirectory() as image_dir, \
             tempfile.TemporaryDirectory() as sparse_dir:
            database_path = os.path.join(image_dir, "database.db")

            colmap_wrapper.run_colmap(image_dir, database_path, sparse_dir)

            # Assert that subprocess.run was called with the correct arguments
            calls = [
                call([
                    'colmap', 'feature_extractor', '--database_path', database_path, '--image_path', image_dir, '--ImageReader.camera_model', 'SIMPLE_RADIAL'
                ], capture_output=True, text=True, check=True),
                call([
                    'colmap', 'exhaustive_matcher', '--database_path', database_path
                ], capture_output=True, text=True, check=True),
                call([
                    'colmap', 'mapper', '--database_path', database_path, '--image_path', image_dir, '--output_path', sparse_dir
                ], capture_output=True, text=True, check=True),
                call([
                    'colmap', 'model_converter', '--input_path', os.path.join(sparse_dir, '0'), '--output_path', os.path.join(sparse_dir, 'model.ply'), '--output_type', 'PLY'
                ], capture_output=True, text=True, check=True)
            ]
            mock_run.assert_has_calls(calls, any_order=False)
            self.assertEqual(mock_run.call_count, 4)


    @patch('src.photogrammetry.colmap_wrapper.subprocess.run')
    def test_run_colmap_orb(self, mock_run):
        # Configure mock to return success for all calls
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),  # feature_extractor
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),  # exhaustive_matcher
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),  # mapper
            subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")   # model_converter
        ]

        with tempfile.TemporaryDirectory() as image_dir, \
             tempfile.TemporaryDirectory() as sparse_dir:
            database_path = os.path.join(image_dir, "database.db")

            colmap_wrapper.run_colmap(image_dir, database_path, sparse_dir, feature_type="orb")

            # Assert that subprocess.run was called with the correct arguments
            calls = [
                call([
                    'colmap', 'feature_extractor', '--database_path', database_path, '--image_path', image_dir, '--ImageReader.camera_model', 'SIMPLE_RADIAL', '--SiftExtraction.use_gpu', '0', '--SiftExtraction.num_octaves', '3', '--SiftExtraction.first_octave', '0', '--SiftExtraction.peak_threshold', '0.01', '--SiftExtraction.edge_threshold', '10'
                ], capture_output=True, text=True, check=True),
                call([
                    'colmap', 'exhaustive_matcher', '--database_path', database_path
                ], capture_output=True, text=True, check=True),
                call([
                    'colmap', 'mapper', '--database_path', database_path, '--image_path', image_dir, '--output_path', sparse_dir
                ], capture_output=True, text=True, check=True),
                call([
                    'colmap', 'model_converter', '--input_path', os.path.join(sparse_dir, '0'), '--output_path', os.path.join(sparse_dir, 'model.ply'), '--output_type', 'PLY'
                ], capture_output=True, text=True, check=True)
            ]
            mock_run.assert_has_calls(calls, any_order=False)
            self.assertEqual(mock_run.call_count, 4)


    @patch('src.photogrammetry.colmap_wrapper.subprocess.run')
    def test_create_empty_colmap_database(self, mock_run):
        # Configure mock to return success
        mock_run.return_value = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="",
            stderr=""
        )

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

class TestReconstruction(unittest.TestCase):
    @patch('src.photogrammetry.colmap_wrapper.create_empty_colmap_database')
    @patch('src.photogrammetry.colmap_wrapper.run_colmap')
    def test_run_reconstruction_colmap_error(self, mock_run_colmap, mock_create_db):
        with tempfile.TemporaryDirectory() as image_dir, \
             tempfile.TemporaryDirectory() as sparse_dir:
            database_path = os.path.join(image_dir, "database.db")

            # Configure the mock to raise a COLMAPError
            mock_run_colmap.side_effect = colmap_wrapper.COLMAPError("Simulated COLMAP error")

            # Run the reconstruction
            result = reconstruction.run_reconstruction(image_dir, database_path, sparse_dir)

            # Assert that the result is None (indicating failure)
            self.assertIsNone(result)

            # Assert that create_empty_colmap_database was called
            mock_create_db.assert_called_once_with(database_path)

            # Assert that run_colmap was called with the correct arguments
            mock_run_colmap.assert_called_once_with(image_dir, database_path, sparse_dir, progress_callback=None)

    @patch('src.photogrammetry.colmap_wrapper.create_empty_colmap_database')
    @patch('src.photogrammetry.colmap_wrapper.run_colmap')
    def test_run_reconstruction_general_exception(self, mock_run_colmap, mock_create_db):
        with tempfile.TemporaryDirectory() as image_dir, \
             tempfile.TemporaryDirectory() as sparse_dir:
            database_path = os.path.join(image_dir, "database.db")

            # Configure the mock to raise a COLMAPError
            mock_run_colmap.side_effect = ValueError("Simulated Value Error")

            # Run the reconstruction
            result = reconstruction.run_reconstruction(image_dir, database_path, sparse_dir)

            # Assert that the result is None (indicating failure)
            self.assertIsNone(result)

            # Assert that create_empty_colmap_database was called
            mock_create_db.assert_called_once_with(database_path)

            # Assert that run_colmap was called with the correct arguments
            mock_run_colmap.assert_called_once_with(image_dir, database_path, sparse_dir, progress_callback=None)

    @patch('src.photogrammetry.reconstruction.os.path.exists')
    @patch('src.photogrammetry.colmap_wrapper.create_empty_colmap_database')
    @patch('src.photogrammetry.colmap_wrapper.run_colmap')
    def test_run_reconstruction_success(self, mock_run_colmap, mock_create_db, mock_path_exists):
        with tempfile.TemporaryDirectory() as image_dir, \
             tempfile.TemporaryDirectory() as sparse_dir:
            database_path = os.path.join(image_dir, "database.db")
            ply_path = os.path.join(sparse_dir, "model.ply")

            # Configure the mocks to simulate a successful run
            mock_run_colmap.return_value = None
            mock_create_db.return_value = None
            mock_path_exists.return_value = True # Simulate that ply exists

            # Run the reconstruction
            result = reconstruction.run_reconstruction(image_dir, database_path, sparse_dir)

            # Assert that the result is the path to the ply file
            self.assertEqual(result, ply_path)

            # Assert that create_empty_colmap_database was called
            mock_create_db.assert_called_once_with(database_path)

            # Assert that run_colmap was called with the correct arguments
            mock_run_colmap.assert_called_once_with(image_dir, database_path, sparse_dir, progress_callback=None)

    @patch('src.photogrammetry.reconstruction.os.path.exists')
    @patch('src.photogrammetry.colmap_wrapper.create_empty_colmap_database')
    @patch('src.photogrammetry.colmap_wrapper.run_colmap')
    def test_run_reconstruction_no_ply(self, mock_run_colmap, mock_create_db, mock_path_exists):
        with tempfile.TemporaryDirectory() as image_dir, \
             tempfile.TemporaryDirectory() as sparse_dir:
            database_path = os.path.join(image_dir, "database.db")

            # Configure the mocks to simulate a successful run, but no ply file
            mock_run_colmap.return_value = None
            mock_create_db.return_value = None
            mock_path_exists.return_value = False # Simulate that ply doesn't exist

            # Run the reconstruction
            result = reconstruction.run_reconstruction(image_dir, database_path, sparse_dir)

            # Assert that the result is None
            self.assertIsNone(result)

            # Assert that create_empty_colmap_database was called
            mock_create_db.assert_called_once_with(database_path)

            # Assert that run_colmap was called with the correct arguments
            mock_run_colmap.assert_called_once_with(image_dir, database_path, sparse_dir, progress_callback=None)
