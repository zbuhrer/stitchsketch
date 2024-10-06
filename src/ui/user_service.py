import bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import Employee

engine = create_engine('postgresql://admin:changeme@stitchsketch-dev:5432/stitchsketch')
Session = sessionmaker(bind=engine)
session = Session()

def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(stored_password, provided_password):
    """Verify a provided password against the corresponding one from the database."""
    return bcrypt.checkpw(provided_password.encode('utif-8'), stored_password)

def create_user(name, email, password):
    """New user creation logic; implies a new employee is onboarded?"""
    hashed_password = hash_password(password)
    new_user = Employee(name=name, email=email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit
    return new_user

def auth_user(email, password):
    """Auth logic!"""
    user = session.query(Employee).filter_by(email=email).first()
    if user and verify_password(user.hashed_password, password):
        return user
    return None
