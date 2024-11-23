# Define the database model and create the database engine
# Import the required modules
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Define the base class for declarative class definitions
Base = declarative_base()

# Load environment variables from a .env file
load_dotenv()

# Get the database URL from environment variables
db_url = os.getenv("DATABASE_URL")

# Create a new SQLAlchemy engine instance
engine = create_engine(url=db_url)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Define the PDF class which will be mapped to the 'pdfs' table in the database
class PDF_Metadata(Base):
    __tablename__ = 'pdfs'

    pdf_id = Column(Integer, primary_key=True)  # Primary key column
    filename = Column(String)  # Column to store the filename
    upload_date = Column(DateTime)  # Column to store the upload date
    content = Column(String)  # Column to store the content of the PDF

# Create all tables in the database which are defined by Base's subclasses
Base.metadata.create_all(bind=engine)

# Get the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()