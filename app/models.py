from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    preferences = Column(String, default="Fireship,Wired,The Verge,Matt Wolfe") 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    subscriptions = relationship("UserSubscription", back_populates="user")

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # 'youtube' or 'blog'
    url = Column(String, unique=True, index=True)
    
    articles = relationship("Article", back_populates="source")
    subscribers = relationship("UserSubscription", back_populates="source")

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))

    user = relationship("User", back_populates="subscriptions")
    source = relationship("Source", back_populates="subscribers")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    link = Column(String, unique=True, index=True)
    published_at = Column(DateTime)
    content = Column(Text, nullable=True)     
    ai_summary = Column(Text, nullable=True)  
    source_id = Column(Integer, ForeignKey("sources.id"))

    source = relationship("Source", back_populates="articles")