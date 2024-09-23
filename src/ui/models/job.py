import os
from uuid import UUID, uuid4
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

from models.database import db_session  # Adjust the import path if needed

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(String(100), nullable=False, default='In Progress')
    created_by = Column(String(255), nullable=False)
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow)
    modified_on = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """Initializes a new Job instance.

        Args:
            kwargs (dict): Keyword arguments representing the job attributes.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create_job(cls, name: str, created_by: str) -> 'Job':
        """Creates a new job and saves it to the database."""
        new_job = cls(id=str(uuid4()), name=name, created_by=created_by)
        db_session.add(new_job)
        db_session.commit()

        # Create necessary directories for job data
        os.makedirs(f"data/jobs/{new_job.id}", exist_ok=True)

        return new_job

    def __repr__(self):
        return f"<Job(id={self.id}, name='{self.name}', status='{self.status}')>"
