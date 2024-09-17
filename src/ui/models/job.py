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
