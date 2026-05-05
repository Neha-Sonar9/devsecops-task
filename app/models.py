from sqlalchemy import Column, Integer, String
from .database import Base

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    payload = Column(String)