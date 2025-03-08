import unittest
from src import config


class TestConfig(unittest.TestCase):

    def test_temp_dir(self):
        self.assertEqual(config.TEMP_DIR, "tmp")

    def test_colmap_executable(self):
        self.assertEqual(config.COLMAP_EXECUTABLE, "colmap")

    def test_colmap_database_name(self):
        self.assertEqual(config.COLMAP_DATABASE_NAME, "database.db")

    def test_default_video_fps(self):
        self.assertEqual(config.DEFAULT_VIDEO_FPS, 1)


if __name__ == '__main__':
    unittest.main()
