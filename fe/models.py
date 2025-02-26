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
        try:
            db.connect()
            # limit to 10 to prevent application hangs
            accounts_data = db.execute_query(
                "SELECT id, name, date_entered, date_modified, modified_user_id, created_by, description, deleted, assigned_user_id FROM accounts WHERE deleted = 0 LIMIT 10")
            accounts = [cls(**account_data) for account_data in accounts_data]
            return accounts
        except Exception as e:
            print(f"Error fetching accounts: {e}")
            return []
        finally:
            db.disconnect()

    @classmethod
    def get_account_by_id(cls, account_id):
        """Fetches a single account from the database by ID."""
        db = DatabaseConnection()
        try:
            db.connect()
            account_data = db.fetch_one(
                "SELECT id, name, date_entered, date_modified, modified_user_id, created_by, description, deleted, assigned_user_id FROM accounts WHERE id = %s", (account_id,))
            if account_data:
                return cls(**account_data)
            else:
                return None
        except Exception as e:
            print(f"Error fetching account with ID {account_id}: {e}")
            return None
        finally:
            db.disconnect()
