import mysql.connector
from mysql.connector import pooling
import json
import os

# Load database configuration from config.json or environment variables


def load_db_config(config_file="config.json"):
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            db_config = config.get("database", {})
            return db_config
    except FileNotFoundError:
        print(f"Config file not found: {config_file}")
        return {}
    except json.JSONDecodeError:
        print(f"Invalid JSON in config file: {config_file}")
        return {}


class DatabaseConnection:
    def __init__(self, config_file="config.json"):
        self.db_config = load_db_config(config_file)
        self.pool_name = "mysql_pool"
        self.pool = self.create_pool()

    def create_pool(self):
        try:
            pool = pooling.MySQLConnectionPool(pool_name=self.pool_name,
                                               pool_size=5,  # Adjust pool size as needed
                                               **self.db_config)
            print("Connection pool created successfully.")
            return pool
        except mysql.connector.Error as err:
            print(f"Failed to create connection pool: {err}")
            return None

    def get_connection(self):
        if self.pool:
            try:
                connection = self.pool.get_connection()
                return connection
            except mysql.connector.Error as err:
                print(f"Error getting connection from pool: {err}")
                return None
        else:
            print("Connection pool is not available.")
            return None

    def execute_query(self, query, params=None, fetch=False):
        connection = self.get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                else:
                    result = None
                connection.commit()
                return result
            except mysql.connector.Error as err:
                print(f"Query execution failed: {err}")
                connection.rollback()
                return None
            finally:
                cursor.close()
                connection.close()  # Return connection to the pool
        else:
            return None

    def update_setting(self, setting_name, setting_value):
        query = "UPDATE settings SET setting_value = %s WHERE setting_name = %s"
        params = (setting_value, setting_name)
        self.execute_query(query, params)

    def get_setting(self, setting_name):
        query = "SELECT setting_value FROM settings WHERE setting_name = %s"
        params = (setting_name,)
        result = self.execute_query(query, params, fetch=True)
        if result:
            return result[0][0]  # Assuming setting_value is the first column
        else:
            return None


# Example usage (for testing purposes)
if __name__ == '__main__':
    db = DatabaseConnection()

    # Example: Update a setting
    db.update_setting('database_path', '/new/database/path')

    # Example: Retrieve a setting
    path = db.get_setting('database_path')
    print(f"Database path from DB: {path}")

    db.close_pool()
