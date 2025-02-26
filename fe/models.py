# stitchsketch/fe/models.py
from database import DatabaseConnection


class Account:
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
    def fetch_all(cls):
        """Fetches all accounts from the database."""
        db = DatabaseConnection()
        accounts = []
        try:
            accounts_data = db.execute_query(
                "SELECT id, name, date_entered, date_modified, modified_user_id, created_by, description, deleted, assigned_user_id FROM accounts WHERE deleted = 0 LIMIT 10", fetch=True)
            if accounts_data:
                accounts = [cls(*account_data)
                            for account_data in accounts_data]
        except Exception as e:
            print(f"Error fetching accounts: {e}")
        finally:
            # Disconnect in the finally block to ensure it always runs
            pass  # Disconnecting is now handled within execute_query.
        return accounts

    @classmethod
    def get_account_by_id(cls, account_id):
        """Fetches a single account from the database by ID."""
        db = DatabaseConnection()
        account = None
        try:
            account_data = db.execute_query(
                "SELECT id, name, date_entered, date_modified, modified_user_id, created_by, description, deleted, assigned_user_id FROM accounts WHERE id = %s", (account_id,), fetch=True)
            if account_data:
                account = cls(*account_data[0]) if account_data[0] else None
        except Exception as e:
            print(f"Error fetching account with ID {account_id}: {e}")
        finally:
            # Disconnect is now handled within execute query
            pass
        return account
