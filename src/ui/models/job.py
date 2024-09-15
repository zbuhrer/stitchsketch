#./models/job.py
import os
import datetime
from typing import Dict
from dotenv import load_dotenv

# Define the Job class
class Job:
  # Constructor method (initializer)
    def __init__(self, id: str, name: str, date_entered: datetime.date,
                 date_modified: datetime.date, modified_user_id: str, created_by: str, description: str):
        """Initializes a new Job instance.

        Args:
            id (str): Unique job ID.
            name (str): Job name.
            date_entered (datetime.date): Date the job was entered into the system.
            date_modified (datetime.date): Date the job was last modified.
            modified_user_id (str): User ID of the user who last modified the job.
            created_by (str): User ID of the user who created the job.
            description (str): Job description.
        """
        self.id = id  # Set the job's unique ID
        self.name = name  # Set the job's name
        self.date_entered = date_entered  # Set the date the job was entered
        self.date_modified = date_modified  # Set the date the job was last modified
        self.modified_user_id = modified_user_id  # Set the user ID of the last modifier
        self.created_by = created_by  # Set the user ID of the creator
        self.description = description  # Set the job's description
        


    def connect(self):
        load_dotenv()
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_name = os.getenv('DB_NAME')

        print(f"Loaded DB credentials: {self.db_host}:{self.db_port} - {self.db_user} @ {self.db_name}")

        # self.db = mysql.connector.connect(
        #     user=self.db_user,
        #     password=self.db_password,
        #     host=self.db_host,
        #     port=self.db_port,
        #     database=self.db_name
        # )
        # self.cursor = self.db.cursor()

    # Class method to create a new Job instance from a database row
    @classmethod
    def from_db_row(cls, row: Dict):
        """Creates a new Job instance from a database row.

        Args:
            row (Dict): Dictionary representing a single row in the database.

        Returns:
            Job: A new Job instance created from the database row.
        """
        return cls(
            id=row['id'],
            name=row['name'],
            date_entered=datetime.date.fromisoformat(row['date_entered']),
            date_modified=datetime.date.fromisoformat(row['date_modified']),
            modified_user_id=row['modified_user_id'],
            created_by=row['created_by'],
            description=row['description']
        )

    # def fetch_jobs_from_db(self):
    #     # Replace with your actual database query
    #     try:
    #         jobs = []  # Initialize an empty list to store job data
    #         db_query_result = self.db.query("SELECT * FROM jobs")  # Replace 'db' with your database object

    #         if db_query_result:  # Check if the query returned any results
    #             for row in db_query_result:
    #                 job = Job(
    #                     id=row[0],
    #                     name=row[1],
    #                     date_entered=datetime.date.fromisoformat(row[2]),
    #                     date_modified=datetime.date.fromisoformat(row[3]),
    #                     modified_user_id=row[4],
    #                     created_by=row[5],
    #                     description=row[6]
    #                 )
    #                 jobs.append(job)

    #         return jobs

    #     except Exception as e:
    #         print(f"Error fetching jobs from database: {e}")
    #         return []



