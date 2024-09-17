from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "postgresql://admin:changeme@localhost/stitchsketch_dev"

engine = create_engine(DATABASE_URL)
SessionFactory = scoped_session(sessionmaker(bind=engine))

# Make db_session an alias for SessionFactory
db_session = SessionFactory()
