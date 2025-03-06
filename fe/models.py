from database import DBConnection  # Import the abstract base class
from abc import ABC, abstractmethod


class BaseModel(ABC):  # Abstract base model class
    @classmethod
    @abstractmethod
    def get_table_name(cls):
        """Return the name of the database table for this model."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """Create an instance of the model from a dictionary."""
        pass

    @abstractmethod
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        pass


class Account(BaseModel):
    def __init__(self, id, name, date_entered, date_modified, modified_user_id, created_by, description, deleted, assigned_user_id):
        self.id = id
        self.name = name
        self.date_entered = date_entered
        self.date_modified = date_modified
        self.modified_user_id = modified_user_id
        self.created_by = created_by
        self.description = description
        self.deleted = deleted
        self.assigned_user_id = assigned_user_id

    def __repr__(self):
        return f"Account(id={self.id}, name='{self.name}')"

    @classmethod
    def get_table_name(cls):
        return "accounts"  # Fixed table name

    @classmethod
    def from_dict(cls, data):
        """Create an Account instance from a dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            date_entered=data['date_entered'],
            date_modified=data['date_modified'],
            modified_user_id=data['modified_user_id'],
            created_by=data['created_by'],
            description=data['description'],
            deleted=data['deleted'],
            assigned_user_id=data['assigned_user_id']
        )

    def to_dict(self):
        """Convert the Account instance to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'date_entered': self.date_entered,
            'date_modified': self.date_modified,
            'modified_user_id': self.modified_user_id,
            'created_by': self.created_by,
            'description': self.description,
            'deleted': self.deleted,
            'assigned_user_id': self.assigned_user_id
        }

    @classmethod
    def fetch_all(cls, db_connection: DBConnection, limit=10, offset=0):
        """Fetches all accounts from the database with pagination."""
        table_name = cls.get_table_name()
        query = f"SELECT * FROM {table_name} WHERE deleted = 0 LIMIT %s OFFSET %s"
        params = (limit, offset)  # Corrected parameter order
        try:
            accounts_data = db_connection.fetch_all(query, params)
            if accounts_data:
                accounts = [cls.from_dict(account_data)
                            for account_data in accounts_data]
                return accounts
            else:
                return []  # Return empty list if no accounts found
        except Exception as e:
            print(f"Error fetching accounts: {e}")
            raise  # Re-raise the exception
        # No finally needed, as the DB connection is handled via a context manager

    @classmethod
    def get_account_by_id(cls, db_connection: DBConnection, account_id):
        """Fetches a single account from the database by ID."""
        table_name = cls.get_table_name()
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        params = (account_id,)
        try:
            account_data = db_connection.fetch_one(query, params)
            if account_data:
                account = cls.from_dict(account_data)
                return account
            else:
                return None  # Return None if no account found
        except Exception as e:
            print(f"Error fetching account with ID {account_id}: {e}")
            raise  # Re-raise the exception
        # No finally needed, as the DB connection is handled via a context manager

    @classmethod
    def create(cls, db_connection: DBConnection, account_data: dict):
        """Creates a new account in the database."""
        table_name = cls.get_table_name()
        columns = ", ".join(account_data.keys())
        placeholders = ", ".join(["%s"] * len(account_data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        params = tuple(account_data.values())
        try:
            db_connection.execute_query(query, params)
        except Exception as e:
            print(f"Error creating account: {e}")
            raise

    def update(self, db_connection: DBConnection, account_data: dict):
        """Updates an existing account in the database."""
        table_name = self.get_table_name()
        set_clauses = ", ".join([f"{col} = %s" for col in account_data.keys()])
        query = f"UPDATE {table_name} SET {set_clauses} WHERE id = %s"
        params = tuple(account_data.values()) + (self.id,)
        try:
            db_connection.execute_query(query, params)
            # Update the current instance with the new data
            for key, value in account_data.items():
                setattr(self, key, value)
        except Exception as e:
            print(f"Error updating account: {e}")
            raise

    @classmethod
    def delete(cls, db_connection: DBConnection, account_id):
        """Deletes an account from the database."""
        table_name = cls.get_table_name()
        query = f"DELETE FROM {table_name} WHERE id = %s"
        params = (account_id,)
        try:
            db_connection.execute_query(query, params)
        except Exception as e:
            print(f"Error deleting account: {e}")
            raise
