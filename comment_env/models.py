from sqlalchemy import Column, Integer, String, DateTime
from comment_env.database import Base
from datetime import datetime

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    comment = Column(String, index=True)
    region = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
