import pymysql
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class DatabaseConnection:
    def __init__(self):
        # Default to localhost
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "3306"))  # Default to 3306
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            print(f"Connected to MariaDB database: {
                  self.db_name}@{self.db_host}:{self.db_port}")
        except pymysql.err.Error as e:
            print(f"Error connecting to MariaDB database: {e}")
            self.conn = None

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def is_connected(self):
        return self.conn is not None

    def get_database_name(self):
        return self.db_name

    def get_number_of_accounts(self):
        if not self.conn:
            return 0
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM accounts")
            count = cursor.fetchone()[0]
            return count
        except pymysql.err.Error as e:
            print(f"Error fetching account count: {e}")
            return 0

    def execute_query(self, query, params=None):
        if not self.conn:
            print("Not connected to the database.")
            return None

        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor.fetchall()
        except pymysql.err.Error as e:
            print(f"Error executing query: {e}")
            return None

    # Example usage (can be removed later)
    def create_accounts_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """
        self.execute_query(query)

    def insert_account(self, name):
        query = "INSERT INTO accounts (name) VALUES (?)"
        self.execute_query(query, (name,))

    def fetch_all_accounts(self):
        query = "SELECT id, name FROM accounts"
        return self.execute_query(query)


# Example usage:
if __name__ == '__main__':
    db_connection = DatabaseConnection()
    db_connection.create_accounts_table()
    db_connection.insert_account("Test Account 1")
    db_connection.insert_account("Test Account 2")

    accounts = db_connection.fetch_all_accounts()
    if accounts:
        for account in accounts:
            print(f"Account ID: {account[0]}, Name: {account[1]}")
    else:
        print("No accounts found.")

    db_connection.disconnect()
