import os
import uuid

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

from .database import db_session

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

    def create_job(self, name, created_by):
        job_id = str(uuid.uuid4())
        new_job = Job(id=job_id, name=name, created_by=created_by)
        db_session.add(new_job)
        db_session.commit()

        # Create input and output directories
        media_dir = "/app/ui/media"  # Update this path if needed
        os.makedirs(f"{media_dir}/{job_id}/input", exist_ok=True)
        os.makedirs(f"{media_dir}/{job_id}/output", exist_ok=True)

        return new_job
