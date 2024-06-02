from sqlalchemy import Column, Integer, String
from .database import Base

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    comment = Column(String, index=True)
