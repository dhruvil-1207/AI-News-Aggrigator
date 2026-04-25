import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/news_db")

# The engine is the core interface to the database
engine = create_engine(DATABASE_URL, echo=True)

# The session is what we use to query and add data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our models will inherit from this Base class
Base = declarative_base()