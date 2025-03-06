import pymysql
import sqlite3
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()  # Load environment variables from .env file

# --- Abstract Base Class for Database Connections ---


class DBConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute_query(self, query, params=None):
        pass

    @abstractmethod
    def fetch_all(self, query, params=None):
        pass

    @abstractmethod
    def fetch_one(self, query, params=None):
        pass

    @abstractmethod
    def get_database_name(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# --- MariaDB Connection Class ---
class MariaDBConnection(DBConnection):
    def __init__(self, db_host=None, db_port=3306, db_name=None, db_user=None, db_password=None):
        self.db_host = db_host or os.getenv("DB_HOST")
        self.db_port = int(db_port or os.getenv("DB_PORT", "3306"))
        self.db_name = db_name or os.getenv("DB_NAME")
        self.db_user = db_user or os.getenv("DB_USER")
        self.db_password = db_password or os.getenv("DB_PASSWORD")
        self.conn = None  # Initialize connection attribute

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                cursorclass=pymysql.cursors.DictCursor  # Use DictCursor
            )
            print(
                f"Connected to MariaDB database: {self.db_name}@{self.db_host}:{self.db_port}")
        except pymysql.err.Error as e:
            print(f"Error connecting to MariaDB database: {e}")
            self.conn = None
            raise  # Re-raise the exception for handling upstream

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def is_connected(self):
        return self.conn is not None

    def get_database_name(self):
        return self.db_name

    def execute_query(self, query, params=None):
        if not self.conn:
            raise Exception("Not connected to the database.")

        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
        except pymysql.err.Error as e:  # Changed sqlite3.Error to pymysql.err.Error
            print(f"Error executing query: {e}")
            if self.conn:
                self.conn.rollback()  # Rollback on error
            raise  # Re-raise the exception

    def fetch_all(self, query, params=None):
        if not self.conn:
            raise Exception("Not connected to the database.")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.err.Error as e:
            print(f"Error fetching data: {e}")
            raise

    def fetch_one(self, query, params=None):
        if not self.conn:
            raise Exception("Not connected to the database.")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except pymysql.err.Error as e:
            print(f"Error fetching data: {e}")
            raise

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

# --- SQLite Connection Class ---


class SQLiteConnection(DBConnection):
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None  # Initialize connection attribute

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            # Use Row factory to access columns by name
            self.conn.row_factory = sqlite3.Row
            print(f"Connected to SQLite database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")
            self.conn = None
            raise  # Re-raise the exception

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def is_connected(self):
        return self.conn is not None

    def get_database_name(self):
        return self.db_path  # For SQLite, the path is the "name"

    def execute_query(self, query, params=None):
        if not self.conn:
            raise Exception("Not connected to the database.")

        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            if self.conn:
                self.conn.rollback()  # Rollback on error
            raise  # Re-raise the exception

    def fetch_all(self, query, params=None):
        if not self.conn:
            raise Exception("Not connected to the database.")

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            raise  # Re-raise the exception

    def fetch_one(self, query, params=None):
        if not self.conn:
            raise Exception("Not connected to the database.")

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            raise  # Re-raise the exception

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def create_config_table(self):
        """Creates the config table in the SQLite database if it doesn't exist."""
        query = """
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """
        try:
            self.execute_query(query)
            print("Config table created successfully.")
        except Exception as e:
            print(f"Error creating config table: {e}")
            raise

    def get_config_value(self, key):
        """Retrieves a configuration value from the SQLite database."""
        query = "SELECT value FROM config WHERE key = ?"
        try:
            result = self.fetch_one(query, (key,))
            if result:
                return result['value']  # Access value by name
            else:
                return None
        except Exception as e:
            print(f"Error getting config value for key {key}: {e}")
            raise

    def set_config_value(self, key, value):
        """Sets a configuration value in the SQLite database."""
        query = "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)"
        try:
            self.execute_query(query, (key, value))
            print(f"Config value set successfully for key {key}.")
        except Exception as e:
            print(f"Error setting config value for key {key}: {e}")
            raise


# --- Example Usage ---
if __name__ == '__main__':
    # MariaDB Example
    try:
        with MariaDBConnection() as db:
            db.execute_query(
                "CREATE TABLE IF NOT EXISTS test (id INT, name VARCHAR(255))")
            db.execute_query(
                "INSERT INTO test (id, name) VALUES (%s, %s)", (1, "Test MariaDB"))
            result = db.fetch_all("SELECT * FROM test")
            print("MariaDB Result:", result)
    except Exception as e:
        print("MariaDB Error:", e)

    # SQLite Example
    try:
        with SQLiteConnection("test.db") as db:
            db.execute_query(
                "CREATE TABLE IF NOT EXISTS test (id INT, name TEXT)")
            db.execute_query(
                "INSERT INTO test (id, name) VALUES (?, ?)", (1, "Test SQLite"))
            result = db.fetch_all("SELECT * FROM test")
            print("SQLite Result:", result)

        # Config Table Example
        with SQLiteConnection("test.db") as db:
            db.create_config_table()
            db.set_config_value("base_media_path", "./media")
            base_media_path = db.get_config_value("base_media_path")
            print("Base Media Path from Config:", base_media_path)

    except Exception as e:
        print("SQLite Error:", e)
