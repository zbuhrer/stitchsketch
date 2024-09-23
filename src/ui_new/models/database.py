from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# use `localhost` DATABASE_URL string for local flet dev, named hostname is for the docker environment
# DATABASE_URL = "postgresql://admin:changeme@StitchSketch-PG/stitchsketch_dev"
DATABASE_URL = "postgresql://admin:changeme@localhost/stitchsketch_dev"

engine = create_engine(DATABASE_URL)
SessionFactory = scoped_session(sessionmaker(bind=engine))

# Make db_session an alias for SessionFactory
db_session = SessionFactory()
