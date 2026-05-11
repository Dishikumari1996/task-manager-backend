from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="todo")  # todo, in-progress, done
    user_id = Column(Integer, ForeignKey("users.id"))
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, default="medium")  # low, medium, high

user = relationship("User", back_populates="tasks")