from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) # e.g., 'youtube', 'blog'
    url = Column(String, unique=True, nullable=False)

    # Establish the relationship to the articles table
    articles = relationship("Article", back_populates="source")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    summary = Column(Text, nullable=True) # Will be filled by the LLM later
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign key linking back to the Source
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source", back_populates="articles")