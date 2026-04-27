import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")# The engine is the core interface to the database
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "connect_timeout": 10,  
    },
    pool_pre_ping=True,
    pool_recycle=300
)
# The session is what we use to query and add data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our models will inherit from this Base class
Base = declarative_base()