from database import SQLiteConnection
import ast


class ConfigManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = SQLiteConnection(self.db_path)
        try:
            with self.db:  # Use context manager to ensure connection is closed
                self.db.create_config_table()  # Ensure config table exists
        except Exception as e:
            print(f"Error initializing ConfigManager: {e}")
            raise

    def get_config(self, key, default=None):
        """Retrieves a configuration value.  Returns default if not found."""
        try:
            with self.db:
                value = self.db.get_config_value(key)
                if value is not None:
                    # Attempt to parse the value as a Python literal
                    try:
                        return ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        # If parsing fails, return the raw string value
                        return value
                else:
                    return default  # Return the default value if key not found
        except Exception as e:
            print(f"Error getting config for {key}: {e}")
            return default  # Return default value in case of error

    def set_config(self, key, value):
        """Sets a configuration value.  Converts non-string values to strings."""
        # Convert value to string for storage
        value_str = str(value)
        try:
            with self.db:
                self.db.set_config_value(key, value_str)
        except Exception as e:
            print(f"Error setting config for {key}: {e}")
            raise


if __name__ == '__main__':
    # Example usage:
    try:
        config_manager = ConfigManager("test_config.db")

        # Get and set configuration values
        base_media_path = config_manager.get_config("media_base_path")
        print(f"Base Media Path: {base_media_path}")

        config_manager.set_config("media_base_path", "/new/media/path")
        base_media_path = config_manager.get_config("media_base_path")
        print(f"Updated Base Media Path: {base_media_path}")

        # Test with a non-string value (e.g., integer)
        config_manager.set_config("max_image_size", 1024)
        max_image_size = config_manager.get_config("max_image_size")
        print(f"Max Image Size: {max_image_size} (type: {type(max_image_size)})"
              )

    except Exception as e:
        print(f"ConfigManager Example Error: {e}")
