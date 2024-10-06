from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, Date, Enum, UUID, TIMESTAMP, Text
from sqlalchemy.orm import relationship, backref, declarative_base
from datetime import datetime

import uuid

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(String)
    created_on = Column(TIMESTAMP, default=datetime.now())
    modified_on = Column(TIMESTAMP, onupdate=datetime.now())

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum('Pending', 'In Progress', 'Complete', 'Cancelled'), nullable=False)
    created_by = Column(String, nullable=False)
    created_on = Column(TIMESTAMP, default=datetime.now())
    modified_on = Column(TIMESTAMP, onupdate=datetime.now())
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    due_date = Column(Date)
    priority = Column(Enum('Low', 'Medium', 'High'), nullable=False)

class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)

class JobMaterial(Base):
    __tablename__ = 'job_materials'
    job_id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('Pending', 'Paid', 'Overdue'), nullable=False)
    issued_on = Column(TIMESTAMP, default=datetime.now())
    due_on = Column(TIMESTAMP, nullable=False)

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)

    def __init__(self, name, email, hashed_password):
        self.name = name
        self.email = email
        self.hashed_password = hashed_password

class JobAssignment(Base):
    __tablename__ = 'job_assignments'
    job_id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
    assigned_on = Column(TIMESTAMP, default=datetime.now())
